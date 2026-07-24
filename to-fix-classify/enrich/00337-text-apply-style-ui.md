# 00337 — "Create new text style" modal overflows a 720px viewport; "Create style" button below the fold; not scrollable

## Root cause analysis

The dialog is not a collision-aware popover — it is a plain `Teleport`-ed fixed-position `div` with manually computed coordinates, in `cua_designpen/src/components/properties/LocalStylesSection.vue`:

- Container (lines 637-643):
  ```html
  <Teleport to="body">
    <div
      v-if="popoverOpen"
      data-test-id="local-style-create-popover"
      :class="popoverCls.content"
      :style="createPanelStyle"
    >
  ```
- Styling (lines 85-87):
  ```ts
  const popoverCls = usePopoverUI({
    content: 'fixed w-[420px] max-w-[calc(100vw-2rem)] overflow-hidden p-0'
  })
  ```
  There is **no `max-height`**, **no `overflow-y-auto`**, and no internal flex layout that pins the footer; `overflow-hidden` only clips, it never scrolls. The "Create style" footer (lines 1060-1069) is the last block in normal flow, so it sits at the very bottom of the un-clamped panel.
- Positioning (lines 240-259, `updateCreatePanelPosition`):
  ```ts
  const left = Math.max(CREATE_PANEL_PADDING, sidebarLeft - CREATE_PANEL_WIDTH - CREATE_PANEL_OFFSET)
  const top = Math.max(CREATE_PANEL_PADDING, anchorRect?.top ?? sidebarRect?.top ?? CREATE_PANEL_PADDING)
  ```
  `top` is anchored to the Styles-section "+" button (`createButtonRef`, line 92/588) and clamped **only against the top edge** (`Math.max`). There is no bottom-edge clamp and no `avoid-collisions` behavior (unlike the reka `PopoverContent` used elsewhere, e.g. `TextStyleCreatePopover.vue:59-67` which passes `:collision-padding="16"` / `:avoid-collisions="true"`).

Why it overflows at 1280x720 specifically: the Styles section sits low in the right panel's Design tab (below Position/Layout/Appearance/Fill/etc.), so `anchorRect.top` is typically several hundred px down. The TEXT panel content — header (~41px, lines 644-654) + fixed `h-[128px]` preview (line 657) + `p-4` body with name/description grid, Properties heading, font input, style/size selects, line-height/letter-spacing rows (lines 680-836) + footer (~41px) — totals roughly 450-500px. `top(≈300-600) + height(≈480) > 720`, pushing the footer below the viewport; because the div is `position: fixed` the page cannot scroll to it, and the panel itself has no scrollbar. Nothing recomputes the position on window resize either (`updateCreatePanelPosition` runs once per open, line 236).

## Proposed fix

In `LocalStylesSection.vue`:

1. Clamp and scroll the panel. Change the popover classes (line 86) to a flex column with a viewport-derived max height, e.g.
   `'fixed w-[420px] max-w-[calc(100vw-2rem)] max-h-[calc(100vh-24px)] flex flex-col overflow-hidden p-0'`,
   make the middle content region (`<div class="space-y-3 p-4">`, line 680, plus the preview block) a `min-h-0 flex-1 overflow-y-auto` scroll area, and keep the header (line 644) and the footer (line 1060) as `shrink-0` siblings so "Create style" is always pinned visible.
2. Clamp the computed `top` against the bottom edge in `updateCreatePanelPosition` (lines 254-258): after measuring (or estimating) the panel height, `top = Math.min(top, window.innerHeight - panelHeight - CREATE_PANEL_PADDING)` with the existing `Math.max(CREATE_PANEL_PADDING, ...)` floor — mirroring the collision behavior reka popovers get for free. (Alternative, larger refactor: render the panel as a reka `PopoverContent` with `avoid-collisions`, as `TextStyleCreatePopover.vue` already does.)
3. Recompute position on window `resize` while `popoverOpen` is true.

## Acceptance criteria

- At a 1280x720 viewport, opening Styles "+" → Text shows the entire dialog inside the viewport: the header, and the "Create style" button (`data-test-id="local-style-create-submit"`) are fully visible without any scrolling of the page.
- If the dialog's natural content is taller than the viewport, the middle section scrolls (`overflow-y`) while the title bar and the "Create style"/close controls remain visible (pinned header/footer).
- The dialog never extends past the bottom viewport edge: its bounding box satisfies `bottom <= window.innerHeight - 12` (CREATE_PANEL_PADDING) for every style kind (TEXT, PAINT, EFFECT, GRID — PAINT/EFFECT lists grow via the "+" property button and must scroll, not overflow).
- Behavior holds regardless of where the Styles "+" anchor sits (e.g. with many sections expanded pushing it near the bottom of the panel).
- Resizing the window while the dialog is open keeps it fully on-screen.

## Regression tests to add

- Unit (extract position math into a pure helper, e.g. `createPanelPosition({anchorTop, sidebarLeft, viewportHeight, panelHeight})`): assert `top + panelHeight <= viewportHeight - 12` for anchorTop values 0, 300, 600, 719; assert the existing left clamp (`>= 12`) is preserved.
- Component test (Vue Test Utils, jsdom with mocked rects): open the TEXT create panel with a mocked anchor at `top: 600` and `window.innerHeight = 720`; assert the rendered container's inline `top` plus its max-height keeps it within 720, and that the container class list includes a `max-h` and the body region an `overflow-y-auto`.
- Component test: the submit button is a descendant of a non-scrolling footer sibling of the scroll region (structure assertion), so it cannot be scrolled out of view.
- E2E at 1280x720: click Styles "+" → Text; assert `local-style-create-submit` is in-viewport (`getBoundingClientRect().bottom <= 720`) and clickable; fill a name and click it; assert the style row appears. Repeat for EFFECT kind after adding 6 extra effect properties (forces tall content) — the submit button must still be reachable via the panel's internal scroll.
- E2E resize: open the dialog at 1280x900, resize to 1280x600, assert the dialog is still fully within the viewport and the submit button clickable.
