# DesignPen [text & typography]: 'set text path options' fails QA — 5/5 runs report broken workflow (10110-set-text-path-options-mcp)

Description:
The text-on-path workflow in the DesignPen/OpenPencil design app has three related defects around `create_vector`, `get_node`, and `set_text_path_options`. First, a `create_vector` call that fails validation with `"Invalid VectorNetwork: regions must be an array"` still creates an orphan node (empty geometry, no strokes) before erroring, and no MCP delete tool exists to remove it. Second, `get_node` on the successfully created vector reports width 100 x height 100 instead of the ~300x80 extents implied by the path (0,0)->(300,80), and does not expose vectorNetwork data, so the path geometry cannot be confirmed. Third, `get_node` on the text node exposes no text-on-path properties (no offset/align/side fields), so `set_text_path_options` (`align: CENTER`, `offset: 24`) can only be confirmed indirectly by tool success responses, never by direct readback.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Using MCP tools, create a text layer named 'Curve note' reading 'ride the wave'.
3. Call `create_vector` for an open two-vertex network (0,0)->(300,80) omitting the `regions` field — observe the error and the orphan node it leaves behind (`find_nodes` shows an extra node).
4. Retry `create_vector` with `"regions": []` — the vector is created.
5. Call `attach_text_to_path` (text -> vector) — returns success.
6. Call `set_text_path_options` with `align: CENTER` and `offset: 24` — returns success.
7. Call `viewport_zoom_to_fit`.
8. Verify with `get_node` on both the vector and the text node.

Actual Result:

- The first `create_vector` call fails with `"Invalid VectorNetwork: regions must be an array"` but still creates an orphan node `0:4` ("Wave path", empty geometry, no strokes); `find_nodes` shows 3 nodes on the page instead of the expected 2, and there is no MCP delete tool to clean it up.
- `get_node` on the good vector `0:5` reports width 100 x height 100, not the ~300x80 extents implied by the path (0,0)->(300,80); zoom-to-fit union bounds (200x200) corroborate the wrong 100x100 scene size, and `get_node` does not expose vectorNetwork data.
- `get_node` on the text node exposes no text-on-path properties (no offset/align/side fields), so `align: CENTER` and `offset: 24` cannot be verified by readback despite `set_text_path_options` returning success (idempotently).

Expected Result:
`create_vector` should not leave an orphan node when it errors (or should accept open paths without an explicit empty `regions` array). The created vector's reported bounds should match the specified path extents (~300x80), and `get_node` should expose vectorNetwork geometry and text-on-path properties (align/offset/side) so the applied options are verifiable.

Estimate: M (3 points) — scoped feature fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed (agent verdict: not-approve)
- Attempt transcripts:
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_3ed35100-d059-455d-a818-599c716b4ea2.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_4f7c6082-5b78-41da-a05f-23d9baf99f17.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_53203f43-007c-420f-878b-36f376b01ee3.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_7687372d-dd25-4ed8-acc2-fb0025824713.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_97cb1f9c-94ec-45c5-861e-619b86ea29e3.txt`

Agent report (verbatim tail of failing run):

```
## Verification Summary

All requested operations were executed. Here's what I found when verifying:

**✅ Confirmed working:**
- **Text node `0:3`** — name "Curve note", characters "ride the wave" (confirmed via `get_node`).
- **Vector `0:5`** — "Wave path", created with the open two-vertex network (0,0)→(300,80) after I added the required `"regions": []` field to the VectorNetwork JSON.
- **`attach_text_to_path`** (text `0:3` → path `0:5`) returned success.
- **`set_text_path_options`** with `align: CENTER`, `offset: 24` returned success — and an idempotent re-call also succeeded, which per the tool contract ("TEXT node ID with a path binding") indirectly confirms the path binding exists.
- **`viewport_zoom_to_fit`** returned center (200, 200) with bounds covering both nodes.

**⚠️ Problems encountered:**
1. **Tool error with a side effect:** My first `create_vector` call failed with `"Invalid VectorNetwork: regions must be an array"` — but it still **created an orphan node `0:4`** ("Wave path", empty geometry, no strokes) before erroring. `find_nodes` shows 3 nodes on the page instead of the expected 2, and there is no MCP delete tool available to clean up this stray node, so the document is left with an unwanted artifact.
2. **Unverifiable path geometry:** `get_node` on vector `0:5` reports **width 100 × height 100**, not the ~300×80 extents implied by the path (0,0)→(300,80), and the zoom-to-fit union bounds (200×200) corroborate the 100×100 scene size. `get_node` does not expose vectorNetwork data, so I cannot positively confirm the path was applied with the specified coordinates.
3. **Unverifiable text-path options:** `get_node` on the text node exposes no text-on-path properties (no offset/align/side fields), so `align: CENTER` and `offset: 24` can only be confirmed indirectly by the successful tool responses, not by direct readback.

The core workflow (create text → create vector → attach → set options → zoom) completed and the tool calls all ultimately returned success, but the first vector-creation attempt errored while leaving an undeletable orphan node polluting the document, the vector's reported bounds don't match the specified path extents, and the read tools can't confirm the path geometry or text-path options took effect.

verdict: not-approve
```
