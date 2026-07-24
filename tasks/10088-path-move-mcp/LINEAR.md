# DesignPen [MCP tools]: 'path move' fails QA — 5/5 runs report broken workflow (10088-path-move-mcp)

Description:
In the DesignPen/OpenPencil design app, the `path_move` workflow hits two bugs in the MCP tool chain. First, `create_vector` rejects an open two-vertex network with `"Invalid VectorNetwork: regions must be an array"` yet still creates an empty stray vector node named "Drift" before failing, with no delete tool available to clean it up. Second, after `path_move` (dx=50, dy=25) returns success on the retried vector, the node's reported bounds remain x:0, y:0, 100x100 — a horizontal 100px line should have a ~0-2px tall bounding box, and the +50/+25 translation is not reflected in the bounds at all; `get_node` also does not expose vector network vertices, so the move cannot be confirmed to have taken effect.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Call `create_vector` for a vector named Drift from an open two-vertex network (0,0)->(100,0) with a 2px black stroke, passing only `vertices` and `segments` (no `regions` field) — observe the validation error, then check `find_nodes` for a stray "Drift" node.
3. Retry `create_vector` with an explicit empty `regions: []` so the call succeeds.
4. Call `path_move` on the vector with dx=50, dy=25.
5. Call `viewport_zoom_to_fit`.
6. Verify with `get_node` / `find_nodes`, comparing the node's reported bounds before/after the move.

Actual Result:

- The first `create_vector` call is rejected with `"Invalid VectorNetwork: regions must be an array"` yet still creates node `0:3`, a bare "Drift" vector with no stroke/path; `find_nodes` shows two "Drift" vectors and no delete tool exists to undo the side effect.
- `path_move` returns success (`{id: "0:4", dx: 50, dy: 25}`), but the node bounds after the move remain x:0, y:0, 100x100 — the translation is not reflected, and a 100px horizontal line should not have a 100px-tall bounding box.
- `get_node` does not expose the vector network vertices, so the expected post-move points (50,25)->(150,25) cannot be confirmed; `viewport_zoom_to_fit` returns bounds (0, 0, 100x100), consistent with no observable move.

Expected Result:
`create_vector` should fail atomically (no orphan node) or accept the network without the undocumented `regions` field; and a successful `path_move` should observably translate the path — reported bounds should match the line geometry and shift by (dx, dy).

Estimate: M (3 points) — scoped feature fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed (agent verdict: not-approve)
- Attempt transcripts:
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_1c36a024-1a33-472e-9cb2-904cfdc5040c.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_1d2005e6-f014-4838-97cc-044c6a85f7de.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_26b419b6-7f4f-4ec9-9508-13c67d72c89f.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_4f32a8a4-9eaa-4a2a-b75c-efe7370fb2e7.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_a50bea13-4d3a-4117-b2e3-f906d5902f9f.txt`

Agent report (verbatim tail of failing run):

```
Confirmed: `0:3` is a stray leftover from my first `create_vector` call — the API returned an error ("Invalid VectorNetwork: regions must be an array") yet still created an empty vector node named "Drift" (no stroke, no path) before failing. I have no delete tool available in this MCP set, so I cannot clean it up.

## Report

**What was done:**
1. `create_vector` — first attempt with `{vertices, segments}` was rejected ("regions must be an array"); second attempt with an explicit empty `regions: []` succeeded, creating vector **"Drift" (id 0:4)** with a 2px black stroke.
2. `path_move` on `0:4` with dx=50, dy=25 — returned success `{id: "0:4", dx: 50, dy: 25}`.
3. `viewport_zoom_to_fit` on `0:4` — returned center (50, 50), bounds (0, 0, 100×100).

**Verification findings:**
- `get_node(0:4)` confirms: name **Drift**, type **VECTOR**, stroke color black (r:0, g:0, b:0, a:1), weight **2**, visible — stroke requirements are met. ✅
- **Problem 1 — stray duplicate:** `find_nodes` revealed **two** "Drift" vectors. The failed first `create_vector` call still created node `0:3` (a bare vector with no stroke/path) despite returning an error — a side-effect bug I cannot undo, since no delete tool is available.
- **Problem 2 — move not verifiable / geometry suspicious:** `get_node` does not expose the vector network vertices, so I cannot directly confirm the points moved to (50,25)→(150,25). Worse, the reported node bounds after `path_move` remain x:0, y:0, **100×100** — a horizontal 100px line should have a ~0–2px tall bounding box, and a +50/+25 translation is not reflected in the reported bounds at all. So while `path_move` reported success, the observable state does not confirm the translation took effect.

The target vector with the correct name and 2px black stroke exists and all tool calls eventually returned success, but the session hit a validation error that left an undeletable duplicate node, and verification could not confirm the path translation (bounds unchanged and inconsistent with the expected geometry).

verdict: not-approve
```
