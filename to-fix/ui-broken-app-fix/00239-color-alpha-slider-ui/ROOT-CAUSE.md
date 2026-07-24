# 00239 — Color picker alpha: fractional slider values, disagreeing rounded readouts, and no-op typed opacity

## Root cause analysis

Three cooperating defects, all in the solid-color picker path:

1. **Slider lands on fractional percents.** The alpha slider operates on the raw 0-1 unit with a 0.001 step — `cua_designpen/src/components/ColorPickerPanel/HueAlphaSliders.vue:28-40`:
   ```html
   <PickerSlider
     label="A"
     :model-value="ctx.color.a"
     :min="0" :max="1" :step="0.001"
     ...
     @update:model-value="ctx.updateAlphaValue"
   />
   ```
   `updateAlphaValue` → `updateAlpha` stores the value verbatim (only clamped), `packages/vue/src/primitives/ColorPicker/model.ts:81-86`. Dragging can therefore commit `a = 0.495` (49.5%).

2. **Disagreeing readouts.** The picker's opacity field rounds to an integer — `packages/core/src/color/picker-solid.ts:28-31`:
   ```ts
   /** 0–1 alpha → integer percent shown in the opacity field. */
   export function unitToOpacityField(unit: number): number {
     return Math.round(clampUnit(unit) * 100)
   }
   ```
   (consumed at `src/components/ColorPickerPanel/context.ts:62` `const opacityField = computed(() => unitToOpacityField(color.value.a))`). The Fill panel's opacity control instead rounds to 2 decimals — `src/components/properties/color-style-row.ts:18-20`:
   ```ts
   export function opacityPercent(opacity: number) {
     return roundPanelNumber(opacity * 100)
   }
   ```
   where `roundPanelNumber` is `roundDisplayNumber` (`packages/core/src/format-number.ts:5-12`, `Number.parseFloat(value.toFixed(2))`), displayed via `ScrubInput` in `src/components/properties/ColorStyleRow.vue:66-73`. So `a = 0.495` reads "50%" in the picker and "49.5%" in the Fill row simultaneously.

3. **Typing "50" is a no-op.** The picker's opacity input commits only on the native `change` event against the rounded display value — `src/components/ColorPickerPanel/FormatControls.vue:34-42`:
   ```html
   <input
     data-test-id="color-opacity-input"
     type="number" min="0" max="100"
     :value="ctx.opacityField"
     @change="ctx.commitOpacity(inputNumberValue($event))"
   />
   ```
   With `a = 0.495` the input already displays "50" (the `Math.round`ed value). A browser fires `change` only when the element's value differs from the value it had when editing began — so typing "50" over "50" never fires the handler and `commitOpacity` (`context.ts:109-112`) is never called; the stored alpha stays 0.495. The "change detection comparing against the displayed rounded text" is exactly this native `change` semantics on `:value="ctx.opacityField"`; there is no keydown-Enter/blur commit path that would compare against the underlying un-rounded alpha.

## Proposed fix

1. Quantize slider commits to the field precision: in `context.ts` `updateAlphaValue` (lines 76-78), round to the displayed unit before storing — `updateColor(updateAlpha(color.value, Math.round(alpha * 100) / 100))` — or change the slider step to `0.01` in `HueAlphaSliders.vue:33`, so a drag can only produce whole-percent alphas and the two readouts cannot diverge.
2. Unify readout precision: make `unitToOpacityField` (`picker-solid.ts:29-31`) use the same panel rounding as the Fill row (`roundDisplayNumber(unit * 100)`) — with fix 1 in place both will show integers, and any legacy fractional alpha (e.g. from an imported document) shows identically ("49.5") in both places.
3. Kill the no-op: commit the opacity field on Enter and blur explicitly instead of relying on native `change` alone — add `@keydown.enter="ctx.commitOpacity(inputNumberValue($event))"` and `@blur="ctx.commitOpacity(inputNumberValue($event))"` in `FormatControls.vue`, and have `commitOpacity` early-return only when the parsed percent equals the *un-rounded* current percent (`color.value.a * 100`), not the displayed text. Then typing "50" over a displayed "50" that masks 49.5% snaps alpha to exactly 0.5.

## Acceptance criteria

- Dragging the picker's alpha slider produces only whole-percent alpha values (`Math.round(a*100) === a*100` after every drag commit); the slider thumb no longer lands on values like 49.5%.
- At any stored alpha, the picker opacity field and the Fill panel opacity field display the same number (e.g. legacy `a = 0.495` shows "49.5" in both, never "50" vs "49.5").
- With stored alpha 0.495 and the picker field displaying its value, typing "50" and pressing Enter (or blurring) sets alpha to exactly 0.5; both readouts then show "50".
- Typing the currently-true value (e.g. "50" when alpha is exactly 0.5) causes no state change, no undo entry, and no re-render churn.
- Typing values out of range clamps: "150" → 100%, "-5" → 0%; clearing the field or typing non-numeric text does not clobber the current alpha (existing `Number.isNaN` guard in `commitOpacity`, `context.ts:110`).

## Regression tests to add

- Unit (`packages/core/src/color` tests): `unitToOpacityField(0.495)` returns `49.5` (post-fix precision-unified), `unitToOpacityField(0.5)` returns `50`; property test: for any `a ∈ [0,1]`, `unitToOpacityField(a) === opacityPercent(a)` (picker and Fill panel formatters agree).
- Unit (picker context): with color `{r,g,b,a:0.495}`, `commitOpacity(50)` emits an update with `a === 0.5` (not skipped); `commitOpacity(49.5)` with `a === 0.495` emits nothing (true no-change short-circuit); `commitOpacity(NaN)` emits nothing.
- Unit (slider quantization): `updateAlphaValue(0.4951)` emits `a === 0.5`; `updateAlphaValue(0.126)` emits `a === 0.13`.
- Component test on `FormatControls.vue` + provider: mount with `a = 0.495`; set the opacity input's value to "50" and dispatch `keydown.Enter` — assert an `update` event with `a === 0.5` fires even though the DOM string did not change (regression for the native-change no-op).
- E2E: set a rectangle fill, open the color picker, drag the alpha slider to mid-range, and assert (via state bridge) `fill.color.a * 100` is an integer AND the Fill panel opacity text equals the picker opacity text; then type "50" + Enter in the picker field and assert `a === 0.5` and both readouts show "50".
