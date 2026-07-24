# DesignPen [text & typography]: 'attach text to path' fails QA — 5/5 runs report broken workflow (10029-attach-text-to-path-mcp)

Description:
The text-on-path workflow in the DesignPen/OpenPencil design app is broken at three points in the MCP tool chain. First, `create_vector` rejects an open two-vertex network with `"Invalid VectorNetwork: regions must be an array"` (the `regions` field is not documented as required) yet still creates a stray vector node before validation fails, and no delete tool exists to remove the orphan. Second, the successfully created vector reports bounds of 100x100 instead of the ~300x80 extent implied by the supplied (0,0)->(300,80) network, so the path geometry is either not applied or not reflected in the node's bounds. Third, `attach_text_to_path` returns success but produces no observable change on the text node — `get_node` exposes no text-on-path indicator, path property, or geometry change, so the binding cannot be verified.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Using MCP tools, create a text layer named 'River label' with characters 'along the bend'.
3. Call `create_vector` for a vector named 'Flow path' from an open two-vertex network (0,0)->(300,80), passing only `vertices` and `segments` (no `regions` field) — observe the validation error and check the page tree for a stray node.
4. Retry `create_vector` with `regions: []` so the call succeeds.
5. Call `attach_text_to_path` binding the text node to the vector node.
6. Call `viewport_zoom_to_fit`.
7. Verify with `get_page_tree` / `get_node` / `find_nodes`.

Actual Result:

- The first `create_vector` call fails with `"Invalid VectorNetwork: regions must be an array"` but still creates a stray vector node `0:4` "Flow path" (bare, 100x100, no stroke); no delete tool is available, so the document ends up with two "Flow path" vectors.
- The retried vector `0:5` reports `width: 100, height: 100` instead of ~300x80 for the (0,0)->(300,80) network; `viewport_zoom_to_fit` bounds (x spanning only 100->300) corroborate the wrong 100x100 size. `get_node` exposes no `vectorNetwork`/`vectorPaths` data.
- `attach_text_to_path` returns success (`{"id": "0:3"}`) but `get_node` on the text node shows no text-on-path indicator, no path property, and unchanged geometry/position — the binding is unverifiable.

Expected Result:
`create_vector` should either accept an open network without `regions` or fail atomically without creating an orphan node; the created vector's bounds should reflect the supplied network (~300x80); and after `attach_text_to_path` succeeds, the binding should be observable on the text node via `get_node` (path reference and/or geometry change).

Estimate: S (2 points) — small handler/layout fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed (agent verdict: not-approve)
- Attempt transcripts:
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_263c3ff5-9a21-4361-a49d-112e1b657dda.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_276b25eb-86ff-431d-a9ef-743726cfc377.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_a3640eca-f469-4776-83d2-a261e655f793.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_e40f050b-8893-4b17-b829-566d966b6ab3.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_f68883c4-d000-4535-b7df-3adce9d3da94.txt`

Agent report (verbatim tail of failing run):

```
All steps have been executed. Here is my verification report:

## Report

**What was created (per the page tree):**
- ✅ **TEXT node `0:3` "River label"** — exists with `characters: "along the bend"` (Inter 14, at 100,100, 200×40).
- ✅ **VECTOR node `0:5` "Flow path"** — exists with the blue stroke applied (weight 2).
- ✅ `attach_text_to_path(textId: 0:3, pathId: 0:5)` returned success (`{"id": "0:3"}`).
- ✅ `viewport_zoom_to_fit` succeeded, centering on (200, 200) with bounds x:100, y:100, 200×200.

**Problems found during verification:**

1. **Orphan duplicate node:** My first `create_vector` call failed with `"Invalid VectorNetwork: regions must be an array"` (the schema description didn't mention `regions` was required for an open path). Despite returning an error, the tool **still created a stray vector node `0:4` "Flow path"** (bare, 100×100, no stroke) before validation failed. There is no delete tool available, so this orphan duplicate remains on the canvas — the document now has two "Flow path" vectors instead of one.

2. **Vector geometry doesn't reflect the supplied network:** The successfully created vector `0:5` reports `width: 100, height: 100`, but a two-vertex network (0,0)→(300,80) should yield an extent of roughly 300×80. The `viewport_zoom_to_fit` bounds (x spanning only 100→300) corroborate that the scene graph treats the vector as 100×100 — so the path either wasn't applied to the node's geometry or isn't reflected in its bounds. `get_node` exposes no `vectorNetwork`/`vectorPaths` data, so I cannot confirm the two-vertex segment actually exists on the node.

3. **Binding unverifiable:** After `attach_text_to_path` reported success, `get_node` on the text node shows no text-on-path indicator — no path property, and its geometry/position is unchanged (the tool claims it "copies the path geometry onto the text node", but nothing observable changed). The binding cannot be confirmed through any available tool output.

**Summary:** The nominal sequence completed (text created and set, vector created on retry, attach call and zoom both returned success), but the session was not clean: the failed first `create_vector` call left an undeletable orphan duplicate node, the vector's reported dimensions contradict the requested (0,0)→(300,80) network, and the text-to-path binding could not be verified in the node data.

Because of the validation error that left a stray duplicate node I couldn't remove, and the inability to verify that the vector network and text-path binding were genuinely applied — verdict: not-approve
```
