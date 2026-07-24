# DesignPen [vector editing]: 'vector shape builder click' fails QA — 3/5 runs report broken workflow (00049-vector-shape-builder-click-ui)

Description:
The Shape builder subtool's click action is a silent no-op. With a closed square carved into two cells by a crossing line, activating Shape builder (More menu > Shape builder, or M) gives working per-cell hover highlighting, but clicking a cell produces no persistent change: no region is carved out into its own shape, no new layer, no path-data change, no persistent selection. The region engine itself works — a drag across both cells correctly merges them and dissolves the divider — so specifically the click action appears broken/unimplemented. The same session also hit an app crash (navigation to about:blank while interacting with the right panel after an add/remove fill test) requiring a reload and snapshot recovery.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Press P to activate the Pen tool; draw a closed square (four corner clicks plus a click on the start point to close) and commit with Enter ("Vector 1", 200×200).
3. Double-click the square to re-enter the path (vector-edit toolbar Move/Lasso/Paint/Bend/Cut/More appears).
4. With the Pen, draw a straight line across the square so it is carved into two cells. Note: start the line just outside the shape — clicking exactly on the square's edges adds anchor points to those segments instead of starting a new subpath.
5. Activate the Shape builder subtool via More menu > Shape builder or by pressing M; hovering highlights each cell individually.
6. Click one cell.

Actual Result:

- "**Shape-builder click on a cell does nothing.**" Clicking cells multiple times (top and bottom, with and without a fill applied) produces "no region is carved out/split into its own shape, no new layer, no path-data change, no persistent selection — the click is a silent no-op." Any highlight is only hover feedback; afterwards there is still one layer "Vector 1" with the square + divider line unchanged.
- The region engine works for drags: a drag across both cells correctly merged them and dissolved the divider.
- App crash: while interacting with the right panel (after an add/remove fill test, panel rendered horizontally shifted/clipped with a stuck "Add fill" tooltip), the app navigated to about:blank; after reload the document was recovered from a snapshot (project renamed "snapshot").
- Minor: the Inspect panel's SVG export omits the open line subpath; Ctrl+Z in edit mode failed to undo pen point-additions; after the reload, double-click on the shape edge no longer re-entered edit mode (Enter was needed).

Expected Result:
Clicking a cell with the Shape builder subtool should carve that region out into its own shape (persistent path/layer change), consistent with the tool's working hover detection and drag-merge behavior; the app must not crash to about:blank during normal panel interaction.

Estimate: L (5 points) — state/undo consistency issue, needs investigation across the edit pipeline

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 3 of 5 runs failed (2 approved)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_09d272ff-d8af-4c3b-a2e4-7aa24fcf3e5e.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_11e1cc7b-a38a-4a9c-ba20-76cea4419a65.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_32cf5051-c602-4aeb-8c99-a06eae1a1e44.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_3655181c-a8a4-469d-947d-b47004fddbd5.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_e1b8a1d9-b9a2-4ccb-8bbc-6fa81636db71.txt`

Agent report (verbatim tail of failing run):

```
Confirmed — the highlight was only hover feedback; after the shape-builder click there is no persistent change to the path (still one layer "Vector 1", square + divider line unchanged, no carved-out cell shape).

All requested steps were performed. Here's my report:

**What worked:**
- **Pen tool (P)** activated via keyboard; drew a closed square (four corner clicks + click on the start point to close).
- **Commit** via Enter — the path became object "Vector 1" (200×200).
- **Re-enter via double-click** — worked, showing the vector-edit toolbar (Move/Lasso/Paint/Bend/Cut/More).
- **Straight line across the square** — drawn in edit mode with the Pen. Note: clicking exactly on the square's edges adds anchor points to those segments instead of starting a new subpath, so I started the line just outside the shape; it crosses the square fully and carves it into two cells (confirmed — Shape builder hover highlights each cell individually).
- **Shape builder** — activated both via More menu > Shape builder and via the M shortcut; per-cell hover detection works.

**Problems encountered:**
1. **Shape-builder click on a cell does nothing.** I clicked cells multiple times (top and bottom, with and without a fill applied): no region is carved out/split into its own shape, no new layer, no path-data change, no persistent selection — the click is a silent no-op. The tool's region engine itself works (a drag across both cells correctly merged them and dissolved the divider, which I undid with Ctrl+Z), so the click action of the subtool appears broken/unimplemented.
2. **App crash:** while interacting with the right panel (after an add/remove fill test, during which the panel rendered horizontally shifted/clipped with a stuck "Add fill" tooltip), the app navigated to a blank page (about:blank). I had to reload; the document was recovered from a snapshot (project renamed "snapshot").
3. Minor issues: the Inspect panel's SVG export omits the open line subpath (shows only the square, though the viewBox includes the line's bounds); Ctrl+Z in edit mode failed to undo pen point-additions; after the reload, double-click on the shape edge no longer re-entered edit mode (had to use Enter).

The core deliverable (square carved into two cells, shape builder activated, one cell clicked) is in place, but the final step's feature misbehaved and the app crashed mid-session.

verdict: not-approve
```
