# DesignPen [MCP tools]: 'path flip' fails QA — 4/5 runs report broken workflow (10086-path-flip-mcp)

Description:
In the DesignPen/OpenPencil design app, the vector-creation half of the `path_flip` workflow is broken. `create_vector` rejects an open two-vertex network with `"Invalid VectorNetwork: regions must be an array"` (the `regions` field is not documented as required) yet still creates a stray, malformed vector node before failing — and no delete tool exists to clean it up, leaving a duplicate "Slope" node. The successfully retried vector reports bounds of 100x100 instead of the ~100x50 implied by the (0,0)->(100,50) segment (the orphan reports the same 100x100, suggesting a default size is reported rather than true path bounds), and `get_node` exposes no vector network data, so the result of `path_flip` (which itself returns success) cannot be verified. The core create -> flip -> zoom-to-fit sequence does complete on the retried node with the correct name and 2px black stroke.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Call `create_vector` for a vector named Slope from an open two-vertex network (0,0)->(100,50) with a 2px black stroke, passing only `vertices` and `segments` (no `regions` field) — observe the validation error, then check `find_nodes` for a stray "Slope" node.
3. Retry `create_vector` with `regions: []` so the call succeeds.
4. Call `path_flip` on the vector with `axis: vertical`.
5. Call `viewport_zoom_to_fit`.
6. Verify with `get_node` / `find_nodes`, checking the node's reported bounds and looking for vector network data.

Actual Result:

- The first `create_vector` call fails with `"Invalid VectorNetwork: regions must be an array"` but still creates a stray node `0:3` named "Slope" with no stroke/path; `find_nodes` confirms two "Slope" vectors and no delete tool is available to remove the orphan.
- The retried vector `0:4` reports width 100 x height 100, whereas a (0,0)->(100,50) segment should yield a height of ~50; the invalid orphan also reports 100x100, suggesting a default size rather than true path bounds.
- `path_flip` vertical returns success (`{"id":"0:4","axis":"vertical"}`), but `get_node` does not expose vector network data, so the post-flip vertex coordinates (expected (0,50)->(100,0)) cannot be confirmed.

Expected Result:
`create_vector` should accept an open network without an undocumented `regions` requirement, or fail atomically without leaving an orphan node; the vector's bounds should match the supplied path (~100x50); and after `path_flip`, the flipped geometry should be observable through the available tools.

Estimate: M (3 points) — scoped feature fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 4 of 5 runs failed (agent verdict: not-approve; 1 approved)
- Attempt transcripts:
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_4beb3f02-4448-485b-87bb-82e78fe8305c.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_86ec7ff5-cd35-4d1f-83e9-e1341f01a427.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_ad79e6f1-fc9b-40f0-91b6-85b6b0661301.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_be012ba9-9579-4f61-b1f0-b973cdaa7c61.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_f57dc87a-691d-4e31-884d-eb64d104e82c.txt`

Agent report (verbatim tail of failing run):

```
## Verification Report

**What I found:**

1. **Vector "Slope" (`0:4`) exists** with:
   - `type: VECTOR`, `name: "Slope"` ✓
   - Stroke: black `(r:0, g:0, b:0, a:1)`, weight **2**, visible, center-aligned ✓
   - Position (0,0)
2. **path_flip vertical** returned success (`{"id":"0:4","axis":"vertical"}`).
3. **viewport_zoom_to_fit** succeeded — viewport centered at (50,50) on bounds (0,0,100,100).

**Problems encountered:**

1. **Orphan node side effect (bug):** My first `create_vector` call failed with `"Invalid VectorNetwork: regions must be an array"` (the `regions` field wasn't documented as required). Despite returning an error, that call **still created a stray node `0:3` named "Slope"** with no stroke/path. `find_nodes` confirms **two** "Slope" vectors now exist, and no delete tool is available to clean up the orphan — the document is left polluted with a malformed duplicate.
2. **Geometry verification limits / size anomaly:** `get_node` does not expose the vector network data, so I could not directly confirm the post-flip vertex coordinates (expected (0,50)→(100,0)). Additionally, the node reports **width 100 × height 100**, whereas a (0,0)→(100,50) segment should yield a height of ~50 — the bounding box doesn't match the supplied path geometry (the invalid orphan `0:3` also reports 100×100, suggesting a default size is being reported rather than true path bounds).

The core sequence (create → flip → zoom-to-fit) did complete on node `0:4` with the correct name and 2px black stroke, but the errored-yet-created orphan duplicate node and the inability to verify the flipped path geometry mean the run was not clean.

verdict: not-approve
```
