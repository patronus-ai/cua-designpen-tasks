# 00083 — Zero padding renders no padding band: canvas padding edit unreachable

All paths below are in the app source at `/Users/mateuszszczech/Desktop/patronus-gyms/cua_designpen` (working tree == deployed release `cua_designpen-0.1.8` for every cited file; verified by diff).

## Root cause analysis

The padding band's **hit zone is gated on `padding > 0` and sized by the padding value itself**, so a padding of 0 produces no hover target, no highlight, and no double-click zone — the documented double-click-the-padding-band interaction cannot start.

1. **Hit detection** — `packages/vue/src/shared/input/auto-layout-hover.ts:24-79` (`resolvePaddingHover`). Every side is wrapped in a strictly-positive guard, e.g. top (lines 32-40):
   ```ts
   if (node.paddingTop > 0) {
     const tickY = node.paddingTop / 2
     if (isNear(localX, centerX) && isNear(localY, tickY)) {
       return { nodeId: node.id, kind: 'padding-value', side: 'top' }
     }
     if (localY <= Math.min(node.paddingTop, AUTO_LAYOUT_HOVER_PADDING_REGION_TOLERANCE)) {
       return { nodeId: node.id, kind: 'padding', side: 'top' }
     }
   }
   ```
   (bottom at :42-53, left at :55-63, right at :65-76; `AUTO_LAYOUT_HOVER_PADDING_REGION_TOLERANCE = 20` at `packages/core/src/constants.ts:105`). With `paddingTop === 0` the whole block is skipped; even without the guard, the band condition `localY <= Math.min(0, 20)` would only match the 1-px edge line `localY <= 0`. So for padding = 0 `resolvePaddingHover` returns `null` for that side.

2. **Double-click entry point** — `packages/vue/src/canvas/useCanvasInput.ts:234-251` (`startAutoLayoutPaddingEdit`, wired to `dblclick` via `onDblClick`, listener registered at line 816):
   ```ts
   const hover = resolveAutoLayoutHover(cx, cy, editor)
   if (hover?.kind !== 'padding' && hover?.kind !== 'padding-value') return false
   ```
   Since step 1 never yields a `padding`/`padding-value` hover at 0, the double-click falls through to the ordinary dblclick behavior (drill into child / text edit) and the inline padding editor (`autoLayoutPaddingEdit`, lines 242-247) can never open. Once padding is made non-zero via the panel (`PaddingControls.vue`), the guards pass and the interaction works — matching the observed behavior.

3. **Rendering (why there's also no visual band)** — `packages/core/src/canvas/overlays/auto-layout-hover.ts`:
   - `paddingRect` (lines 159-168) sizes the band by the padding value: `if (side === 'top') return [abs.x, abs.y, node.width, node.paddingTop]` → a zero-height rect.
   - `drawStripedRect` (lines 81-82) early-returns on it: `if (width <= 0 || height <= 0) return`.
   - The center hover ticks are likewise gated `if (node.paddingTop > 0)` etc. in `drawBaselineTicks` (lines 176-197).
   So even if a hover were synthesized, nothing would draw for a zero side.

Summary: hit area == painted band == the padding value itself, with explicit `> 0` gates at `auto-layout-hover.ts:32/42/55/65` (input) and `overlays/auto-layout-hover.ts:82/162-167/176-197` (render). Zero padding therefore has no hover highlight, no hit zone, and no double-click affordance; the only way to bootstrap is the Design panel.

## Proposed fix

Give each padding side a minimum interactive band at the frame's inner edge, independent of the padding value:

1. In `resolvePaddingHover` (`packages/vue/src/shared/input/auto-layout-hover.ts`), remove the `> 0` gates and use a minimum region: for top, `if (localY <= Math.max(Math.min(node.paddingTop, TOLERANCE), MIN_PADDING_HIT))` with a new constant `AUTO_LAYOUT_HOVER_MIN_PADDING_HIT` (e.g. 4-6 canvas px, ideally screen-px divided by zoom so it stays clickable at any zoom). Keep the value-tick (`padding-value`) branch gated on `> 0` (there is no tick to hit at 0), but return `kind: 'padding'` for the edge band. Ordering note: run spacing detection first (already the case, `resolveAutoLayoutHover:138-139`) so the new edge bands don't swallow gap hits.
2. In the renderer, when a side's padding is 0 but it is the current hover (`overlays/auto-layout-hover.ts` `drawPaddingHover`, lines 232-253), draw a thin highlight line/strip at the edge (e.g. a 2-screen-px striped strip via a floored minimum in `paddingRect`) so the zero-padding band is discoverable; keep `drawStripedRect`'s `<= 0` guard for non-hovered geometry.
3. No change needed in `startAutoLayoutPaddingEdit`/`updateAutoLayoutPaddingEdit` (`useCanvasInput.ts:234-277`) — they already handle value 0 (`Math.max(0, value)`), so once the hover resolves, double-click-to-edit works from 0.

## Acceptance criteria

- With a selected auto-layout frame whose padding is 0 on all sides, hovering within the minimum edge band (a few px inside any inner edge) shows the padding hover highlight for that side.
- Double-clicking that band opens the inline padding editor with value 0; typing a number commits it (undo entry "Update padding") — no trip to the Design panel needed.
- The value pill/tick interactions for non-zero padding are unchanged (hover band width still equals the padding once > 0, capped by the 20px region tolerance).
- Gap (`itemSpacing`) hover/dblclick on the same frame still wins inside gaps — the new edge bands do not intercept spacing hits.
- Double-click in the frame's content area (away from edges/gaps) still drills into the child as before.
- At high zoom the edge band does not balloon (stays a constant screen-size affordance), and at low zoom it remains hittable.

## Regression tests to add

- **Unit (`resolvePaddingHover`, vitest):** frame 200x100, `layoutMode: 'VERTICAL'`, all paddings 0, single-selected: assert `resolveAutoLayoutHover(x, y)` returns `{ kind: 'padding', side: 'top' }` for a point 2px below the top inner edge (center-x), and correspondingly for bottom/left/right; assert a center point still returns `null`.
- **Unit:** same frame with `paddingTop: 30`: point at `localY = 25` returns top band (existing behavior preserved, `min(30, 20)` cap respected → assert `localY = 25` actually misses per the tolerance rule and `localY = 15` hits — pin the current capped semantics).
- **Unit (precedence):** two children with `itemSpacing: 12`, padding 0: a point inside the gap returns `kind: 'spacing'`, not a padding band.
- **Unit (`startAutoLayoutPaddingEdit`):** with the zero-padding frame selected, synthesize a dblclick at the top edge band → assert `autoLayoutPaddingEdit.value` is set with `side: 'top', value: 0`; commit `16` → assert `paddingTop === 16` and one undo entry labeled `Update padding`.
- **Render unit (mock canvas):** `drawPaddingHover` with hover side `top` and `paddingTop: 0` issues at least one draw call (the minimum-strip highlight); with no hover, zero draw calls for zero sides.
- **E2E:** seed an auto-layout frame with padding 0, select it, dispatch dblclick at (frameCenterX, frameTop + 3px) on the canvas, type `24`, Enter; assert via MCP `get_node` that `paddingTop === 24`.
