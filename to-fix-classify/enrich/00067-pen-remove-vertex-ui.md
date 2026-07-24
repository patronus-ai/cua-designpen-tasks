# 00067-pen-remove-vertex-ui — enrichment appendix

## Root cause analysis

App source: `/Users/mateuszszczech/Desktop/patronus-gyms/cua_designpen` (gym runs release **v0.1.8** per `apps/cua_designpen/.release-info`).

Contrary to the QA classification ("no delete-anchor mechanism exists"), v0.1.8 **does** route a plain pen click on a mid-path (degree-2) anchor to removal — `handlePenNodeEditDown`, `packages/vue/src/shared/input/node-edit/index.ts:502-509`:

```ts
if (vi !== null) {
  // Figma parity: pen click on a mid-path anchor (exactly two incident
  // segments) removes the point and heals the curve into one segment.
  // Alt-click removes any vertex regardless of degree.
  if (e.altKey || vertexDegree(vi, es.segments) === 2) {
    nodeEditEditor.nodeEditRemoveVertex?.(vi)
    return
  }
```

(this was added in commit `88eefcf8`, included in v0.1.7+; 2 of 5 QA runs did pass). The actual defect is downstream, in the **delete-heal**: the removal happens, but the healed geometry is visually indistinguishable from a corner→smooth toggle, so the path never "simplifies".

`nodeEditRemoveVertex` (`src/app/editor/vector-edit/network.ts:152-162`) calls `removeVertex` (`packages/core/src/vector/bezier.ts:275-310`). For a degree-2 vertex it merges the two incident segments via `buildMergedSegmentForRemovedVertex` (`bezier.ts:125-187`). For a zigzag corner both incident segments are straight, so the neighbor-tangent directions `dirA`/`dirB` are `{0,0}`; the scaled-tangent estimate then deviates from the corner by more than the 5% gate (`bezier.ts:176-179`):

```ts
const tangents =
  scaledDev < totalLen * 0.05
    ? { tangentStart: scaledTS, tangentEnd: scaledTE }
    : solveMergedTangents(vA, vR, vB, dirA, dirB, mt, t)
```

and `solveMergedTangents` (`bezier.ts:189-228`) — with zero direction vectors its determinant is 0 — hits the fallback (`bezier.ts:215-227`) that fabricates tangents pointing at the removed corner and scales them so the merged cubic passes exactly **through** the removed vertex position `vR`:

```ts
const toRA = { x: vR.x - vA.x, y: vR.y - vA.y }
const toRB = { x: vR.x - vB.x, y: vR.y - vB.y }
...
return {
  tangentStart: { x: c * toRA.x, y: c * toRA.y },
  tangentEnd: { x: c * toRB.x, y: c * toRB.y }
}
```

Net effect on the task's zigzag: clicking a middle anchor replaces two straight segments with **one curved segment (with visible Bézier handles) that still passes through the old corner** — the corner merely rounds. The QA transcript describes precisely this: "converts the anchor into a curve/smooth node (bezier handles appear, the corner rounds)"; the agent even concluded the point was not deleted because the curve still passes through it. Shape-preserving heal is correct when the removed point sits on a genuinely smooth curve (that is what `delete-heal.test.ts` covers — split a cubic, remove the split point, curve preserved), but for a *corner between straight segments* Figma/Illustrator simplify to a straight segment; forcing the curve through the corner defeats the purpose of removal.

Secondary findings confirming the "no alternative mechanism" part of the report: the vector-edit context menu has no "Remove point" item, and Delete/Backspace deletes the whole vector node (verified in the failing transcript).

## Proposed fix

Fix the heal in `buildMergedSegmentForRemovedVertex` / `solveMergedTangents` (`packages/core/src/vector/bezier.ts`):

- If **both** incident segments are straight (all four tangent vectors of `segA`/`segB` are zero), return a straight merged segment: `tangentStart = tangentEnd = {x:0, y:0}`. This is the exact Figma/Illustrator "delete anchor point" behavior and makes the path visibly simplify.
- More generally, remove the through-`vR` fallback for the degenerate case: when `solveMergedTangents`' determinant is ~0 because `dirA`/`dirB` are zero or parallel, fall back to the scaled neighbor tangents (`scaledTS`/`scaledTE`; zero for straight neighbors) instead of fabricating `c*toRA`/`c*toRB` tangents. Keep the through-point solve only when both direction vectors are non-zero and independent (the genuinely-smooth-curve case, which the existing `delete-heal.test.ts` asserts).

No change is needed in `handlePenNodeEditDown` for this pid — plain click on a degree-2 anchor already removes (keep it; note the gesture conflict with pid 00063, which wants the same click to branch — see `00063-pen-chain-from-vertex-ui.md` for the drag-disambiguation proposal).

Optional hardening (addresses the "no alternative mechanism" complaint): add a "Remove point" item to the vector-edit context menu and make Delete/Backspace remove the selected vertices (via `removeVertex`/`healOrBreakVertex`) instead of deleting the whole node when `nodeEditState` has a non-empty `selectedVertexIndices`.

Risk: changing the degenerate-heal output alters geometry produced by any flow that removes a corner vertex (pen click, Alt-click, any future Delete-key path). The existing smooth-curve heal test (`packages/core/src/vector/delete-heal.test.ts`, "heals a degree-2 mid-point... preserving the curve") uses non-zero tangent directions and is unaffected.

## Acceptance criteria

- Draw the 5-point zigzag (100,300), (160,200), (220,300), (280,200), (340,300); commit; with pen still active in edit mode, click a middle anchor (e.g. (220,300)): the vertex count drops from 5 to 4 and the two incident straight segments are replaced by **one straight segment** between the neighbors (tangents zero) — no Bézier handles appear, the path no longer passes through the removed point.
- Removing a degree-2 point that lies on a genuinely smooth curve (non-zero incident tangents) still preserves the curve shape within the existing tolerance (current `delete-heal.test.ts` behavior unchanged).
- Alt-click removal of any-degree vertices produces the same simplification for straight corners.
- Undo restores the removed vertex and both original segments as one history step.
- The whole-shape Delete behavior is unchanged unless the optional selected-vertex Delete is implemented, in which case Delete with selected vertices removes only those vertices.

## Regression tests to add

- **Unit (core, `packages/core/src/vector/delete-heal.test.ts`)** — add:
  - "removing a straight-corner vertex yields a straight segment": network A(0,0)-B(100,100)-C(200,0), both segments with zero tangents; `removeVertex(net, indexOf(B))` → 2 vertices, 1 segment, `tangentStart` and `tangentEnd` both `{x:0,y:0}` (assert exact zeros, not just small deviation).
  - "straight-corner heal does not pass through the removed corner": sample the merged segment at t=0..1 and assert max distance from B is large (e.g. > 50), i.e. the curve is the chord, not a bulge through B.
  - Degenerate-parallel case: collinear A-B-C straight segments → merged straight segment (already shape-identical; assert zero tangents).
- **Unit (vue, `packages/vue/src/shared/input/node-edit/pen-remove-vertex.test.ts`)** — extend the existing suite: after simulating the pen click on a zigzag middle anchor, assert the resulting session network's merged segment has zero tangents (path simplified), not merely that the vertex count decreased.
- **E2E (gym probe)** — replay task 00067: draw + commit the zigzag, pen-click the middle anchor at (220,300); via MCP `get_node` assert the vector's network has 4 vertices and 3 segments with all-zero tangents, and via screenshot that no curve bulge remains at (220,300).
