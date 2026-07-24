# DesignPen [MCP tools]: 'get selection' fails QA — 5/5 runs report broken workflow (10009-get-selection-mcp)

Description:
The `get_selection` MCP tool in DesignPen/OpenPencil never reflects the active selection. Immediately after `select_nodes(["0:3"])` returns `{"selected": ["0:3"]}` (success), `get_selection` returns `{"selection": []}` — consistently empty across multiple retries. The rest of the workflow works when the node id is sourced from the `create_shape`/`select_nodes` responses instead (create star, rename via `update_node`, `viewport_zoom_to_fit` all succeed), so the bug is isolated to `get_selection` not reading back selection state.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Using MCP tools only, call create_shape to create a star named Target (e.g. at (100,100), 200x200) — note the returned id (e.g. 0:3).
3. Call select_nodes with that id — it returns `{"selected": ["0:3"]}`.
4. Immediately call get_selection to read the selected node's id.
5. Retry the select_nodes + get_selection sequence several times.
6. Rename the node to 'Chosen' via update_node using the id from step 2, then call viewport_zoom_to_fit.

Actual Result:

- `get_selection` returns `{"selection": []}` (empty) every time, even immediately after `select_nodes` reports success with `{"selected": ["0:3"]}` — consistent across multiple retries.
- The workaround works: the id sourced from `create_shape`/`select_nodes` responses lets `update_node(id="0:3", name="Chosen")` succeed (`updated: ["name"]`), and `viewport_zoom_to_fit(["0:3"])` returns the star's correct bounds `{x:100, y:100, width:200, height:200}`.
- Because `get_selection` is broken, the prescribed flow (reading the node id from `get_selection`) is blocked and selection state / the rename cannot be independently read back.

Expected Result:
After a successful `select_nodes` call, `get_selection` should return the selected node id(s) (e.g. `{"selection": ["0:3"]}`) so the selection can be read back and used in subsequent tool calls.

Estimate: M (3 points) — scoped feature fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed (agent verdict: not-approve)
- Attempt transcripts:
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_41a7b6ff-6c5d-4829-be41-82db727bc2fa.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_670be923-4ea0-4055-b36a-afd5376902d7.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_75eb1410-d03c-4e61-a625-b35cd8bcf61c.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_7c0a4916-69bc-458d-a54e-2e577b9aaa95.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_c96da562-03db-4750-8445-c1a00a3c91de.txt`

Agent report (verbatim tail of failing run):

```
The node `0:3` still exists and accepts updates. Here's my final report:

## Report

**What was accomplished:**
1. ✅ Created a STAR node named "Target" at (100, 100), size 200×200 — it was assigned id `0:3`.
2. ✅ Called `select_nodes(["0:3"])` — it returned `{"selected": ["0:3"]}`, indicating success.
3. ❌ Called `get_selection` to read the selected node's id — it returned `{"selection": []}` (empty). I retried the select + get_selection sequence multiple times, and it consistently returned empty despite `select_nodes` reporting success each time.
4. ✅ Renamed the node to "Chosen" via `update_node(id="0:3", name="Chosen")` — the tool confirmed `updated: ["name"]`. (I had to source the id from the `create_shape`/`select_nodes` responses instead of `get_selection`, since the latter returned nothing.)
5. ✅ Called `viewport_zoom_to_fit(["0:3"])` — it returned bounds `{x:100, y:100, width:200, height:200}`, matching the star's expected geometry, confirming the node exists on canvas.

**Verification findings:**
- The node `0:3` definitively exists (confirmed by `viewport_zoom_to_fit` returning its correct bounds, and `update_node` accepting the id without error).
- The rename operation itself reported success (`updated: ["name"]`).
- However, I could **not** independently read back the node's name or confirm selection state, because `get_selection` appears to be broken in this environment: it always returns an empty selection immediately after a successful `select_nodes` call. This also prevented me from following the task's prescribed flow of reading the node id from `get_selection`.

**What went wrong:** `get_selection` never reflected the active selection (returned `[]` every time, even right after `select_nodes` succeeded). This blocked the required step of reading the id from `get_selection` and prevented full verification of the rename — I could only rely on the success responses of the other tools.

verdict: not-approve
```
