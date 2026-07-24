# DesignPen [file handling]: 'save-as-named-file then open' fails QA — 5/5 runs report broken workflow (10124-open-file-mcp)

Description:
The save-to-named-file / reopen workflow is broken via MCP. `save_file` with any explicit path (`beacon.fig`, the absolute `/opt/patronus-gym/apps/cua_designpen/beacon.fig`, or an arbitrary `test.fig`) consistently returns `404 Not Found`, so a named `.fig` is never written to disk. A path-less `save_file()` does return `{"saved": true}`, but gives no control over the filename, so it cannot satisfy "save as beacon.fig". Consequently `open_file("beacon.fig")` fails with `invalid zip data` (the file was never created). There is also a serious side-effect bug: a failed `open_file` call silently discards the active unsaved document — the previously created Beacon ellipse (`0:3`) disappears, node ids shift to a fresh blank document, and the work is lost. Node creation and `viewport_zoom_to_fit` work; the named-save + reopen flow is the broken part. (One of the five failing runs instead hit an "OpenPencil app is not connected" infra error rather than the 404; the 404 save bug is the dominant cause across the other four.)

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport); use only MCP tools.
2. Create an ellipse named "Beacon" (e.g. at (100,100), 200x200).
3. Call `save_file` with path `beacon.fig` (also try the absolute path and a different name like `test.fig`).
4. Call `save_file()` with no path.
5. Call `open_file("beacon.fig")`.
6. Call `viewport_zoom_to_fit` and re-check the document with `get_node`.

Actual Result:
- `save_file(path: "beacon.fig")` → `404 Not Found`; same for the absolute path and for `test.fig` — every path-based save 404s.
- `save_file()` with no path → `{"saved": true}` (only the unnamed default save works).
- `open_file("beacon.fig")` → `{"error":"invalid zip data"}` because the file was never written (a control name like `beacon_test_xyz.fig` returns the same error).
- Data-loss side effect: after the failed `open_file`, the active document is reset to a fresh blank "Document" → empty "Page 1"; the Beacon ellipse (`0:3`) is gone (`get_node 0:3` → "not found") and had to be recreated.
- Ellipse creation and `viewport_zoom_to_fit` themselves worked.

Expected Result:
`save_file` with a path like `beacon.fig` should write the document to disk, and `open_file` on that file should load it in a new tab. A failed `open_file` must not discard or reset the current unsaved document.

Estimate: M (3 points) — fix the path-based save endpoint (likely `OPENPENCIL_MCP_ROOT` misconfiguration causing the 404) plus guard `open_file` against clobbering the active document on failure.

Evidence:

- QA job `db76a8af-97c9-41fb-bbba-42d2d887d5b8`, model `claude-opus-4-8` — 5 of 5 runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_47545f96-8105-4eb7-8b96-f3e920b9a215.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_4908842a-2294-48ee-b8ab-b8a3c6591f8b.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_577bcc0b-9f5b-41cc-8ce0-4db36714fa0f.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_718d45b8-a500-49a9-8c61-87fbcabfb01c.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_629f5b93-783c-41cd-9e84-d0d935c5c02e.txt`

Agent report (verbatim tail of failing run):

```
2. Save the document as beacon.fig via save_file — Failed (blocker). save_file(path: "beacon.fig") returned 404 Not Found. I retried it, tried the absolute path /opt/patronus-gym/apps/cua_designpen/beacon.fig, and even a different filename test_save.fig — all returned the same 404. So saving with any explicit path is broken. A path-less save_file() did report {"saved": true}, but that gives no control over the filename, so it can't satisfy "save as beacon.fig".

3. open_file on beacon.fig — Failed. Returned {"error":"invalid zip data"} for both the relative and absolute paths — consistent with the file never having been written as a valid .fig (because the save in step 2 failed).

4. viewport_zoom_to_fit — Called it; it returned {"center":{0,0},"zoom":1,"empty":true}.

5. Verification — The failed open_file left the workspace in a reset/empty state:
   - get_node("0:3") → "Node not found" (the Beacon ellipse is gone).
   - get_node("0:0") → a Document frame containing only an empty Page 1 canvas (no children).
   - viewport_zoom_to_fit → empty: true.

Conclusion: The task could not be completed. Saving to a named file (beacon.fig) consistently fails with 404, open_file then fails with "invalid zip data" because the file was never written, and the attempted open wiped out the previously created Beacon ellipse — leaving an empty document. This looks like a broken save-with-path endpoint (possibly OPENPENCIL_MCP_ROOT not being configured so the write target 404s), which cascades into the open and the lost work.

verdict: not-approve
```
