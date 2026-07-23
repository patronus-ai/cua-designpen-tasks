# DesignPen [MCP tools]: 'new document' fails QA — 5/5 runs report broken workflow (10123-new-document-mcp)

Description:
After creating a fresh empty document via the `new_document` MCP tool in the DesignPen/OpenPencil design app, the document has no addressable root or page node and `viewport_zoom_to_fit` cannot be satisfied. `new_document` itself works (`{"created": true}`, `find_nodes` confirms 0 nodes), but `get_node` on common root IDs (`0:0`, `0:1`) returns "Node not found", and `viewport_zoom_to_fit` — whose schema requires at least one node ID (`minItems: 1`) — returns `"error": "No valid nodes found"` for any ID, making the documented workflow (new_document then zoom-to-fit) impossible on an empty document. The tools also provide no way to confirm the "fresh tab" aspect; `new_document` only confirms creation.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Call the `new_document` MCP tool to open a brand-new empty document in a fresh tab.
3. Call `find_nodes` (no filter, and with `type: FRAME`) and `get_node` on root IDs `0:0` / `0:1` to inspect the fresh document.
4. Call `viewport_zoom_to_fit` (with a best-guess node ID such as `0:0`, since the schema requires at least one ID).

Actual Result:

- `new_document` returns `{"created": true}` and `find_nodes` confirms `count: 0` — the document is genuinely empty.
- `get_node` on `0:0` and `0:1` returns "Node not found" — no addressable root/page node exists in the fresh document.
- `viewport_zoom_to_fit` fails: the schema mandates at least one node ID (`minItems: 1`), and the call with `0:0` returns `"error": "No valid nodes found"`. There is no valid node ID that could make it succeed on an empty document.
- There is no way to confirm via MCP that the document opened in a fresh tab.

Expected Result:
A fresh document should expose an addressable root/page node (or `viewport_zoom_to_fit` should accept an empty document, e.g. by allowing zero IDs or fitting the page), so the new_document -> zoom-to-fit workflow can complete and be verified with the read tools.

Estimate: M (3 points) — scoped feature fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed (agent verdict: not-approve)
- Attempt transcripts:
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_017e46b2-51b0-4d5c-bacf-6f5d3a0a559b.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_333933f1-d8e1-419a-8586-84ec46b90169.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_d478b03d-9261-415a-b023-749ed20eca16.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_dd2a05b1-8a67-4223-bb27-93dbeac960f5.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_e92aa96d-8962-40f9-ae05-edef1c6cb5be.txt`

Agent report (verbatim tail of failing run):

```
## Summary of what I did and found

**Steps executed (MCP tools only):**

1. **`new_document`** → returned `{"created": true}` — a brand-new document was created successfully.

2. **Verification of the new document:**
   - `find_nodes` (no filter) → `count: 0`, no nodes — confirms the document is genuinely empty.
   - `get_node` on common root IDs (`0:0`, `0:1`) → "Node not found" — no addressable root/page node exists.
   - `find_nodes` with `type: FRAME` → `count: 0` — no frames either.

3. **`viewport_zoom_to_fit`** → This call **failed**. The tool's schema requires at least one node ID (`minItems: 1`), but the fresh empty document contains zero nodes. I attempted the call with a best-guess ID (`0:0`) and it returned `"error": "No valid nodes found"`. There is no valid node ID that could make this call succeed on an empty document.

**Conclusion:** The primary goal — opening a brand-new empty document — worked and was verified (0 nodes present). However, the required `viewport_zoom_to_fit` step could not complete successfully: it is impossible to satisfy on an empty document since the tool mandates at least one valid node ID and none exist. Additionally, the MCP tools provide no way to confirm the "fresh tab" aspect — the `new_document` response only confirms creation.

**What went wrong:** `viewport_zoom_to_fit` errored with "No valid nodes found" because the new empty document has no nodes to fit, and the tool requires ≥1 valid node ID — an unavoidable blocker for that step of the task.

verdict: not-approve
```
