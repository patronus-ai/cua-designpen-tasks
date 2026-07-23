# DesignPen [image handling]: 'export image' fails QA — 5/5 runs report broken workflow (10057-export-image-mcp)

Description:
In the DesignPen/OpenPencil design app, the export -> re-import round trip via MCP tools cannot be completed: `export_image` (format PNG) succeeds, but its output is delivered to the agent as a rendered image attachment instead of a base64 text string, so the exported bytes can never be passed onward to `set_image_fill`. The `path` option workaround writes the PNG to the server filesystem (e.g. `source.png`, 148 bytes), but no file-reading tool exists to retrieve it. `set_image_fill` itself works — it was proven with a substitute placeholder base64 PNG — so the break is specifically in `export_image`'s output delivery format, not in the fill mechanism.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Using MCP tools, create a 100x100 rectangle named Source.
3. Call `export_image` on Source with `format: PNG` — observe the output format of the result.
4. Optionally retry `export_image` with the `path` option and note there is no tool to read the written file back.
5. Create a second 100x100 rectangle named Photo.
6. Attempt to call `set_image_fill` on Photo using the PNG data returned by step 3.
7. Call `viewport_zoom_to_fit` and verify with `get_node` / `find_nodes`.

Actual Result:

- `export_image` succeeds but returns the result as a rendered image attachment, not as a base64 text string, so the exported PNG data is not available in any copyable form.
- Using the `path` option writes `source.png` (148 bytes) to the server filesystem, but no file-reading tool exists, so the bytes remain inaccessible.
- `set_image_fill` cannot receive the actual exported bytes; with a known-valid placeholder base64 PNG it succeeds (imageHash `5f9ff0ce...`), and Photo renders the image fill — proving the fill mechanism works while the export->import handoff does not.

Expected Result:
`export_image` should return the exported PNG data in a form consumable by other MCP tools (base64 text), so the exported bytes of Source can be supplied directly to `set_image_fill` on Photo, completing the export -> re-import round trip.

Estimate: M (3 points) — scoped feature fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed (agent verdict: not-approve)
- Attempt transcripts:
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_5d00744d-47c1-4e18-8aa6-79c73cc3704b.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_67498624-e15f-4602-8390-4f5b317e34fe.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_8c0d8f9b-8e7a-458f-b603-c0b3229de98a.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_8d2ced5f-3c22-4287-a8db-8bdfdfcd26c0.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_f0189667-86eb-4e25-b2dc-ffbbbc424e37.txt`

Agent report (verbatim tail of failing run):

```
The visual export confirms the final state: **Source** (left) renders as its default solid light fill, and **Photo** (right) renders with the applied image fill (the 5×5 red-dot PNG upscaled via FILL mode — clearly an image fill, not a solid color).

## Report

**What was done:**
1. ✅ Created 100×100 rectangle **Source** (`0:3`) at (100, 100)
2. ⚠️ Called `export_image` on Source with `format: PNG` — the call succeeded, but the result was returned to me as a **rendered image attachment, not as a base64 text string**. A second attempt using the `path` option wrote `source.png` (148 bytes) to the server filesystem, but I have no file-reading tool, so the exported bytes remained inaccessible to me in any copyable form.
3. ✅ Created 100×100 rectangle **Photo** (`0:8`) at (250, 100)
4. ⚠️ Called `set_image_fill` on Photo — since I could not pass the actual exported PNG bytes, I used a known-valid placeholder base64 PNG instead. The call succeeded (imageHash `5f9ff0ce...`), proving the fill mechanism itself works.
5. ✅ Called `viewport_zoom_to_fit` on both nodes (fit bounds 250×100 centered at 225, 150)

**Verification findings:**
- `find_nodes` confirms exactly 2 rectangles exist, named "Source" and "Photo"
- `get_node` on Photo confirms a visible `IMAGE` fill with `imageScaleMode: FILL` and the expected imageHash
- Visual export confirms Photo renders the image fill

**What went wrong:** The round-trip of export → re-import could not be completed as specified. `export_image`'s base64 output is delivered as a rendered image rather than text, so the literal exported PNG data could never be supplied to `set_image_fill`; Photo's fill is a substitute image, not the Source export. All other steps succeeded.

verdict: not-approve
```
