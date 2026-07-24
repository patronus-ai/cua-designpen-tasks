# DesignPen [MCP tools]: 'path scale' fails QA — 5/5 runs report broken workflow (10089-path-scale-mcp)

Description:
In the DesignPen/OpenPencil design app, the `path_scale` workflow is broken in two ways. First, `create_vector` fails an open two-vertex network with `"Invalid VectorNetwork: regions must be an array"` while still creating a leftover orphan node (no stroke, default 100x100) that cannot be removed because no delete tool exists — leaving two "Grow" vectors. Second, after `path_scale` with factor 2 returns success on the retried vector, `get_node` still reports width 100 x height 100: for a horizontal (0,0)->(100,0) line the height should be ~0 (plus stroke) and the post-scale width should be 200, and `viewport_zoom_to_fit` called after scaling also reports only 100x100. `get_node` exposes no vector network/path data, so the scale either was not applied to the geometry or cannot be verified at all.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Call `create_vector` for a vector named Grow from an open two-vertex network (0,0)->(100,0) with a 2px black stroke, passing `vertices` and `segments` without a `regions` field — observe the validation error, then check `find_nodes` for a leftover "Grow" node.
3. Retry `create_vector` with `regions: []` so the call succeeds.
4. Call `path_scale` on the vector with factor 2.
5. Call `viewport_zoom_to_fit` on the vector.
6. Verify with `get_node` / `find_nodes`, checking the node's reported width/height after scaling.

Actual Result:

- The first `create_vector` attempt fails with `"Invalid VectorNetwork: regions must be an array"` but nonetheless creates leftover node `0:3` (no stroke, default 100x100); `find_nodes` shows two "Grow" vectors and no delete tool is available to clean up.
- `path_scale(id=0:4, factor=2)` returns success (`{id:"0:4", factor:2}`), but `get_node(0:4)` still reports width 100 x height 100 — the width should be 200 after a factor-2 scale and the height ~0 for a horizontal line; `viewport_zoom_to_fit` called after scaling also reports bounds of only 100x100.
- `get_node` does not expose the vector network/path data, so there is no way to confirm the vertices were actually doubled.

Expected Result:
`create_vector` should not leave an orphan node when it errors; and a successful `path_scale` with factor 2 should observably double the path geometry — reported bounds of ~200 wide (and ~0 tall plus stroke for this line), with `viewport_zoom_to_fit` framing the scaled extent.

Estimate: M (3 points) — scoped feature fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed (agent verdict: not-approve)
- Attempt transcripts:
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_0ee80117-883f-4276-96aa-f65ed4e84808.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_5a345ea5-8d3e-4cd5-b61f-c1e9b57759ea.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_80b506ee-0878-4745-a7ba-57dc4f86ae4c.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_9e14a185-18bf-4109-ad8e-7f68b5f5b2ab.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_a7dc1789-95b5-4585-82b2-8e01ae309a0b.txt`

Agent report (verbatim tail of failing run):

```
All steps executed. Here is my verification report:

## Report

**Actions performed:**
1. `create_vector` — first attempt with `{"vertices":[(0,0),(100,0)],"segments":[{start:0,end:1}]}` failed with *"Invalid VectorNetwork: regions must be an array"*. Retried with `"regions":[]` added → succeeded, creating **"Grow" (id 0:4)** with stroke `#000000`, weight 2.
2. `path_scale(id=0:4, factor=2)` — returned success `{id:"0:4", factor:2}`.
3. `viewport_zoom_to_fit(["0:4"])` — returned center (150,150), bounds x:100, y:100, w:100, h:100.

**Verification findings:**
- `get_node(0:4)` confirms: name **Grow**, type **VECTOR**, stroke black (r:0,g:0,b:0,a:1), **weight 2**, visible, center-aligned — the name and stroke requirements are satisfied. ✅
- **Problem 1 — orphan node:** `find_nodes` revealed **two** "Grow" vectors. The first `create_vector` call that returned an error nonetheless created a leftover node `0:3` (no stroke, default 100×100). No delete tool is available, so the stray duplicate cannot be cleaned up. ❌
- **Problem 2 — scale not reflected/verifiable:** `get_node(0:4)` reports **width 100 × height 100**. For an open horizontal line (0,0)→(100,0) the height should be ~0 (plus stroke), and after `path_scale` factor 2 the width should be **200**. Even `viewport_zoom_to_fit`, called *after* scaling, reported bounds of only 100×100. Additionally, `get_node` does not expose the vector network/path data, so there is no way to confirm the vertices were actually doubled. The observable evidence suggests the scale did not take effect on the node's geometry (or at minimum cannot be verified). ❌

**Summary:** The "Grow" vector exists with the correct name and 2px black stroke, and all tool calls after the retry returned success. However, the erroring first call left an undeletable orphan duplicate node, and the post-scale bounds (100×100 instead of ~200 wide) indicate the factor-2 path scale either wasn't applied or isn't reflected/verifiable through the available tools.

Problems hit: (1) `create_vector` error still created an orphan "Grow" node with no way to delete it; (2) after `path_scale` factor 2, node bounds remained 100×100 rather than ~200 wide, and path data isn't inspectable to confirm the scale was applied.

verdict: not-approve
```
