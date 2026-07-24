# DesignPen [boolean operations]: 'boolean exclude' fails QA — 5/5 runs report broken workflow (10031-boolean-exclude-mcp)

Description:
The `boolean_exclude` MCP tool in the DesignPen/OpenPencil design app creates a structurally correct `BOOLEAN_OPERATION` node but does not recompute the node's bounding box from its children. Excluding two 100x100 rectangles offset by (50,50) should produce union bounds of 150x150, but the resulting node reports `x:100, y:100, width:100, height:100` — exactly the first rectangle's bounds. Because the bounds are stale, `viewport_zoom_to_fit` frames only a 100x100 region and leaves part of the resulting shape (the second rectangle's non-overlapping region) outside the fitted viewport. All tool calls return success with no errors; the bug is a silent bounds-calculation defect.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Using MCP tools, create a 100x100 rectangle at (100, 100).
3. Create a second 100x100 rectangle at (150, 150), i.e. offset by 50px on both axes so they overlap.
4. Call `boolean_exclude` with both rectangle ids.
5. Call `viewport_zoom_to_fit` on the resulting BOOLEAN_OPERATION node.
6. Inspect the result node with `get_node` and check its reported x/y/width/height against its children's combined extent.

Actual Result:

- The `BOOLEAN_OPERATION` node reports `x:100, y:100, width:100, height:100` even though its children span from relative (0,0) to (150,150); the bounds match only the first rectangle and were not recalculated after the boolean operation.
- `viewport_zoom_to_fit` reports and fits bounds of only 100x100 at (100,100), so part of the resulting shape lies outside the fitted region.
- Structure is otherwise correct: the node contains both rectangles as children with the 50px offset preserved, and all calls execute without errors.

Expected Result:
The boolean exclude result node's bounding box should be recomputed from its children — 150x150 covering absolute (100,100) to (250,250) — and `viewport_zoom_to_fit` should frame the full combined shape.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed (agent verdict: not-approve)
- Attempt transcripts:
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_3d6f38a6-89a1-49ea-8656-b0735b59d93f.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_65076092-633d-4b35-b4f6-210e2727d32c.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_9c68a056-b211-4bf5-8a36-2050b8e554d3.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_ab6ea75b-6f04-4755-b56a-b73537857a1f.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_f1a53cd0-ec96-45d7-b2fe-70934f88614e.txt`

Agent report (verbatim tail of failing run):

```
Verification complete. Here's a summary of what I did and found:

## Actions performed
1. **Created Rect 1** — RECTANGLE, 100x100 at (100, 100) → id `0:3` ✓
2. **Created Rect 2** — RECTANGLE, 100x100 at (150, 150), i.e. offset +50px on both axes → id `0:4` ✓
3. **Called `boolean_exclude`** with `["0:3", "0:4"]` → returned a new node `0:5` named "Boolean exclude" of type `BOOLEAN_OPERATION` ✓
4. **Called `viewport_zoom_to_fit`** on `0:5` ✓

## Verification findings
- `get_node("0:5")` confirms a `BOOLEAN_OPERATION` node containing both rectangles as children: Rect 1 at relative (0,0) and Rect 2 at relative (50,50), both 100x100 — the 50px overlap offset is correctly preserved.
- `find_nodes` confirms exactly one "Boolean exclude" node exists, and both rectangles still exist (as its children, not as top-level nodes).
- The document tree confirms the hierarchy: Document → Page 1 → Boolean exclude → [Rect 1, Rect 2].

**However, I found a geometry discrepancy:** the resulting `BOOLEAN_OPERATION` node reports `x:100, y:100, width:100, height:100`, but its children span from relative (0,0) to (150,150). The bounding box of an exclude of two 100x100 squares offset by (50,50) should be **150x150** (covering absolute 100,100 → 250,250). The node's bounds were apparently not recalculated after the boolean operation (they match only the first rectangle). This also affected `viewport_zoom_to_fit`, which reported and fit bounds of only 100x100 at (100,100), meaning part of the resulting shape (Rect 2's non-overlapping region) lies outside the reported/fitted bounds.

All tool calls executed without errors and the structural result is correct, but the verification revealed a bounds-calculation bug in the boolean exclude result (reported 100x100 instead of the expected 150x150 union bounds), which also caused zoom-to-fit to frame the wrong region.

verdict: not-approve
```
