# 00317 — Standard ligatures toggle missing from Type settings → Details → Letterforms

## Root cause analysis

The "Standard ligatures" row is NOT missing from the code — it is the first row of the Letterforms dictionary:

- `cua_designpen/packages/core/src/text/feature-sections.ts:32-37`
  ```ts
  const LETTERFORM_ROWS = [
    { label: 'Standard ligatures', tags: ['liga'] },
    { label: 'Rare ligatures', tags: ['dlig', 'hlig'] },
    { label: 'Contextual alternates', tags: ['calt'] },
    { label: 'Ordinals', tags: ['ordn'] }
  ]
  ```

The row is removed at render time by the declared-tag filter in `buildFeatureSections`:

- `cua_designpen/packages/core/src/text/feature-sections.ts:83-88`
  ```ts
  const declaredRows = (rows: FeatureRow[]) =>
    rows
      .map((row) => ({ ...row, tags: row.tags.filter((tag) => hasFeature(catalog, tag)) }))
      .filter((row) => row.tags.length > 0)
  ```
  A row renders only when the font's GSUB/GPOS feature list declares at least one of its tags ("Figma's don't show what the font doesn't have", per the comment at `src/components/properties/TypeDetailsSections.vue:62-65`).

The catalog is parsed from the raw font bytes (`packages/core/src/text/features.ts:15-39` `parseFeatureCatalog`, served via `fontManager.getFeatureCatalog` at `packages/core/src/text/fonts.ts:557-565`, keyed to the selected node's family at `packages/vue/src/controls/typography/actions.ts:58-72`).

**Empirically verified** by running the repo's own parser (`parseFeatureCatalog` from `packages/core/dist/text/features.js`) against the bundled fonts in `cua_designpen/public/`:

| Font | liga | dlig | calt | ordn |
|---|---|---|---|---|
| Inter-Regular.ttf / InterVariable.ttf (default font) | **no** | yes | yes | yes |
| Poppins-Regular.ttf | no | no | no | no |
| Roboto-Regular.ttf | yes | yes | no | no |
| Montserrat-Regular.ttf | yes | yes | no | yes |
| HostGrotesk-Regular.ttf | yes | no | yes | yes |

Inter — the app's `DEFAULT_FONT_FAMILY` — genuinely declares **no `liga` GSUB feature** (Inter implements its ligature-like substitutions via `calt`/`dlig`). So on the default font the filter yields exactly the reported Letterforms section: "Rare ligatures", "Contextual alternates", "Ordinals" — no Standard-ligatures toggle. Meanwhile the app's shaping model treats `liga` as default-ON for every font (`DEFAULT_ON_TAGS = new Set(['kern', 'calt', 'liga'])`, `feature-sections.ts:160-162`) and the shaper (CanvasKit/HarfBuzz) applies standard ligatures by default, so standard ligatures render but can never be disabled from the UI.

Honesty note: for fonts that DO declare `liga` (Roboto, Montserrat, Host Grotesk) the code as written should render the row. If QA observed the row absent on those families too, the top-ranked residual hypothesis is that testing stayed on the default family (Inter); no code path was found that strips `liga` for a liga-declaring font (source, `packages/core/dist`, and the built app bundle `dist/assets/raster-1JfPCedS.js` all contain the `Standard ligatures`/`liga` row).

Secondary observation (narrow right panel / horizontal reach to the Type settings button): the properties panel's default splitter share is 12.5% (`src/app/shell/layout-storage.ts:6` `DEFAULT_EDITOR_LAYOUT = [15, 72.5, 12.5]`) — 160px at 1280px viewport — floored by `min-w-[240px]` on the panel (`src/views/EditorView.vue:295`). At that 240px floor the alignment row that hosts the Type-settings trigger overflows and wraps; the code acknowledges this at `src/components/properties/TypographySection.vue:667-670`: "Wraps at the 240px panel floor (RLCU-2358): both align groups plus the type-settings trigger exceed the row, and the panel clips horizontal overflow."

## Proposed fix

In `packages/core/src/text/feature-sections.ts`, exempt default-ON tags from the declared-tag gate: a feature the shaper enables by default must always be offered so users can turn it off. Concretely, change `declaredRows` (lines 83-88) to keep a row when any of its tags is in `DEFAULT_ON_TAGS` even if `hasFeature` is false, e.g.:

```ts
const offered = (tag: string) => hasFeature(catalog, tag) || featureDefault(tag)
const declaredRows = (rows: FeatureRow[]) =>
  rows
    .map((row) => ({ ...row, tags: row.tags.filter(offered) }))
    .filter((row) => row.tags.length > 0)
```

This surfaces "Standard ligatures" (liga) for every font — including Inter/Poppins — and also hardens "Contextual alternates" (calt) and "Kerning pairs" (kern), the other default-ON toggles, against fonts that don't declare them. `mergeFeatureDeviations`/`resolveFeature` (lines 175-192) already handle liga-off deviations correctly, so no write-side change is needed.

For the secondary panel-width issue: raise the properties-panel default share in `DEFAULT_EDITOR_LAYOUT` (`src/app/shell/layout-storage.ts:6`) so its resolved width at 1280px comfortably exceeds the 240px floor (e.g. `[15, 65, 20]`), or raise `min-w-[240px]` at `src/views/EditorView.vue:295` to a width at which the alignment row (two align groups + type-settings trigger) fits without wrapping.

## Acceptance criteria

- With a text node using Inter (default font) selected, opening Type settings → Details shows a "Letterforms" section whose first row is "Standard ligatures", followed by "Rare ligatures", "Contextual alternates", "Ordinals".
- The "Standard ligatures" toggle reads ON by default (liga is a default-ON tag) and toggling it OFF visibly changes rendered ligature pairs (e.g. "fi", "ffl" in a sample like "office waffle") for a liga-bearing font such as Roboto or Montserrat.
- Toggling Standard ligatures OFF writes a `{ tag: 'liga', enabled: false }` deviation to the node's `fontFeatures`; toggling back ON removes the deviation (deviations-only merge, ADR0016).
- The row appears for every selectable font family (Inter, Roboto, Poppins, Montserrat, Host Grotesk, Roboto Flex), not only fonts declaring `liga` in GSUB.
- Rows for non-default-ON tags (e.g. Ordinals) still hide when the font does not declare them (Roboto shows no Ordinals row).
- Secondary: at a 1280x720 viewport with default (unpersisted) layout, the Type settings trigger button in the Typography section is visible and clickable without horizontal scrolling.

## Regression tests to add

- Unit (`packages/core/src/text/feature-sections.test.ts`):
  - `buildFeatureSections([])` (empty catalog) → Letterforms section exists and contains rows for exactly the default-ON letterform tags: assert a row `{ label: 'Standard ligatures', tags: ['liga'] }` is present.
  - `buildFeatureSections(interCatalog)` where `interCatalog` has `dlig/calt/ordn` but no `liga` → Letterforms rows are `['Standard ligatures', 'Rare ligatures', 'Contextual alternates', 'Ordinals']` in that order.
  - `buildFeatureSections(robotoCatalog)` (has `liga`, no `calt`/`ordn`) → contains 'Standard ligatures' and 'Rare ligatures'; still contains 'Contextual alternates' (default-ON) but NOT 'Ordinals'.
  - `mergeFeatureDeviations(undefined, ['liga'], false)` → `[{ tag: 'liga', enabled: false }]`; `mergeFeatureDeviations(prev, ['liga'], true)` → `[]` (round-trip clears the deviation).
- Integration (Vue component test on `TypeDetailsSections.vue`): mount with an Inter-shaped catalog prop (no `liga` entry) and assert `[data-test-id="feature-section-letterforms"]` renders a `FeatureToggleRow` labeled "Standard ligatures" whose initial value is `true`; emitting its change fires `setFeature(['liga'], false)`.
- E2E (1280x720): select a Roboto text node containing "office waffle", open Type settings → Details, toggle "Standard ligatures" off, screenshot-diff or glyph-count assert the "ffi/ffl" ligatures decompose; assert the node's `fontFeatures` contains `{tag:'liga',enabled:false}` via the state bridge.
- E2E (secondary): fresh profile (no persisted `editor-layout` in localStorage) at 1280x720 — assert the Type settings trigger's bounding box is fully within the viewport and `click()` opens the popover without any horizontal scroll action.
