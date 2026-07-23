# DesignPen [MCP tools]: 'batch update' fails QA — 5/5 runs report broken workflow (10001-batch-update-mcp)

Description:
The DesignPen/OpenPencil `batch_update` MCP tool silently drops the `width` property. When a single operations JSON setting `{"width":150,"opacity":0.5}` is applied to two rectangles, the tool returns `"updated": 2` but the per-node results list only `["opacity"]` as applied — opacity changes land, width does not, and no error is raised. The tool's supported props (spacing, padding, sizing, name, visible, corner_radius, etc.) do not include `width`, and no other MCP tool in the toolset can resize an existing node, so the requested end state (both rectangles at width 150) is unachievable.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Using MCP tools only, call create_shape to make a 100x100 rectangle named Card A at (0,0).
3. Call create_shape to make a 100x100 rectangle named Card B at (150,0).
4. Call batch_update with a single operations JSON that sets width=150 and opacity=0.5 on both rectangles in one call.
5. Call viewport_zoom_to_fit.
6. Verify with get_node on both rectangles and find_nodes.

Actual Result:

- `batch_update` returns `"updated": 2`, but the per-node results list only `["opacity"]` as the applied property — `width` is silently ignored for both nodes, with no error.
- `get_node` confirms: Card A (0:3) at (0,0), width=100, height=100, opacity=0.5; Card B (0:4) at (150,0), width=100, height=100, opacity=0.5 — opacity applied, widths unchanged.
- `viewport_zoom_to_fit` reports bounds of 250x100, consistent with two 100-wide rects with a 50px gap (widths unchanged).
- The `batch_update` supported props (spacing, padding, sizing, name, visible, corner_radius, etc.) do not include `width`, and no other available MCP tool can resize an existing node.

Expected Result:
`batch_update` should apply `width=150` (and `opacity=0.5`) to both rectangles in one call, or at minimum return an explicit error for unsupported properties instead of silently dropping them.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed (agent verdict: not-approve)
- Attempt transcripts:
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_0f86b389-ea68-4c48-8a0e-1b3addc01714.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_35a04d6d-c48d-4289-86e1-03afbc6be0ae.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_8082898e-124a-4bcb-941e-c2aaa6791edd.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_8b78ef81-4506-436e-b0bc-2e49aa201625.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_9f4003cc-34f3-4f2c-a465-728237aa8a05.txt`

Agent report (verbatim tail of failing run):

```
## Report

**What I did:**
1. **create_shape** — Created `Card A` (id `0:3`) as a 100×100 rectangle at (0,0), and `Card B` (id `0:4`) as a 100×100 rectangle at (150,0). ✅
2. **batch_update** — Sent a single operations JSON applying `{"width":150,"opacity":0.5}` to both rectangles. The tool returned `"updated": 2`, but the per-node results listed only `["opacity"]` as the applied property — **`width` was silently ignored** for both nodes.
3. **viewport_zoom_to_fit** — Succeeded; reported bounds of 250×100 (consistent with two 100-wide rects with a 50px gap, i.e., widths unchanged).
4. **Verification** (`get_node` on both + `find_nodes`):
   - `Card A` (0:3): RECTANGLE at (0,0), **width=100**, height=100, **opacity=0.5**
   - `Card B` (0:4): RECTANGLE at (150,0), **width=100**, height=100, **opacity=0.5**
   - `find_nodes` confirms exactly the two expected rectangles exist.

**Findings:** Creation, opacity update, zoom, and verification all worked. However, the `width=150` part of the batch update did **not** take effect — both rectangles remain 100px wide. The `batch_update` tool's supported props (spacing, padding, sizing, name, visible, corner_radius, etc.) don't include `width`, so it was dropped without error, and no other available MCP tool can resize an existing node. The requested end state (both cards at width 150) could not be achieved.

One part of the required outcome (width=150 on both rectangles) failed because `batch_update` doesn't support the `width` property and silently ignored it, with no alternative resize tool available.

verdict: not-approve
```
