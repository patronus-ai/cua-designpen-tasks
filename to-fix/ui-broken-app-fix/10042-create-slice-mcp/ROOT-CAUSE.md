# pid 10042 — `create_slice` returns a FRAME instead of a SLICE

## Root cause analysis

`create_slice` literally creates a frame. `packages/core/src/tools/create/basic.ts:77-103`:

```ts
export const createSlice = defineTool({
  name: 'create_slice',
  mutates: true,
  description: 'Create a slice (export region) on the canvas.',
  ...
  execute: (figma, args) => {
    ...
    const node = figma.createFrame()        // <-- basic.ts:94
    if (resolved.parent) resolved.parent.appendChild(node)
    node.x = args.x
    node.y = args.y
    node.resize(args.width, args.height)
    node.name = args.name ?? 'Slice'
    node.fills = []
    return nodeSummary(node)
  }
})
```

`figma.createFrame()` (`packages/core/src/figma-api/index.ts:183-185`) delegates to `this.graph.createNode('FRAME', ...)`, so the resulting node's `type` is `FRAME` — only the name defaults to "Slice" and fills are emptied to fake transparency.

The defect is structural, not a one-character typo: **the scene graph has no SLICE node type at all.** The `NodeType` union in `packages/core/src/scene-graph/types.ts:211-229` is:

```
'CANVAS' | 'FRAME' | 'RECTANGLE' | 'ROUNDED_RECTANGLE' | 'ELLIPSE' | 'TEXT' | 'LINE'
| 'STAR' | 'POLYGON' | 'VECTOR' | 'BOOLEAN_OPERATION' | 'GROUP' | 'SECTION'
| 'COMPONENT' | 'COMPONENT_SET' | 'INSTANCE' | 'CONNECTOR' | 'SHAPE_WITH_TEXT'
```

— no `SLICE`. There is likewise no `figma.createSlice()` factory (only `createFrame/createRectangle/.../createSection`, `figma-api/index.ts:183-220`). So the tool cannot currently produce a `type: 'SLICE'` node; the FRAME substitution was the implementer's stopgap.

Consequences: `find_nodes`/`query_nodes` type filters can't isolate slices, `get_node` reports `type: FRAME`, and any consumer keying export regions off `type === 'SLICE'` (Figma-plugin parity) silently misses them.

## Proposed fix

Add first-class SLICE support:

1. `packages/core/src/scene-graph/types.ts:211` — add `'SLICE'` to the `NodeType` union.
2. `packages/core/src/scene-graph/node-defaults.ts` — defaults for SLICE (no fills/strokes, not a container; behaves like an export region: `clipsContent: false`, ignores auto-layout).
3. `packages/core/src/figma-api/index.ts` — add `createSlice(): FigmaSliceNode { return this._createNode('SLICE') }` next to `createSection()` (index.ts:219).
4. `packages/core/src/tools/create/basic.ts:94` — replace `figma.createFrame()` with `figma.createSlice()`; keep name default `'Slice'`; drop the `node.fills = []` hack if SLICE defaults already have no fills.
5. Audit renderers/exporters that switch on node type (canvas draw, export pipeline, kiwi `.fig` serialize/import — note `kiwi/fig/node-change/slice-raw-fields.ts` already exists for slice fields on import, suggesting import maps slices to something else today) so a SLICE draws as an outline-only export region and round-trips through save/open.

Minimal fallback if full SLICE modeling is out of scope: make `create_slice` return an explicit error ("slices not supported") rather than silently fabricating a FRAME — a wrong-type success is worse than an honest failure for automation clients.

## Acceptance criteria

- `create_slice {x:10, y:20, width:300, height:200, name:"Hero export"}` returns `type: "SLICE"` in its result summary.
- `get_node` on the returned id reports `type: "SLICE"`, `x: 10`, `y: 20`, `width: 300`, `height: 200`, `name: "Hero export"`.
- `find_nodes {type:"SLICE"}` (enum extended) returns the created node; `find_nodes {type:"FRAME"}` does not.
- Name defaults to `"Slice"` when omitted (existing behavior preserved).
- A document containing a SLICE saves (`save_file`) and reopens (`open_file`) without error, with the node's type intact.
- The slice renders as a non-filled region (no visible solid fill) on the canvas.

## Regression tests to add

Unit — `packages/core/src/tools/create/basic.test.ts` (file exists):

1. **Type assertion**: execute `createSlice.execute(figma, {x:0, y:0, width:100, height:50})`; assert `result.type === 'SLICE'` and `graph.getNode(result.id).type === 'SLICE'`.
2. **Geometry + default name**: assert `x/y/width/height` match args and `name === 'Slice'` when omitted, custom name when provided.
3. **Parenting**: with `parent_id` of a frame, assert the slice is appended under that parent and coordinates are parent-relative (same contract as `create_shape`).

Unit — scene graph:

4. `graph.createNode('SLICE', pageId)` produces a node with slice defaults (no fills, correct type) — placed near `node-defaults.test.ts`.

Integration — `tests/integration/mcp`:

5. Over the MCP bridge: `create_slice` → `get_node` → assert `type === 'SLICE'`; then `find_nodes {type:'SLICE'}` returns exactly that node.
6. Round-trip: `create_slice` → `save_file` → `open_file` → `get_node`; assert type survives serialization.
