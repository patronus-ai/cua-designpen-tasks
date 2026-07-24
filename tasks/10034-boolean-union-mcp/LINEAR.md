# DesignPen [boolean operations]: 'boolean union' fails QA — 5/5 runs report broken workflow (10034-boolean-union-mcp)

Description:
The `boolean_union` MCP tool in the DesignPen/OpenPencil design app produces a structurally correct `BOOLEAN_OPERATION` node but keeps the first rectangle's dimensions instead of recomputing its extent to encompass all children. Unioning two 100x100 rectangles offset by (50,50) yields a node reporting `width: 100, height: 100` at (100,100), where the correct union bounding box is 150x150 covering (100,100) to (250,250). `viewport_zoom_to_fit` inherits the incorrect bounds and frames only part of the combined shape. Every call returns success, so the defect is silent — it is a bounds-calculation bug in the boolean union (or bounds reporting) implementation.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Using MCP tools, create a 100x100 rectangle at (100, 100).
3. Create a second 100x100 rectangle at (150, 150) — offset by 50px on both axes so they overlap.
4. Call `boolean_union` with both rectangle ids.
5. Call `viewport_zoom_to_fit` on the resulting BOOLEAN_OPERATION node.
6. Inspect the result node with `get_node` / `find_nodes` and compare its reported width/height against the children's combined extent.

Actual Result:

- The union node reports `width: 100, height: 100` at (100, 100), although its children span from local (0,0) to (150,150) — the node kept the first rectangle's dimensions instead of recomputing its extent.
- `viewport_zoom_to_fit` confirmed the same incorrect bounds (100x100, center at 150,150), so zoom-to-fit frames only part of the combined shape.
- Structure is correct: `0:5` is a `BOOLEAN_OPERATION` node containing both rectangles as children with the correct relative offset, and all tool calls succeed without errors.

Expected Result:
The boolean union node's bounding box should be recomputed to encompass all children — 150x150 covering canvas (100,100) to (250,250) — and `viewport_zoom_to_fit` should frame the entire combined shape.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed (agent verdict: not-approve)
- Attempt transcripts:
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_3242fb18-3641-4913-8da3-34bb1847961d.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_32b5b058-2df9-4d9c-87e8-22a8e6c28930.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_6395491f-0d4f-4966-87e8-bd98bf1f21df.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_a2280c95-5c79-4cd8-98f7-d699a0de9924.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_db4599a2-ea43-40e3-84fe-2dbbe2f7c851.txt`

Agent report (verbatim tail of failing run):

```
All steps executed, but verification revealed a problem. Here's my report:

## What I did
1. **Created Rect 1** (`0:3`): 100×100 at (100, 100) ✓
2. **Created Rect 2** (`0:4`): 100×100 at (150, 150) — offset by 50px on both axes ✓
3. **Called `boolean_union`** with `["0:3", "0:4"]` → produced node `0:5` of type `BOOLEAN_OPERATION` ✓
4. **Called `viewport_zoom_to_fit`** on `0:5` ✓
5. **Verified** with `get_node` and `find_nodes`.

## What verification found
- **Structure is correct:** `0:5` is a `BOOLEAN_OPERATION` node containing both rectangles as children, with the correct relative offset (Rect 1 at local (0,0), Rect 2 at local (50,50), both 100×100). `find_nodes` confirms all 3 nodes exist in the document.
- **Bounds are wrong:** The union node reports `width: 100, height: 100` at (100, 100). Since its children span from local (0,0) to (150,150), the union's bounding box should be **150×150** (covering canvas (100,100)→(250,250)), not 100×100. The `viewport_zoom_to_fit` response confirmed the same incorrect bounds (100×100, center at 150,150) — it appears the boolean operation node kept the first rectangle's dimensions instead of recomputing its extent to encompass both children.

So while every tool call succeeded without errors and the node hierarchy is right, the resulting union node's geometry is inconsistent with its contents — the bounding box is 100×100 where 150×150 is expected, which also made zoom-to-fit frame only part of the combined shape. This looks like a bug in the boolean union (or bounds reporting) implementation.

verdict: not-approve
```
