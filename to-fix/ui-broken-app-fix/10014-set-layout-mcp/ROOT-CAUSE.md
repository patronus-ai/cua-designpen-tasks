# pid 10014 — `set_layout` repositions only the first child

## Root cause analysis

The reflow itself is fine — the bug is that `set_layout`'s enable-auto-layout path **pins every child except one as `layoutPositioning: 'ABSOLUTE'`**, and absolute children are skipped by the layout engine, so they stay at (0,0).

Chain of evidence:

1. **`set_layout` enable path** — `packages/core/src/tools/modify/layout.ts:67-81`. When the frame had `layoutMode === 'NONE'` and a `direction` is passed, it calls `layoutModeUpdates(...)` and then:
   ```ts
   for (const childId of absoluteIds) {
     figma.graph.updateNode(childId, { layoutPositioning: 'ABSOLUTE' })
   }
   ```

2. **Where `absoluteIds` comes from** — `layoutModeUpdates` → `autoLayoutFromChildren` (`packages/core/src/editor/layout-mode.ts:176-191` and `231-292`), which is a "Figma parity: enabling auto-layout must not change the frame's visual box" heuristic. It calls `partitionOverlappingChildren(visible, mode)` (layout-mode.ts:255).

3. **The partition heuristic** — `packages/core/src/editor/layout-overlap.ts:22-40`: an item is pinned ABSOLUTE when it 2D-overlaps a flow item AND its main-axis span is contained in that item's span. For children that were all created at (0,0) with equal (or contained) sizes — the normal MCP flow of `create_shape` children before enabling layout — every child overlaps and is span-contained in the first/largest one, so **exactly one child lands in `flow` and all the rest land in `absolute`**.

4. **Reflow runs but skips them** — the automation bridge recomputes layout after every mutating tool: `src/app/automation/bridge/tool-handlers.ts:51-57` (`computeAllLayouts(store.graph, store.state.currentPageId)`). The yoga apply step then explicitly ignores absolute children: `packages/core/src/layout/apply.ts:40` — `if (!child.visible || child.layoutPositioning === 'ABSOLUTE') return`. Result: the single flow child moves to the padding offset (e.g. (12,12)); the pinned children keep their stored (0,0).

The heuristic was designed for freeform frames whose children are already visually arranged (label over rectangle, RLCU-2465/RLCU-2461); for the degenerate stacked-at-origin case it silently defeats the caller's intent.

Two secondary defects confirmed:

- **Response echoes only `{ id, spacing }`** — `packages/core/src/tools/modify/layout.ts:109`: `return { id: args.id, spacing: node.itemSpacing }` — never direction, padding, alignment.
- **`get_node` exposes no padding** — `packages/core/src/figma-api/serialization.ts:101-105` serializes only `layoutMode`, `layoutDirection`, `itemSpacing` when `layoutMode !== 'NONE'`; `paddingTop/Right/Bottom/Left` are never emitted, so the agent cannot even verify what it set.

## Proposed fix

1. **Don't pin fully-stacked children** in `set_layout`. Cheapest targeted fix: in `tools/modify/layout.ts` enable path, skip the ABSOLUTE pinning when the flow set would degenerate to a single child while multiple visible children exist and all sit at the same origin — or better, fix the heuristic at the source: in `partitionOverlappingChildren` (`editor/layout-overlap.ts`), when *every* item would be pairwise coincident/contained (i.e. `flow.length === 1 && absolute.length === items.length - 1` and all items share the same x/y), return all items as `flow` — stacked-at-origin children are not a "label over rectangle" composition, they are simply unpositioned.
2. **Echo the full applied state** from `set_layout` (`layout.ts:109`): return `{ id, layoutMode, itemSpacing, paddingTop, paddingRight, paddingBottom, paddingLeft, primaryAxisAlignItems, counterAxisAlignItems }` read back from the node.
3. **Serialize padding in `get_node`** (`figma-api/serialization.ts:101-105`): inside the `layoutMode !== 'NONE'` branch add `obj.paddingTop/paddingRight/paddingBottom/paddingLeft` (and ideally `primaryAxisAlign`/`counterAxisAlign`).

## Acceptance criteria

- Create a frame with 3 children each 100×100 at (0,0); call `set_layout` with `direction: HORIZONTAL, spacing: 16, padding: 12`; afterwards the children's stored positions are (12,12), (128,12), (244,12) and none has `layoutPositioning: 'ABSOLUTE'`.
- The same call on a frame whose children are already visually arranged (e.g. label centered on a larger rectangle) still pins the contained child ABSOLUTE (existing RLCU-2465 parity preserved — `layout.test.ts` / `layout-overlap.test.ts` suites stay green).
- `set_layout`'s response includes `layoutMode`/direction and all four padding values actually applied, not just `{ id, spacing }`.
- `get_node` on an auto-layout frame reports `paddingTop`, `paddingRight`, `paddingBottom`, `paddingLeft` matching what `set_layout` wrote.

## Regression tests to add

Unit — `packages/core/src/tools/modify/layout.test.ts`:

1. **Stacked children reflow**: frame 400×200, three 100×100 children at (0,0); execute `set_layout {direction:'HORIZONTAL', spacing:16, padding:12}`, then run `computeAllLayouts(graph, pageId)`; assert each child's `(x, y)` equals `(12 + i*(100+16), 12)` and `layoutPositioning === 'AUTO'` for all three.
2. **Parity case still pins**: rectangle 200×100 at (0,0) + text 50×20 at (75,40) (contained span); execute `set_layout {direction:'HORIZONTAL'}`; assert the text child is `ABSOLUTE` and keeps its position.
3. **Response shape**: assert the `set_layout` result object contains keys `layoutMode`, `paddingTop`, `paddingRight`, `paddingBottom`, `paddingLeft` with the passed values (`HORIZONTAL`, 12, 12, 12, 12).

Unit — `packages/core/src/editor/layout-overlap.test.ts`:

4. **Degenerate partition**: `partitionOverlappingChildren` with three identical rects at the same origin returns all three in `flow` and none in `absolute`.

Integration — `tests/integration/mcp`:

5. End-to-end over the bridge: `create_shape` frame + 3 children at (0,0) → `set_layout` HORIZONTAL/16/12 → `get_node` on the frame with `depth: 1`; assert all three children's `x` values are distinct and increasing, and the frame's serialized output includes `paddingLeft: 12`.
