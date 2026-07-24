# 10032-boolean-intersect-mcp — enrichment appendix

## Root cause analysis

App source: `/Users/mateuszszczech/Desktop/patronus-gyms/cua_designpen` (gym runs release **v0.1.8** per `apps/cua_designpen/.release-info`).

The MCP tool is defined in `packages/core/src/tools/vector/boolean.ts:29-40`:

```ts
export const booleanIntersect = defineTool({
  name: 'boolean_intersect',
  ...
  execute: (figma, { ids }) => {
    const result = figma.booleanOperation('INTERSECT', ids)
    return nodeSummary(result)
  }
})
```

`figma.booleanOperation` delegates to `_booleanOperation` in `packages/core/src/figma-api/index.ts:393-426`, which is where the bug lives. The BOOLEAN_OPERATION node's frame is computed as the **union of all children regardless of the operation type** — the `operation` argument is only stored as metadata:

```ts
// Boolean node extent is the union of all children (Figma parity), not the first child's box.
const bounds = computeAbsoluteBounds(childNodes, (id) => this.graph.getAbsolutePosition(id))
...
const group = this.graph.createNode('BOOLEAN_OPERATION', parentId, {
  name: `Boolean ${operation.toLowerCase()}`,
  x: bounds.x - parentAbs.x,
  y: bounds.y - parentAbs.y,
  width: bounds.width,
  height: bounds.height,
  booleanOperation: operation
})
```

`computeAbsoluteBounds` (`packages/core/src/geometry.ts:191-201`) is a plain AABB union accumulator. The comment's "Figma parity" claim is wrong for INTERSECT/SUBTRACT: in Figma the boolean node's bounds are the bounding box of the **result geometry** (50x50 for two 100x100 rects offset by 50,50), not of the operands.

The rendered pixels are actually correct: the canvas layer computes the real geometry via Skia path ops — `BOOLEAN_PATH_OP` maps `INTERSECT → 'Intersect'` and `makeBooleanOperationPath` folds children with `result.op(path, operation)` (`packages/core/src/canvas/boolean.ts`, map at the top of the file, fold in `makeBooleanOperationPath`). But the scene-graph node's `x/y/width/height` — which is what MCP `get_node` reports and what `viewport_zoom_to_fit` frames — is never derived from that result path. Hence every verification path an agent has (node bounds 150x150, zoom-to-fit framing the union extent) reports the union, and all 5 QA runs failed.

The same union-bounds defect exists in the UI toolbar path, `booleanOperationSelected` (`packages/core/src/editor/structure/boolean.ts:38-49`), which also calls `computeAbsoluteBounds(topLevel, ...)` unconditionally — so a UI-driven Intersect has the same wrong bounds. Shared root cause with pid 10033 (boolean_subtract).

## Proposed fix

Make the boolean node's bounds honor the operation type. Add a shared helper (e.g. `booleanResultBounds(operation, childRects: Rect[]): Rect` in `packages/core/src/geometry.ts`) and use it in both creation sites:

- `_booleanOperation` (`packages/core/src/figma-api/index.ts:407`)
- `booleanOperationSelected` (`packages/core/src/editor/structure/boolean.ts:38`)

Semantics:

- `UNION`, `EXCLUDE`: union of child AABBs (current behavior, correct).
- `INTERSECT`: intersection of all child AABBs (`max` of lefts/tops, `min` of rights/bottoms). If empty (no overlap), clamp to a zero-size rect at the intersection anchor or refuse the op with an error — decide and document.
- `SUBTRACT`: the base child's AABB — `childRects[0]` in `_booleanOperation` (MCP `ids[0]` order) and the **bottom-most** child in the z-sorted UI path (`booleanOperationSelected` sorts `topLevel` bottom-to-top first, so index 0 there too).

Child repositioning is already safe: children are moved in with `graph.reparentNode` (`packages/core/src/scene-graph/index.ts:909+`), which converts absolute positions, so shrinking the parent frame keeps children visually fixed; rendering builds the result path from child transforms and does not use the boolean node's width/height, so pixels are unchanged.

Note an accepted limitation/risk: AABB intersection is exact for axis-aligned rectangles (the QA case) but is a conservative superset of the true result bbox for rotated/curved operands. Exact tight bounds would require evaluating the Skia result path (`makeBooleanOperationPath(...).getBounds()`), which lives in the renderer layer — feasible as a post-creation "recompute bounds from render" pass, but a larger change. Ship the AABB fix first; it fixes both 10032 and 10033 as specified.

## Acceptance criteria

- Via MCP: `create_shape` RECTANGLE at (0,0) 100x100, RECTANGLE at (50,50) 100x100, then `boolean_intersect` with both ids → the created BOOLEAN_OPERATION node reports x=50, y=50, width=50, height=50 via `get_node`.
- The node still has both rectangles as children, `booleanOperation: 'INTERSECT'`, and children keep their absolute positions (rendered overlap region unchanged at (50,50)-(100,100)).
- `viewport_zoom_to_fit` after the op frames the 50x50 result region, not a 150x150 union extent.
- `boolean_union` and `boolean_exclude` bounds are unchanged (union of operands).
- UI Intersect (toolbar/menu on two selected overlapping rects) produces the same 50x50 bounds; undo restores both original rects at their original positions and stacking order.
- Non-overlapping operands passed to `boolean_intersect` behave per the documented decision (zero-size node or explicit tool error) — never a union-sized node.

## Regression tests to add

- **Unit (core, figma-api)** — `packages/core/src/figma-api/boolean-bounds.test.ts` (or extend the existing figma-api suite): create two 100x100 rect nodes at (0,0) and (50,50) in a test graph; call `figma.booleanOperation('INTERSECT', [a, b])`; assert node `{x:50, y:50, width:50, height:50}` and both children's `getAbsolutePosition` unchanged. Companion cases: `UNION` → 150x150 at (0,0); nested-parent case (rects inside a frame at (10,10)) → node x/y are parent-relative (40,40).
- **Unit (core, geometry)** — `booleanResultBounds`: intersection of disjoint rects (documented empty behavior), intersection of 3+ rects, single-axis overlap.
- **Unit (core, editor/structure)** — `booleanOperationSelected` with operation `'INTERSECT'` on two overlapping rects: boolean node bounds are the overlap; undo restores original indices/positions (existing undo assertions extended with bounds checks).
- **Integration (MCP tool)** — through the tool registration layer: call `boolean_intersect` end-to-end and assert the `get_node` JSON for the new node contains the 50x50 frame; then `viewport_zoom_to_fit` and assert the viewport rect covers ~(50,50,50,50).
- **E2E (gym probe)** — replay task 10032's exact steps and assert the reported bounds are 50x50.
