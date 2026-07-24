# 20008 — H = 1e99 accepted in Design panel; "Zoom to fit" freezes the app

All paths below are in the app source at `/Users/mateuszszczech/Desktop/patronus-gyms/cua_designpen` (working tree == deployed release `cua_designpen-0.1.8` for every cited file; verified by diff).

## Root cause analysis

Two cooperating defects: (a) the W/H fields have **no upper bound and no sanity cap anywhere in the write path**, and (b) after zoom-to-fit on the resulting astronomical bounds, the **ruler tick loop becomes a literal infinite loop** because its floating-point increment is smaller than the ULP of the loop variable.

### (a) Dimension input accepts 1e99

- Panel field: `src/components/properties/LayoutSection/SizeControls.vue:570-580` — the H `ScrubInput` passes `:min="0"` and **no `:max`** (W field identically at lines 481-490; the multi-select variant in `src/components/properties/PositionSection.vue:266-273` passes `:min="1"`, also no max).
- Input primitive: `packages/vue/src/primitives/ScrubInput/ScrubInputRoot.vue:17-18` defaults `min = -Infinity, max = Infinity`; `commitEdit` (line 133) clamps only to that range:
  ```ts
  const clamped = Math.min(max, Math.max(min, val))
  ```
  `1e99` is finite, so it passes untouched.
- Write path: `commitSizeProp` → `ctx.commitProp('height', …)` → `createNodePropScrubActions` (`packages/vue/src/controls/node-props/helpers.ts:195-210`) → `store.updateSizePreview` / `store.commitSizeUpdate` (`packages/core/src/editor/undo.ts:269` and `:351`). Neither function — nor `graph.updateNode` below them — applies any finite/positive/maximum check. Grep for a document-level max dimension constant finds none (`MAX_TEXTURE_SIZE` at `packages/core/src/canvas/renderer.ts:549` is GL-query only). The node's height is stored as `1e99`.

### (b) "Zoom to fit" hangs the main thread

`zoomToFit` (`packages/core/src/editor/viewport.ts:130-137`) computes page bounds (height ≈ 1e99) and calls `zoomToBounds` (viewport.ts:97-128):

```ts
const zoom = sanitizeZoom(Math.min(availW / (maxX - minX), availH / (maxY - minY)), safeCurrentZoom())
ctx.state.zoom = zoom
ctx.state.panY = rulerInset + padding + availH / 2 - ((minY + maxY) / 2) * zoom   // line 125
```

- `availH / 1e99 ≈ 6e-97` → `sanitizeZoom` (viewport.ts:13-16) clamps it **up** to `ZOOM_MIN = 0.02` (viewport.ts:6). Zoom is fine.
- But `panY` is unclamped: `-(5e98)·0.02 ≈ -1e97`. Finite, so the `Number.isFinite` guard at viewport.ts:104 passes, and `requestRepaint()` fires (line 126).

The repaint draws rulers — on by default: `showRulers: true` in `src/app/editor/session/types.ts:10`, drawn at `packages/core/src/canvas/renderer/pipeline.ts:293`. In `drawVerticalRulerTicks` (`packages/core/src/canvas/rulers.ts:92-131`):

```ts
const worldTop = -r.panY / r.zoom          // = 1e97 / 0.02 = 5e98
const worldBottom = (vh - r.panY) / r.zoom // ≈ 5e98 + 36000 → rounds to the same 5e98 double
const startY = Math.floor(worldTop / step) * step
for (let wy = startY; wy <= worldBottom; wy += minorStep) {   // line 110 — INFINITE LOOP
```

`rulerStep` (rulers.ts:262-272) yields `step = RULER_TARGET_PIXEL_SPACING / zoom = 100 / 0.02 = 5000` → `minorStep = 1000` (rulers.ts:101). The ULP of a double near `5e98` is ≈ `6.4e82`, so `wy += 1000` **does not change `wy`**; `wy <= worldBottom` stays true forever and the main thread never returns from the draw. This exactly matches "blocks the main thread indefinitely, unrecoverable, container dies" — it is not a slow render, it is a non-terminating `for` loop. `drawHorizontalRulerTicks` (rulers.ts:73) has the same hazard for huge widths/panX. (Secondary same-class hazards, reachable with other setups: `packages/core/src/canvas/layout-grids.ts:129-143` loops `for (x/y = offset; < node.width/height; += sectionSize)` — with height 1e99 this is ~1e96 iterations even without the ULP issue; `packages/core/src/canvas/shadows.ts:73-74` loops over `node.width/height` for noise effects but is bounded by `MAX_RAW_NOISE_CELLS`.)

Note the app doesn't freeze at the moment H is typed — a 1e99-px rect draw is clipped by Skia — it freezes on the first repaint whose viewport world-range origin is astronomical, which zoom-to-fit's pan computation guarantees.

## Proposed fix

1. **Clamp dimensions at the editor boundary** (single choke point, protects panel, canvas drag, and MCP tools alike): in `updateSizePreview` and `commitSizeUpdate` (`packages/core/src/editor/undo.ts:269, 351`) — or better, in the underlying `graph.updateNode` size handling — sanitize `width`/`height` to `Number.isFinite(v) ? clamp(v, MIN_NODE_SIZE, MAX_NODE_SIZE) : current`, with `MAX_NODE_SIZE` a new constant (Figma uses ~6e6; anything ≤ 2^24 keeps float math exact at pixel scale). Also pass `:max="MAX_NODE_SIZE"` on the W/H `ScrubInput`s in `SizeControls.vue` and `PositionSection.vue` so the UI clamps visibly.
2. **Make the ruler/grid loops structurally hang-proof** (defense against any future huge-coordinate state, e.g. corrupt files): in `drawHorizontalRulerTicks`/`drawVerticalRulerTicks` (`packages/core/src/canvas/rulers.ts:73, 110`), iterate over an integer tick index instead of accumulating a float — `const first = Math.floor(worldTop/minorStep); const count = Math.ceil((worldBottom - worldTop)/minorStep) + 1; for (let i = 0; i <= count; i++) { const wy = (first + i) * minorStep; … }` — and bail out (skip ticks) when `count` is not finite or exceeds a hard cap (e.g. 10000). Apply the same index-based pattern to `layout-grids.ts:129-143`.
3. **Clamp the viewport target**: in `zoomToBounds` (`packages/core/src/editor/viewport.ts:123-125`), after computing zoom/pan, reject or clamp non-finite / `|pan| > MAX_SAFE_PAN` results (mirroring what `sanitizeZoom` already does for zoom) so a degenerate scene can never park the camera at 1e97.

## Acceptance criteria

- Typing `1e99` (and `Infinity`, `NaN`, `-5`) into the frame H field in the Design panel results in a clamped/rejected value — the node's stored height is finite and ≤ MAX_NODE_SIZE — with no freeze.
- With a node whose height was force-set to 1e99 (e.g. via a pre-fix document or direct graph write), invoking "Zoom to fit" completes within one frame: the app remains responsive, zoom ∈ [0.02, 256], pan finite and within the safe cap.
- Ruler rendering with any `panX/panY/zoom` combination terminates: a draw with `panY = -1e97, zoom = 0.02` returns (unit-testable by calling the tick functions with a mock canvas and asserting a bounded draw-call count).
- Layout-grid rendering on a frame with height 1e9 and sectionSize 10 draws at most the capped number of lines and returns.
- Normal editing is unaffected: setting H=500 commits exactly 500; zoom-to-fit on a normal page frames it with the 25px padding as before.

## Regression tests to add

- **Unit (core editor):** `commitSizeUpdate(id, …)` after `updateSizePreview(id, { height: 1e99 })` → assert `graph.getNode(id).height === MAX_NODE_SIZE`; same for `Infinity`, `NaN` (value unchanged), and `-10` (clamped to min).
- **Unit (viewport):** `zoomToBounds(0, 0, 200, 1e99)` → assert `state.zoom === 0.02` (ZOOM_MIN) and `Number.isFinite(state.panY) && Math.abs(state.panY) <= MAX_SAFE_PAN`; assert the function returns (wrap in a timeout-guarded test).
- **Unit (rulers, mock canvas):** call `drawVerticalRulerTicks` with `panY = -1e97, zoom = 0.02, viewportHeight = 720` and a mock `canvas.drawLine` counter → assert it returns and issues ≤ 10000 draw calls. Repeat for the horizontal variant with `panX = -1e97`. This is the direct regression for the ULP infinite loop.
- **Unit (layout-grids, mock canvas):** grid with `sectionSize = 10` on a node with `height = 1e9` → returns, bounded draw count.
- **E2E (browser/gym):** select the seed frame, type `1e99` into the H field (`data-test-id="layout-height-input"`), press Enter, invoke Zoom to fit (Shift+1 / zoom dropdown), then within 5s assert the page still responds to a trivial `evaluate_script` (`1+1`) — the pre-fix build never returns.
