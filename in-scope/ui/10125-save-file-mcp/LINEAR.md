# DesignPen [file handling]: 'save file' fails QA — 5/5 runs report broken workflow (10125-save-file-mcp)

Description:
The `save_file` MCP tool in the web build of the DesignPen/OpenPencil design app cannot save to a named file. Both a relative path (`artifact.fig`) and an absolute path (`/opt/patronus-gym/apps/cua_designpen/artifact.fig`) are rejected with "save_file with an explicit 'path' is not supported in the web build. Omit 'path' to persist the current document, or use export_fig." Saving works only via the pathless fallback (`save_file` with no path returns `saved: true`), which persists the document internally but never produces the requested `artifact.fig` file. Rectangle creation and zoom-to-fit work correctly.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Using MCP tools, create a 100x100 rectangle named 'Saved Marker'.
3. Call `save_file` with path `artifact.fig` — observe the rejection.
4. Retry with the absolute path `/opt/patronus-gym/apps/cua_designpen/artifact.fig` — same rejection.
5. Call `save_file` without a path — observe it succeeds but produces no `artifact.fig`.
6. Call `viewport_zoom_to_fit` and verify the rectangle with `get_node`.

Actual Result:

- `save_file` with `path: "artifact.fig"` and with the absolute path both fail with: "save_file with an explicit 'path' is not supported in the web build. Omit 'path' to persist the current document, or use export_fig."
- The pathless fallback `save_file` succeeds (`saved: true`), persisting document state internally — but not to the requested `artifact.fig` file; no `artifact.fig` is ever produced.
- Rectangle creation and zoom-to-fit succeed: `get_node` confirms RECTANGLE "Saved Marker" (`0:3`), exactly 100x100 at (0,0); viewport centered at (50, 50) with bounds (0, 0, 100, 100).

Expected Result:
`save_file` with path `artifact.fig` should write the current document to that file (or the suggested `export_fig` alternative should be available), so the document can be saved under an explicit filename in the web build.

Estimate: M (3 points) — scoped feature fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed (agent verdict: not-approve)
- Attempt transcripts:
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_508b48e6-c09d-4d28-aa1f-aec93be5858c.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_57ca9cae-c2e4-43d6-8a19-859bcceb52a4.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_b4ba0bfa-a447-4825-80aa-99b7b3a87df3.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_d4685444-0cff-4873-b138-c6355eb17faa.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_e617be5a-5cb5-4b63-af7c-6fe08706c362.txt`

Agent report (verbatim tail of failing run):

```
## Report

**What I did and found:**

1. ✅ **Rectangle creation** — Created a RECTANGLE named "Saved Marker" (ID `0:3`). Verification via `get_node` confirms:
   - Name: `Saved Marker`
   - Type: `RECTANGLE`
   - Size: exactly 100 × 100 pixels
   - Position: (0, 0)

2. ❌ **save_file with path `artifact.fig`** — This failed. Both `path: "artifact.fig"` and the absolute `path: "/opt/patronus-gym/apps/cua_designpen/artifact.fig"` were rejected with the error: *"save_file with an explicit 'path' is not supported in the web build. Omit 'path' to persist the current document, or use export_fig."* As a fallback, I called `save_file` without a path, which succeeded (`saved: true`), so the document state is persisted — but **not** to the requested `artifact.fig` file.

3. ✅ **viewport_zoom_to_fit** — Succeeded; viewport centered at (50, 50) with bounds (0, 0, 100, 100), matching the rectangle exactly.

**Summary:** The rectangle exists with the correct name and dimensions, the document is persisted, and the viewport is fitted to it. However, the explicit requirement to save to `artifact.fig` could not be fulfilled because the web build of the MCP server does not support `save_file` with an explicit path — no `artifact.fig` file was produced.

The task did not go fully smoothly: saving to the requested `artifact.fig` path is unsupported in this environment (tool returned an explicit "not supported in the web build" error for both relative and absolute allowed paths), so that requirement was blocked.

verdict: not-approve
```
