# DesignPen [MCP tools]: 'analyze spacing' fails QA — 5/5 runs report broken workflow (10025-analyze-spacing-mcp)

Description:
The `analyze_spacing` MCP tool in DesignPen/OpenPencil fails to detect geometric gaps between page-level sibling nodes. With three 100x100 rectangles perfectly aligned at y=0 with exact uniform 50px gaps (x = 0, 150, 300), the tool reported `totalNodes` correctly but returned empty `gaps`, `paddings`, `offGridGaps`, and `offGridPaddings` on every call (default grid=8 twice, grid=50 once). It likely only reports auto-layout gap/padding inside containers, not free-placed siblings. The rest of the workflow (shape/frame creation, viewport_zoom_to_fit, verification) works; the agent had to derive the gap of 50 manually from `get_node` coordinates instead of from `analyze_spacing`.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Using MCP tools only, call create_shape to make a 100x100 rectangle named Col 1 at (0, 0).
3. Call create_shape to make a 100x100 rectangle named Col 2 at (150, 0).
4. Call create_shape to make a 100x100 rectangle named Col 3 at (300, 0).
5. Call analyze_spacing (try default grid=8 and grid=50) and inspect the returned gaps.
6. Create a frame named 'gap-N' where N is the uniform gap it detects.
7. Call viewport_zoom_to_fit and verify with find_nodes and get_node.

Actual Result:

- `analyze_spacing` was called three times (default grid=8 twice, grid=50 once); each time it reported `totalNodes` correctly (3, then 4) but returned empty `gaps`, `paddings`, `offGridGaps`, and `offGridPaddings` — despite the three rectangles being perfectly aligned at y=0 with exact uniform 50px gaps.
- The tool appears not to compute geometric gaps between page-level sibling nodes (likely only auto-layout gap/padding inside containers).
- Workaround required: the gap N=50 was derived from `get_node` coordinate measurements (Col 1 ends at x=100, Col 2 starts at x=150, etc.) and the frame named `gap-50` accordingly; shape creation, frame creation, zoom, and verification all worked.

Expected Result:
`analyze_spacing` should detect the uniform 50px geometric gaps between the aligned page-level sibling rectangles and report them in `gaps`, so the frame name can be derived from the tool's output rather than manual geometry measurement.

Estimate: M (3 points) — scoped feature fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed (agent verdict: not-approve)
- Attempt transcripts:
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_157773cc-23b3-42b6-92e8-e33dcb7fffd6.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_23c30551-3c0e-428b-8f05-a734587b4b72.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_7b23836b-ee79-446f-a7f8-0209ee2db69f.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_8d057398-30e2-447c-980f-a4a3d7cd6701.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_942b2e68-6519-4a34-a4ae-baad2675a3ed.txt`

Agent report (verbatim tail of failing run):

```
All steps are complete. Here's my verification report:

## Results

**Created nodes (verified via `find_nodes` + `get_node`):**
| Node | Type | ID | Position | Size |
|---|---|---|---|---|
| Col 1 | RECTANGLE | 0:3 | (0, 0) | 100×100 ✓ |
| Col 2 | RECTANGLE | 0:4 | (150, 0) | 100×100 ✓ |
| Col 3 | RECTANGLE | 0:5 | (300, 0) | 100×100 ✓ |
| gap-50 | FRAME | 0:6 | (0, 200) | 400×100 ✓ |

**Gap verification (from geometry):** Col 1 ends at x=100, Col 2 starts at x=150 → gap 50; Col 2 ends at x=250, Col 3 starts at x=300 → gap 50. The uniform gap is **50**, hence the frame name `gap-50`.

**Viewport:** `viewport_zoom_to_fit` succeeded, framing bounds (0, 0, 400, 300) centered at (200, 150), covering all four nodes.

**The problem encountered:** `analyze_spacing` did **not** detect the gaps. It was called three times (default grid=8 twice, grid=50 once); each time it reported `totalNodes` correctly (3, then 4) but returned empty `gaps`, `paddings`, `offGridGaps`, and `offGridPaddings` — even though the three rectangles are perfectly aligned at y=0 with exact uniform 50px gaps. The tool appears not to compute geometric gaps between page-level sibling nodes (it likely only reports auto-layout gap/padding inside containers). Since no move/reparent/delete tools were available to restructure the layout into a frame without polluting the document, I derived N=50 from `get_node` coordinate measurements instead of from the `analyze_spacing` output, and named the frame accordingly.

Everything else (shape creation, frame creation, zoom, verification) worked flawlessly, but the task as specified — naming the frame from the gap that `analyze_spacing` *detects* — could not be done literally because the tool detected no gap and I had to work around it with manual geometry measurement.

verdict: not-approve
```
