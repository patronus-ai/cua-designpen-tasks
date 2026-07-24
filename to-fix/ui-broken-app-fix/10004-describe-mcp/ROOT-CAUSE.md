# pid 10004 — `describe` rejects document root "0:0"

## Root cause analysis

The `describe` tool bypasses the FigmaAPI node-resolution layer that implements the `"0:0"` document-root alias; it reads the raw scene graph directly, where no node with id `0:0` exists.

**The alias lives only in `FigmaAPI.getNodeById`** — `packages/core/src/figma-api/index.ts:166-174`:

```ts
getNodeById(id: string): FigmaNodeProxy | null {
  const node = this.graph.getNode(id)
  if (node) return this.wrapNode(id)
  // Figma addresses the document root as "0:0", but local ids are
  // session-global, so a fresh document's root gets an unpredictable id.
  // Keep the conventional handle working (real "0:0" nodes take priority).
  if (id === '0:0') return this.wrapNode(this.graph.rootId)
  return null
}
```

Tools that resolve nodes through `figma.getNodeById` (e.g. `get_node` at `packages/core/src/tools/read/nodes.ts:91`, `set_layout` at `packages/core/src/tools/modify/layout.ts:57`) therefore accept `0:0`. `viewport_zoom_to_fit`'s description (`packages/core/src/tools/vector/viewport.ts:32`) documents `"0:0"` as the document root, setting the expectation.

**`describe` skips this layer.** `packages/core/src/tools/describe/index.ts:15-30` passes the raw id into helpers that call `figma.graph.getNode(nodeId)` directly:

- `describeOneNode` — `packages/core/src/tools/describe/tree.ts:49-50`:
  ```ts
  const raw = figma.graph.getNode(nodeId)
  if (!raw) return { id: nodeId, error: `Node "${nodeId}" not found` }
  ```
- `autoDepth` — `packages/core/src/tools/describe/tree.ts:88-89` also calls `graph.getNode(nodeId)` (returns depth for size 0 rather than erroring, but computes on nothing).

Since a fresh document's root gets a session-global unpredictable id (per the comment above), `graph.getNode('0:0')` returns `undefined` and describe answers `Node "0:0" not found`.

Two aggravating discoverability gaps confirmed in source:

1. `describe` with no id errors instead of defaulting: `packages/core/src/tools/describe/index.ts:27` — `if (!args.id) return { error: 'Provide id (string) or ids (string[])' }`.
2. `find_nodes` can never surface a page/document node to describe: it searches only within the current page (`page.findAll`, `packages/core/src/tools/read/nodes.ts:122-127`) and its `type` enum (`nodes.ts:105-119`) contains no PAGE/CANVAS/DOCUMENT entry. So there is no tool-side way to discover the real root id, making the broken `0:0` alias the only documented handle.

## Proposed fix

In `packages/core/src/tools/describe/index.ts`, resolve ids through the API layer before touching the graph. Minimal change — add a resolver that canonicalizes each incoming id:

```ts
const resolveId = (id: string) => figma.getNodeById(id)?.id ?? id
```

and use `resolveId(nodeId)` / `resolveId(args.id)` before calling `autoDepth` and `describeOneNode` (index.ts:21-22 and 28-29). `getNodeById` already returns the real root proxy for `"0:0"`, so `?.id` yields the canonical root id; unknown ids fall through unchanged and keep the existing `Node "<id>" not found` error from `tree.ts:50`.

Complementary (recommended):
- `describe` with no `id`/`ids` should default to the current page (`figma.currentPage.id`) instead of erroring (index.ts:27).
- Document the `0:0` alias in the `describe` tool description, mirroring `viewport_zoom_to_fit`.

## Acceptance criteria

- `describe` with `id: "0:0"` returns a description of the document root (id equals `figma.graph.rootId`, includes `children` covering the pages), on a fresh document whose root id is not literally `0:0`.
- `describe` with `ids: ["0:0", <valid frame id>]` succeeds for both entries.
- If a real node with id `0:0` exists (imported file), `describe` returns that node, not the alias target (parity with `getNodeById` priority).
- `describe` with a genuinely unknown id still returns `{ id, error: 'Node "<id>" not found' }`.
- Auto-depth for `0:0` is computed from the real root's subtree size (not from an empty subtree).
- (If defaulting is implemented) `describe` with no arguments describes the current page instead of erroring.

## Regression tests to add

Unit (`tests/unit` or alongside `packages/core/src/tools/describe/`):

1. **Alias resolution**: build a graph whose root id is e.g. `17:0`; execute `describe.execute(figma, { id: '0:0' })`; assert `result.id === figma.graph.rootId` and no `error` key.
2. **Alias in batch**: `describe.execute(figma, { ids: ['0:0'] })`; assert `result.nodes[0].id === figma.graph.rootId`.
3. **Real 0:0 wins**: create a graph containing an actual node with id `0:0`; assert describe returns that node's name/type, not the root's.
4. **Unknown id**: `describe.execute(figma, { id: '999:999' })` still yields `error: 'Node "999:999" not found'`.
5. **autoDepth parity**: assert `autoDepth(graph, '0:0')` (post-fix, via resolved id) equals `autoDepth(graph, graph.rootId)`.

Integration (`tests/integration/mcp`): over the MCP bridge, call `describe` with `id: "0:0"` on a freshly created document (`new_document`) and assert the response contains `children` and no `not found` error — same session in which `viewport_zoom_to_fit` with `ids: ["0:0"]` succeeds.
