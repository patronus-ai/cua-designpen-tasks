# DesignPen [strokes]: 'set stroke width profile' fails QA — 3/5 runs report broken workflow (10109-set-stroke-width-profile-mcp)

Description:
The `create_vector` MCP tool in the DesignPen/OpenPencil design app has a failed-call-still-creates-a-node bug: when a call fails validation with `"Invalid VectorNetwork: regions must be an array"` (the tool requires an explicit empty `regions` array even for open paths), it nonetheless creates an orphan VECTOR node with no stroke or path applied before erroring. Because no delete tool exists in the MCP set, the document is left with an unremovable duplicate. The stroke-width-profile workflow itself otherwise works — a retry with `regions: []` created the "Taper" vector correctly and `set_stroke_width_profile` accepted 3 points — though `get_node` does not expose the profile data for read-back, so the only confirmation is the tool's success response.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Call `create_vector` to create a vector named "Taper" from an open two-vertex network (0,0)->(100,0) with a 4px black stroke, omitting the `regions` field from the VectorNetwork JSON.
3. Observe the error `"Invalid VectorNetwork: regions must be an array"`.
4. Call `find_nodes` — observe an orphan "Taper" node was created by the failed call anyway.
5. Retry `create_vector` with `regions: []` — a second "Taper" vector is created successfully.
6. Call `set_stroke_width_profile` on the new vector with points making it thin at the start and thick at the end (e.g. `{t:0, width:0.5}`, `{t:0.5, width:4}`, `{t:1, width:10}`).
7. Call `viewport_zoom_to_fit` and verify with `get_node`/`find_nodes`.

Actual Result:

- The first `create_vector` call fails with `"Invalid VectorNetwork: regions must be an array"` but still creates an orphan node (`0:3`, named "Taper", no stroke or path applied); `find_nodes` confirms two "Taper" vectors exist.
- There is no delete tool in the MCP set, so the stray node cannot be cleaned up.
- The intended vector `0:4` is correct: solid black stroke, weight 4, and `set_stroke_width_profile` confirmed `pointCount: 3` — but `get_node` does not expose the profile data for read-back.
- Minor anomaly: `get_node` reports the line's bounds as 100×100 even though a horizontal line with a max 10px profile width should be far shorter vertically.

Expected Result:
A `create_vector` call that fails validation should be atomic — no node should be created on error (or `regions` should default to an empty array for open paths). Additionally, the stroke width profile should be readable back via `get_node`, and bounds should reflect the actual geometry.

Estimate: M (3 points) — scoped feature fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 3 of 5 runs failed (agent verdict: not-approve; 2 approved)
- Attempt transcripts:
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_3f2250c2-a3c5-495c-ae86-e7ddef68c49f.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_95bdfe19-b734-4015-84d9-8bb4b44ad7ae.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_a99ba80c-ea74-4edb-b01c-012b79510158.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_de69f18a-3d63-4142-b2ac-83111e3c54dd.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_f520c1dc-ebb3-4137-87c1-2622b9a73616.txt`

Agent report (verbatim tail of failing run):

```
**Verification summary — what I found:**

1. **Vector created:** Node `0:4`, name **"Taper"**, type **VECTOR**, positioned at (100, 100), built from the open two-vertex network (0,0)→(100,0) with one segment and no regions (open path).
2. **Stroke:** Confirmed via `get_node` — solid black (`r:0, g:0, b:0, a:1`), **weight 4**, opacity 1, visible, center-aligned.
3. **Width profile:** `set_stroke_width_profile` accepted 3 points — `{t:0, width:0.5}` → `{t:0.5, width:4}` → `{t:1, width:10}` — and confirmed `pointCount: 3`, so the stroke tapers from thin at the start to thick at the end. (Note: `get_node` doesn't expose the profile data for read-back; the only confirmation is the tool's success response.)
4. **Viewport:** `viewport_zoom_to_fit` succeeded, centering on (150, 150) over the node's bounds.

**Problems encountered:**

- My first `create_vector` call failed with `"Invalid VectorNetwork: regions must be an array"` (the tool requires an explicit empty `regions` array for open paths — a schema quirk, easily worked around).
- **Bug/side effect:** despite returning an error, that failed call still **created an orphan node** (`0:3`, also named "Taper", with no stroke or path applied). `find_nodes` confirms two "Taper" vectors now exist. There is **no delete tool** available in the MCP set, so I cannot clean up the stray node — the document is left with an unwanted duplicate.
- Minor anomaly: `get_node` reports the line's bounds as 100×100 even though a horizontal line with a max 10px profile width should be far shorter vertically — likely a default-size reporting quirk.

The intended vector `0:4` is correct and complete, but the failed-call-still-creates-a-node bug left an orphan duplicate I couldn't remove.

verdict: not-approve
```
