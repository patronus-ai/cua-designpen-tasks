# 00336 — "Create new text style" dialog: preset-only font size; text styles cannot be edited or deleted

## Root cause analysis

The Styles "+" → Text dialog is `cua_designpen/src/components/properties/LocalStylesSection.vue` (title computed at line 163-168: `if (styleKind.value === 'TEXT') return 'Create new text style'`).

**Preset-only font size.** The dialog's font-size control is a hardcoded preset list rendered through `AppSelect` (a button/listbox combobox, not a text input):

- `LocalStylesSection.vue:117-127`
  ```ts
  const fontSizeOptions = [
    { value: 8, label: '8' }, { value: 10, label: '10' }, { value: 12, label: '12' },
    { value: 14, label: '14' }, { value: 16, label: '16' }, { value: 20, label: '20' },
    { value: 24, label: '24' }, { value: 32, label: '32' }, { value: 48, label: '48' }
  ]
  ```
- `LocalStylesSection.vue:795-799`
  ```html
  <AppSelect
    v-model="fontSize"
    :options="fontSizeOptions"
    :ui="{ trigger: 'h-8 rounded-md border border-border bg-input px-2 text-xs' }"
  />
  ```
  No 40, no free typing — the only sizes creatable are the nine presets. This diverges from the Typography panel, which renders font size as an editable `ScrubInput` (typed values allowed) with a richer preset list that includes 40: `src/components/properties/TypographySection.vue:564-586` (`<ScrubInput ... :model-value="ctx.node.value.fontSize" @commit=...>`) and `TypographySection.vue:109` `const FONT_SIZE_PRESETS = [10, 11, 12, 13, 14, 16, 20, 24, 32, 36, 40, 48, 64, 96, 128]`. (Line height and letter spacing in the same dialog ARE plain editable inputs, lines 801-835, making the size combobox an inconsistency within the dialog itself.)

**No edit path from the Styles panel.** Each listed text style row renders `StyleRowName` (`LocalStylesSection.vue:1078-1093`), whose only affordance is the pencil button wired to inline rename: `src/components/properties/StyleRowName.vue:34-45` (`Tip label="Rename style"` → `emit('start')` → `rename.start`), committing through `editor.renameLocalStyleWithUndo(...)` (`LocalStylesSection.vue:208-211`). The property editor for text styles exists — `src/components/properties/TextStyleEditorPopover.vue` (writes via `editor.updateTextStyleWithUndo`, line 68) — but it is mounted only inside the Typography section (`TypographySection.vue:296`) and opened only via `openStyleEditor(ctx.node.value)` (`TypographySection.vue:239-244, 291, 385`), which requires a selected text node that already has the style applied. From the Styles panel list there is no way to edit a style's font/size/spacing.

**No delete path anywhere.** The scene graph supports removal — `removeTextStyle(id)` at `packages/core/src/scene-graph/index.ts:452` — but no UI component ever calls it as a user action: the only call sites are undo-inverse closures (`packages/core/src/editor/styles.ts:215`). Grep across `src/` finds no delete/trash affordance for text styles (the analogous `removePaintStyle` calls at `LocalStylesSection.vue:307` and `SelectionColorsSection.vue:115` are also only undo inverses). Styles accumulate permanently.

## Proposed fix

1. Replace the `AppSelect` at `LocalStylesSection.vue:795-799` with the same editable pattern the Typography panel uses: a `ScrubInput` (already imported at line 30) bound to `fontSize` with `:min="1"`, plus the preset dropdown fed by the shared `FONT_SIZE_PRESETS` list (lift `FONT_SIZE_PRESETS` from `TypographySection.vue:109` into a shared module, e.g. `packages/vue/src/controls/typography`, so both surfaces use one list that includes 40). Delete the local `fontSizeOptions` (lines 117-127).
2. Add per-row actions to the Styles panel text-style rows (`LocalStylesSection.vue:1078-1093`): an "Edit style" button that opens `TextStyleEditorPopover` with that `style.id` (mount the popover in `LocalStylesSection.vue` with its own `open`/`styleId` refs, mirroring `TypographySection.vue:236-244,296`), and a "Delete style" button calling a new `editor.deleteTextStyleWithUndo(styleId)` in `packages/core/src/editor/styles.ts` that snapshots the style, calls `graph.removeTextStyle(id)`, detaches/clears `textStyleId` on nodes referencing it, and pushes an undo entry restoring both.

## Acceptance criteria

- In Styles "+" → Text, the Size control accepts a typed value: typing 40 and creating the style yields a text style with `fontSize === 40` (visible in the row meta as "40/Auto").
- The Size control's preset dropdown offers the same list as the Typography panel's font-size presets (10, 11, 12, 13, 14, 16, 20, 24, 32, 36, 40, 48, 64, 96, 128).
- Typed non-preset values (e.g. 17, 40.5) are accepted and clamped to ≥ 1; invalid text does not clobber the current value.
- Each text style row in the Styles panel exposes Edit and Delete actions in addition to Rename.
- Edit opens the text-style editor for that style without requiring any node selection; committing a change (e.g. size 12 → 18) updates the style and re-renders nodes bound to it.
- Delete removes the style from `editor.graph.textStyles`, clears `textStyleId` from nodes that referenced it (their resolved text properties are preserved as local values), and is undoable (undo restores the style and the node bindings).

## Regression tests to add

- Unit (`src/components/properties/create-text-style.test.ts` or a new `local-styles-section.test.ts`): creating a TEXT style through the dialog's model with `fontSize` set to 40 produces `createTextStyleWithUndo(name, {... fontSize: 40 ...})`; a value of 0/negative is clamped by the existing `Math.max(1, fontSize.value)` guard (`LocalStylesSection.vue:283`).
- Unit (shared presets): assert the exported `FONT_SIZE_PRESETS` contains 40 and that both the Typography panel and the create dialog consume the same exported constant (import-identity test).
- Unit (`packages/core/src/editor/styles` tests): `deleteTextStyleWithUndo` removes the style, clears `textStyleId` on a node that had it applied, and `undo()` restores both the style object and the node's `textStyleId`.
- Component test (Vue Test Utils) on `LocalStylesSection.vue`: the TEXT create panel renders an editable size input (`input` element accepting keyboard input), not a `role="combobox"` button; typing "40" + Enter updates the bound `fontSize` ref to 40.
- Component test: a rendered `local-text-style` row exposes buttons with accessible names matching /edit/i and /delete/i; clicking delete for a style used by a node emits the delete action with that style id.
- E2E: open Styles "+" → Text, type 40 into Size, Create style → assert a `local-text-style` row shows "40/Auto"; then Edit it to 18 → row shows "18/Auto"; then Delete it → row disappears and Cmd/Ctrl+Z restores it.
