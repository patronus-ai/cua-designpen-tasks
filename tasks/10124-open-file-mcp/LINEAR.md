# DesignPen [file handling]: 'open file' fails QA — 5/5 runs report broken workflow (10124-open-file-mcp)

Description:
The save-to-file / reopen workflow is impossible in the web build of the DesignPen/OpenPencil design app. `save_file` with an explicit path (e.g. `/opt/patronus-gym/apps/cua_designpen/beacon.fig`) is rejected with "save_file with an explicit 'path' is not supported in the web build. Omit 'path' to persist the current document, or use export_fig." — but the suggested `export_fig` tool is not exposed in the MCP toolset. Because no `.fig` file can ever be written to disk, `open_file` on that path then fails with "Failed to fetch file: Not Found" (default names `document.fig` and `untitled.fig` are also not found). Node creation, pathless `save_file` (internal persist), and zoom-to-fit all work; only save-as-named-file plus reopen is broken.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Using MCP tools, create an ellipse named "Beacon".
3. Call `save_file` with path `beacon.fig` (or the absolute `/opt/patronus-gym/apps/cua_designpen/beacon.fig`) — observe the rejection.
4. Note the error suggests `export_fig`, which is not present in the available MCP tool list.
5. Call `open_file` on `beacon.fig` so it loads in a new tab — observe the failure (also try `document.fig` / `untitled.fig` as possible default save targets).
6. Call `viewport_zoom_to_fit` and verify the ellipse with `get_node`.

Actual Result:

- `save_file` with an explicit path is rejected with: "save_file with an explicit 'path' is not supported in the web build. Omit 'path' to persist the current document, or use export_fig."
- The suggested fallback tool `export_fig` is not in the available MCP toolset, so the document can only be persisted internally, never to a named file.
- `open_file` on `/opt/patronus-gym/apps/cua_designpen/beacon.fig` fails with "Failed to fetch file: Not Found"; probing `document.fig` and `untitled.fig` also returns not found.
- The ellipse creation (ELLIPSE "Beacon", `0:3`, (100,100), 200x200), pathless `save_file` (`{"saved": true}`), zoom-to-fit, and `get_node` verification all worked.

Expected Result:
`save_file` with a path like `beacon.fig` should write the document to disk (or `export_fig` should be exposed in the MCP toolset as the error message suggests), and `open_file` on that file should then load it in a new tab.

Estimate: M (3 points) — scoped feature fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed (agent verdict: not-approve)
- Attempt transcripts:
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_14bd08dc-c851-4eed-ab25-f446bed44b26.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_a72c2c2b-79d4-461d-87ac-64adf7598c48.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_b6ccbda8-495c-48d4-8315-be505d3b3ad3.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_cddfc693-28ef-4647-958f-d0df61b7fb6c.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_f62b38b2-a3aa-4a21-b4fa-4df3d77d5b06.txt`

Agent report (verbatim tail of failing run):

```
## Report

Here's what I did and what I found during verification:

**Completed successfully:**
1. **Created the ellipse** — An ELLIPSE named "Beacon" (ID `0:3`) was created at (100, 100) with size 200×200.
2. **Persisted the document** — `save_file` without a path returned `{"saved": true}`.
3. **viewport_zoom_to_fit** — Succeeded, fitting the view to the Beacon ellipse (bounds: x=100, y=100, 200×200; center at 200, 200).
4. **Verification via get_node** — Confirmed the node `0:3` is `type: ELLIPSE`, `name: "Beacon"`, at (100, 100), 200×200. The full document tree shows: `Document (0:1)` → `Page 1 (0:2)` → `Beacon (0:3)`. The ellipse exists and is correctly named.

**Blocked:**
- **Saving as `beacon.fig`**: `save_file` with path `/opt/patronus-gym/apps/cua_designpen/beacon.fig` was rejected with the error: *"save_file with an explicit 'path' is not supported in the web build. Omit 'path' to persist the current document, or use export_fig."* The suggested `export_fig` tool is not in my available MCP toolset, so I could only persist the document internally without a named file.
- **Opening `beacon.fig` in a new tab**: Because the file was never written to disk, `open_file` on `/opt/patronus-gym/apps/cua_designpen/beacon.fig` failed with *"Failed to fetch file: Not Found"*. I also probed `document.fig` and `untitled.fig` as possible default save targets — both not found.

**Conclusion:** The ellipse creation, internal save, zoom-to-fit, and verification all worked, but the core requirement to save the document as `beacon.fig` and reopen it in a new tab could not be completed: the web build of `save_file` refuses explicit paths, and the recommended fallback (`export_fig`) is not exposed in my tool list, making `open_file` impossible since no `beacon.fig` exists on disk.

verdict: not-approve
```
