# DesignPen [clipboard / copy-paste]: 'copy as text' fails QA — 3/5 runs report broken workflow (00104-copy-as-text-ui)

Description:
The Copy/Paste as > Copy as text flow on a text layer is degraded by three separate issues. First, at default zoom the right-click context menu is taller than the 720px viewport and does not scroll, so the "Copy/Paste as" item near the bottom is cut off and unreachable via the normal flow. Second, after zooming the browser to 80% to fit the menu, canvas hit-testing is misaligned — clicks/right-clicks on the text layer miss it and deselect it (pointer coordinates not recalibrated after zoom change). Third, verification via "Paste here" fails with the toast "Clipboard access is blocked in this browser context". The "Copy as text" action itself produced no error toast, so the copy likely succeeded, but it could not be positively verified end-to-end.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Select the Text tool (T) in the bottom toolbar, click on the canvas, and type "clipboard check" to create a text layer.
3. Select the text layer (blue highlight in Layers panel, selection handles on canvas).
4. Right-click the text layer on the canvas at default zoom — observe the context menu is taller than the viewport, with "Copy/Paste as" cut off at the bottom and no way to scroll to it (arrow keys go to the canvas and nudge the layer instead).
5. Zoom the browser page to 80% so the full menu fits, then try right-clicking the text layer on the canvas — observe clicks miss/deselect it; instead right-click its row in the Layers panel.
6. Choose Copy/Paste as > Copy as text from the context menu.
7. Attempt to verify by right-clicking empty canvas and choosing "Paste here".

Actual Result:

- Context menu overflow bug: at default zoom the "Copy/Paste as" item is off-screen and unreachable — the menu doesn't scroll, and arrow keys nudge the selected layer 1px on the canvas instead of navigating the menu.
- Canvas hit-testing misalignment at 80% browser zoom: clicks/right-clicks on the text layer miss it and deselect it; the Layers panel row had to be used as a workaround.
- "Copy as text" itself clicked with no error toast, so the copy most likely succeeded, but verification via "Paste here" failed with a red error toast: "Clipboard access is blocked in this browser context", so the copied content could not be confirmed.

Expected Result:
The right-click context menu should fit (or scroll) within a 720px viewport so "Copy/Paste as > Copy as text" is reachable at default zoom, canvas hit-testing should remain accurate after browser zoom changes, and Copy as text should place the layer's plain text content on the clipboard verifiably.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 3 of 5 runs failed (2 approved)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_029240a3-1c4c-428d-a2af-07698dc1e1f9.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_8e9340d1-a6ee-4869-a975-7bafa45b4dc4.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_dcbeeadc-cc00-431d-9d4b-e8543e4c4a5e.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_e5d237c9-504b-42b9-b993-5ff9c055e395.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_e9dda8c7-687f-4dcd-aa29-f72c6dd16af4.txt`

Agent report (verbatim tail of failing run):

```
The task is complete. Here's a summary of what happened:

**What was accomplished:**
1. ✅ Created a text layer using the Text tool (T) in the bottom toolbar and typed "clipboard check"
2. ✅ Selected the text layer (confirmed by blue highlight in the Layers panel, selection handles on canvas, and Text properties in the right panel)
3. ✅ Right-clicked and chose **Copy/Paste as > Copy as text** — the submenu appeared with options (Copy as text, Copy as SVG, Copy as PNG, Copy as JSX, Copy node ID, Copy XPath) and "Copy as text" was clicked successfully with no error

**Problems encountered along the way:**
- **Context menu overflow bug:** At default zoom, the right-click context menu was taller than the 720px viewport, so the "Copy/Paste as" item at the bottom was cut off and unreachable — the menu doesn't scroll, and arrow keys went to the canvas (nudging the layer 1px, which I restored to Y=250). I had to work around this by zooming the browser to 80% so the full menu could fit.
- **Canvas hit-testing misalignment at 80% zoom:** Clicks/right-clicks on the text layer on the canvas missed it (deselecting it), apparently due to the app not recalibrating pointer coordinates after the zoom change. I worked around this by selecting and right-clicking the layer row in the Layers panel instead, which opened the same context menu reliably.
- **Clipboard verification blocked:** When I tried to verify the copy by using "Paste here", the app showed a red error toast: *"Clipboard access is blocked in this browser context"* — clipboard read is blocked in this environment, so I couldn't confirm the pasted content end-to-end. The "Copy as text" action itself produced no error toast (while the app clearly surfaces clipboard failures as toasts), so the copy most likely succeeded, but it couldn't be positively verified.

The intended end state was reached (text layer "clipboard check" created and selected, Copy as text executed via the right-click menu), but I hit a menu-overflow bug that made the required menu item unreachable by the normal flow, a canvas hit-testing bug at the workaround zoom level, and a clipboard-access block that prevented verification.

verdict: not-approve
```
