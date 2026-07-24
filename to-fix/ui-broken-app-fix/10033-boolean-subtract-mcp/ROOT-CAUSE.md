# 10033-boolean-subtract-mcp — enrichment appendix

## Root cause analysis

Shared root cause with pid 10032 (`10032-boolean-intersect-mcp.md`), confirmed. App source: `/Users/mateuszszczech/Desktop/patronus-gyms/cua_designpen` (gym runs release **v0.1.8**).

The MCP tool (`packages/core/src/tools/vector/boolean.ts:16-27`):

```ts
export const booleanSubtract = defineTool({
  name: 'boolean_subtract',
  ...
  description: 'Subtract the second node from the first.',
  params: { ids: { type: 'string[]', description: 'Node IDs (first minus rest)', required: true } },
  execute: (figma, { ids }) => {
    const result = figma.booleanOperation('SUBTRACT', ids)
    return nodeSummary(result)
  }
})
```

calls `_booleanOperation` in `packages/core/src/figma-api/index.ts:393-426`, which computes the new BOOLEAN_OPERATION node's frame as the **union of all operands regardless of the operation**:

```ts
// Boolean node extent is the union of all children (Figma parity), not the first child's box.
const bounds = computeAbsoluteBounds(childNodes, (id) => this.graph.getAbsolutePosition(id))
...
const group = this.graph.createNode('BOOLEAN_OPERATION', parentId, {
  ...
  width: bounds.width,
  height: bounds.height,
  booleanOperation: operation
})
```

For A = 100x100 at (0,0) minus B = 100x100 at (50,50), the union AABB is 150x150 — but `A − B ⊆ A`, so the result's bounds can never exceed A's 100x100 box. The comment even records the deliberate (wrong for SUBTRACT) choice: "not the first child's box".

The operand order is honored by the renderer: children are reparented in `ids` order (`figma-api/index.ts:421-423`), and `makeBooleanOperationPath` (`packages/core/src/canvas/boolean.ts`) folds `result = childPaths[0]` then `result.op(path, PathOp.Difference)` for the rest (`BOOLEAN_PATH_OP: { SUBTRACT: 'Difference', ... }`) — so the *pixels* are the correct L-shape. Only the scene-graph frame (`x/y/width/height`), which MCP `get_node` reports and `viewport_zoom_to_fit` frames, is union-sized. QA confirmed: all 4 failing runs saw 150x150 bounds, independently corroborated by zoom-to-fit framing the union.

The UI path `booleanOperationSelected` (`packages/core/src/editor/structure/boolean.ts:38-49`) has the identical union-bounds line; its z-order sort (lines 23-29: "SUBTRACT carves the upper shapes out of the bottom one") means the base there is the bottom-most child, index 0 after sorting.

## Proposed fix

Same shared fix as 10032: a `booleanResultBounds(operation, childRects)` helper used by both `_booleanOperation` (`packages/core/src/figma-api/index.ts:407`) and `booleanOperationSelected` (`packages/core/src/editor/structure/boolean.ts:38`), with:

- `SUBTRACT` → bounds of the **base** operand only: `childRects[0]` (MCP: `ids[0]`, matching the tool's "first minus rest" contract; UI: the bottom-most child after the existing z-sort).
- `INTERSECT` → AABB intersection; `UNION`/`EXCLUDE` → union (unchanged).

`reparentNode` (`packages/core/src/scene-graph/index.ts:909+`) preserves children's absolute positions, and rendering derives geometry from child transforms rather than the boolean node's frame, so clamping the frame to the base shape changes only reported bounds/selection/zoom framing — not pixels.

Risk/notes:
- Base-operand bounds are a conservative superset of the true `A − rest` bbox (if the subtraction eats a full edge of A, the tight bbox is smaller than A). Exact tight bounds require evaluating the Skia result path (`makeBooleanOperationPath(...).getBounds()`) — renderer-layer, larger change; the base-clamp is what the task verifies (100x100) and is always a valid upper bound within A.
- Verify no callers rely on the boolean frame being the union (e.g. selection outlines, export crop); the frame shrink can expose any such hidden coupling — covered by the regression tests below.

## Acceptance criteria

- Via MCP: rect A 100x100 at (0,0), rect B 100x100 at (50,50), `boolean_subtract` with `[A, B]` → `get_node` on the result reports x=0, y=0, width=100, height=100.
- The node keeps both children (A and B) in that order with `booleanOperation: 'SUBTRACT'`; children's absolute positions are unchanged; the rendered result is still the L-shaped `A − B`.
- `viewport_zoom_to_fit` after the op frames the 100x100 base region, not 150x150.
- Argument order still means "first minus rest": `boolean_subtract([B, A])` reports B's 100x100 frame at (50,50).
- `boolean_union`/`boolean_exclude` bounds are unchanged; `boolean_intersect` matches pid 10032's criteria.
- UI Subtract on the same two rects (B on top) yields the bottom shape's 100x100 bounds; undo restores both rects, original stacking order and positions.

## Regression tests to add

- **Unit (core, figma-api)** — in the shared `boolean-bounds` suite: `booleanOperation('SUBTRACT', [A, B])` with A at (0,0) 100x100 and B at (50,50) 100x100 → node frame `{x:0, y:0, width:100, height:100}`; reversed order `[B, A]` → `{x:50, y:50, width:100, height:100}`; three operands `[A, B, C]` → still A's frame; operands inside a translated parent frame → parent-relative x/y correct.
- **Unit (core, geometry)** — `booleanResultBounds('SUBTRACT', ...)` returns exactly the first rect regardless of the others (including a subtrahend fully containing the base).
- **Unit (core, editor/structure)** — `booleanOperationSelected(..., 'SUBTRACT')` on two overlapping rects where the *selection order* is top-first: assert the bounds come from the bottom-most (z-order) shape, proving the sort→base coupling; assert undo restores original geometry.
- **Integration (MCP tool)** — end-to-end `boolean_subtract` through tool registration: `get_node` JSON shows the 100x100 frame; `viewport_zoom_to_fit` viewport covers ~(0,0,100,100).
- **E2E (gym probe)** — replay task 10033's steps; assert reported bounds 100x100 and a screenshot diff showing the L-shape unchanged.
