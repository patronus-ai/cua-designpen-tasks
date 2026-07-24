# DesignPen [file save / MCP]: 'save_file with path' fails QA — 5/5 runs report broken workflow (10125-save-file-mcp)

Description:
`save_file` with an explicit `path` argument consistently fails with a `404 Not Found` error, even when the resolved path is inside the allowed root (`OPENPENCIL_MCP_ROOT`). Calling `save_file` with no path succeeds (`{"saved": true}`), which isolates the defect to the path-based save endpoint. Both a relative path (`artifact.fig`) and the absolute in-root path (`/opt/patronus-gym/apps/cua_designpen/artifact.fig`) return the same 404, so the artifact file is never written to the requested location. Reproduced 5/5 runs. This points to a missing/broken save-to-path route (or misconfigured `OPENPENCIL_MCP_ROOT` handling) on the app/server side.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport) with MCP tools available and `OPENPENCIL_MCP_ROOT` configured.
2. `create_shape` a 100×100 RECTANGLE named 'Saved Marker'.
3. Call `save_file` with `path: "artifact.fig"`.
4. (For comparison) call `save_file` with no path.

Actual Result:

- Rectangle 'Saved Marker' is created and verified correctly (id `0:3`, 100×100 at (0,0)).
- `save_file(path="artifact.fig")` fails: `Save to "/opt/patronus-gym/apps/cua_designpen/artifact.fig" failed: 404 Not Found`. Retried with the absolute in-root path — same 404.
- `save_file` with no path succeeds (`{"saved": true}`), confirming the connection/document are fine and the failure is specific to path-based save.
- The required `artifact.fig` file is never produced.

Expected Result:
`save_file` with a `path` inside the allowed `OPENPENCIL_MCP_ROOT` should write the document to that path and return success, producing the `artifact.fig` file — matching the behavior of the pathless save.

Estimate: M (3 points) — repair the path-based save endpoint / root resolution so in-root paths write successfully instead of returning 404; scoped to one MCP tool.

Evidence:

- QA job `db76a8af-97c9-41fb-bbba-42d2d887d5b8`, model `claude-opus-4-8` — 5 of 5 runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_75f5b117-0701-41e6-80cb-d8ff91a3a845.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_fd96056c-91b9-4131-b46d-8740e0a2e5aa.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_c1b327b3-1822-4671-9b5e-8372ec453e3c.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_acd9bac0-48e9-4bed-8456-9bc26dbf1eaa.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_858544e8-a726-464b-a141-bfb34d68575e.txt`

Agent report (verbatim tail of failing run):

```
I've completed all the steps and verified the results. Here's my report:

## Summary of Findings

**1. Create rectangle — ✅ Success**
- Created a RECTANGLE named "Saved Marker" (ID `0:3`), 100×100 px at position (0,0).

**2. Save file with path `artifact.fig` — ❌ Failed**
- `save_file` with `path: "artifact.fig"` returned an error: `Save to "/opt/patronus-gym/apps/cua_designpen/artifact.fig" failed: 404 Not Found`.
- Retried — same failure.
- Also tried the absolute path `/opt/patronus-gym/apps/cua_designpen/artifact.fig` (inside the allowed root) — same 404 error.
- Notably, calling `save_file` **without** a path succeeded (`{"saved": true}`), which shows the problem is specific to the path-based save required by the task.

**3. Viewport zoom to fit — ✅ Success**
- Returned center (50, 50) and bounds {x:0, y:0, width:100, height:100}, correctly framing the rectangle.

**4. Verification via MCP tools — ✅ Confirmed**
- `get_node("0:3")` confirms: type RECTANGLE, name "Saved Marker", x:0, y:0, width:100, height:100.
- `get_node("0:0", depth:2)` confirms the document structure: Document → Page 1 → "Saved Marker" rectangle. The shape is correctly present on the canvas.

## Conclusion
The rectangle creation, zoom-to-fit, and verification all worked correctly. However, the core required step — `save_file` with `path artifact.fig` — consistently failed with a **404 Not Found** error, despite the path being inside the allowed root and a path-less save succeeding. This is a blocker that prevented producing the required `artifact.fig` file.

verdict: not-approve
```
