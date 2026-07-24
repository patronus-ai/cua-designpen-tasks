# 00063-pen-chain-from-vertex-ui — enrichment appendix

## Root cause analysis

App source: `/Users/mateuszszczech/Desktop/patronus-gyms/cua_designpen` (gym runs release **v0.1.8** per `apps/cua_designpen/.release-info`; v0.1.8 contains commit `88eefcf8`, which is the deciding change here).

The pen click on a vertex of the edited network is handled by `handlePenNodeEditDown` in
`packages/vue/src/shared/input/node-edit/index.ts` (entry: `startPenInput` at `packages/vue/src/canvas/pen-input/use.ts:99-111`, which delegates here whenever the pen is active with an open edit session and no live chain). Lines 502-518:

```ts
if (vi !== null) {
  // Figma parity: pen click on a mid-path anchor (exactly two incident
  // segments) removes the point and heals the curve into one segment.
  // Alt-click removes any vertex regardless of degree.
  if (e.altKey || vertexDegree(vi, es.segments) === 2) {
    nodeEditEditor.nodeEditRemoveVertex?.(vi)
    return
  }
  // Endpoints and junction vertices: pen click starts a chain anchored
  // there (branch/extend) ...
  const v = es.vertices[vi]
  nodeEditEditor.penStartChainFromVertex?.(vi)
  if (editor.state.penState) setDrag(createPenDrag(v.x, v.y))
  return
}
```

Two defects combine to produce the observed behavior:

1. **The degree-2 rule steals the branch gesture.** Commit `88eefcf8` ("fix(pen): remove mid-path anchor on pen click instead of extending a chain", 2026-07-23, in v0.1.7+) made `vertexDegree(vi) === 2` route to `nodeEditRemoveVertex` unconditionally. Branching (`penStartChainFromVertex`, defined at `src/app/editor/pen/connect.ts:118-126`) is now reachable only for open endpoints (degree 1) and junctions (degree ≥ 3). In the task's Y-shape scenario, after the first arm is drawn the shared vertex at (300,350) has degree 2 (stem + arm 1), so the second branch click deletes it instead of re-rooting the pen there. This is exactly "works only on open endpoints".

2. **The delete-heal disguises the removal as a corner→smooth conversion.** `nodeEditRemoveVertex` (`src/app/editor/vector-edit/network.ts:152-162`) calls `removeVertex` (`packages/core/src/vector/bezier.ts:275-310`), which for a degree-2 vertex merges the two incident segments via `buildMergedSegmentForRemovedVertex` (`bezier.ts:125-187`). For two **straight** incident segments the neighbor tangents `dirA`/`dirB` are zero, so the scaled-tangent estimate deviates from the corner and the 5%-deviation gate (`bezier.ts:176-179`) falls into `solveMergedTangents` (`bezier.ts:189-228`); with zero direction vectors `det === 0` and the fallback (`bezier.ts:215-227`) synthesizes tangents `c*toRA` / `c*toRB` that force the merged cubic **through the removed corner position**:

```ts
const toRA = { x: vR.x - vA.x, y: vR.y - vA.y }
const toRB = { x: vR.x - vB.x, y: vR.y - vB.y }
...
return {
  tangentStart: { x: c * toRA.x, y: c * toRA.y },
  tangentEnd: { x: c * toRB.x, y: c * toRB.y }
}
```

The result: one curved segment with visible Bézier handles that still passes through (300,350). The QA transcript matches this exactly: "it converted the node to a smooth point, adding bezier control handles and curving the existing first arm" (reproduced with zero-movement clicks — removal fires on mousedown, no drag needed). The anchor is in fact deleted, but the through-point heal makes the click look like a corner/smooth toggle rather than a branch.

**Conflict warning:** pid 00067 expects a plain pen click on the same state (degree-2 anchor, no live chain) to *remove* the anchor. The two task expectations collide on one gesture; any fix must disambiguate (see below).

## Proposed fix

In `handlePenNodeEditDown` (`packages/vue/src/shared/input/node-edit/index.ts:502-518`), disambiguate remove vs. branch on degree-2 anchors by gesture instead of resolving everything on mousedown:

- On mousedown over a degree-2 anchor, do **not** mutate immediately. Arm a pending drag state (e.g. `type: 'pen-anchor-pending'`, carrying `vertexIndex`).
- On mouseup with cursor movement below the click threshold (~3px/zoom, same deadzone already used for vertex drags in `handleNodeEditMove`): perform `nodeEditRemoveVertex(vi)` — plain click removes (Figma/Illustrator parity, keeps 00067's expectation).
- On movement ≥ threshold before mouseup: call `penStartChainFromVertex(vi)` and convert the drag into a normal `createPenDrag` so the outgoing tangent is pulled out — press-and-drag branches a new chain from **any** vertex, including interior/shared (degree-2) ones.
- Keep Alt-click = remove-any-degree as today.

Additionally fix the heal so a removal is visually a removal (shared with 00067 — see `00067-pen-remove-vertex-ui.md`): in `buildMergedSegmentForRemovedVertex`, when both incident segments are straight, return a straight merged segment instead of the through-corner curve.

Risk / note: task 00063's prompt instructs plain *clicks* to branch ("pen-click (300,350) once more, and draw the second arm"). With click=remove + drag=branch, a strictly click-driven agent still cannot branch; either the task prompt must be reworded to press-and-drag, or the alternative resolution (plain click = branch, remove only via Alt-click/context menu) must be chosen — which would in turn break 00067's plain-click-removes expectation. The two tasks cannot both be satisfied by the same plain-click gesture; this must be decided by the task owners. The workaround that already works today (draw the arm from empty canvas and connect back onto the shared vertex — `penSetConnectTarget` path in `packages/vue/src/canvas/pen-input/use.ts:132-138`) should remain intact.

## Acceptance criteria

- With the pen active in a vector edit session and no live chain, press-and-drag starting on an interior/shared (degree-2) vertex starts a new chain anchored at that vertex (no vertex is removed, no handles appear on the existing segments, the existing segments stay straight/unchanged).
- Committing the branched chain (Escape/Enter) merges it into the same vector network, welded to the anchor vertex (no duplicate vertex at the anchor position).
- Branching still works from open endpoints (degree 1) and junction vertices (degree ≥ 3) exactly as before.
- The Y-shape flow of the task is achievable: stem (300,500)→(300,350); branch arm 1 to (240,250); branch arm 2 from the now-degree-2 vertex (300,350) to (360,250); final network has 4 vertices, 3 segments, all straight, vertex (300,350) has degree 3.
- Alt-click on any vertex still removes it.
- Clicking (without drag) an interior anchor behaves per the resolution chosen for 00067 (removal that visibly simplifies) — it must never convert the anchor to a smooth point that curves neighboring segments.
- The connect-back workaround (start a chain on empty canvas, click an existing network vertex to connect) keeps working.

## Regression tests to add

- **Unit (vue, `packages/vue/src/shared/input/node-edit/`)** — `pen-branch-from-interior-vertex.test.ts`:
  - Build an edit session with vertices A(300,500), B(300,350), C(240,250) and straight segments A-B, B-C (B has degree 2). Simulate pen mousedown on B, mousemove beyond the threshold, and assert `editor.state.penState` is live with `anchorVertexIndex === indexOf(B)` and `es.vertices.length` unchanged (nothing removed).
  - Same setup, mousedown+mouseup on B with zero movement: assert the resolution chosen for 00067 (vertex removed) and, critically, that no `penState` was created and no tangents were added to A-B/B-C beyond the heal result.
- **Unit (core, `packages/core/src/editor/shapes/pen-branching.test.ts`)** — extend: `resolvePenActiveIndex`/merge behavior when the anchor vertex has degree 2; `mergePenChainIntoNetwork` with `anchor.vertexIndex` pointing at a degree-2 vertex produces a degree-3 junction with no duplicate vertex.
- **Integration (session, `src/app/editor/pen/`)** — script the full Y-shape: pen-draw stem, Escape, branch arm 1 (drag gesture), Escape, branch arm 2 from the shared vertex, commit; assert the committed node's `vectorNetwork` has exactly 4 vertices / 3 segments, all `tangentStart`/`tangentEnd` equal to `{x:0,y:0}`.
- **E2E (gym probe)** — replay task 00063's steps with press-and-drag branching; assert via MCP `get_node` that the resulting vector's bounds are x:240, y:250, w:120, h:250 and the network has 4 vertices.
