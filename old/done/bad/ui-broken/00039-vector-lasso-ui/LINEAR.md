# DesignPen [vector editing]: 'vector lasso' fails QA — 5/5 runs report broken workflow (00039-vector-lasso-ui)

Description:
Arrow-key nudging of lasso-selected vertices in vector edit mode is broken. The Lasso subtool (toolbar button or Q) correctly selects vertices, but pressing ArrowUp never moves the selected points on canvas — instead the keypress decrements the whole layer's Y field in the Design panel (1px per press) while the rendered geometry stays frozen, and even that Y change is reverted on exiting edit mode (verified: exported SVG path unchanged). The phantom nudges also pollute the undo stack: Ctrl+Z steps the Y field 1px at a time instead of undoing the last edit, indicating a history/render desync. Mouse-dragging a vertex works, so the bug is specific to arrow-key nudging of vertex selections.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Press P to activate the Pen tool; click 5 alternating points to draw a zigzag; press Enter (or Escape) to commit it as "Vector 1".
3. Double-click the zigzag to enter vector edit mode (Move/Lasso/Paint/Bend/Cut toolbar with anchor points visible).
4. Activate the Lasso subtool (toolbar button or press Q) and sweep a freehand loop around two of the points — exactly those two select (solid filled anchors).
5. Press ArrowUp several times to nudge the selected points upward.
6. Exit vector edit mode (Escape or Enter-commit) and inspect the geometry; also try Ctrl+Z after the nudges.

Actual Result:

- Pressing ArrowUp with two points lasso-selected did not move them: "The canvas rendering never changed (verified by pixel-level zoom against the ruler)."
- Instead the layer's Y field in the Design panel decremented 1px per press (250→240 after 10 presses) as if the whole layer were being nudged, while H stayed 100 and nothing moved on canvas.
- On exiting vector edit mode, even that Y change was reverted to 250; the exported SVG path (`M1 101L71 1M71 1L141 101M141 101L211 1M211 1L281 101`) confirmed the geometry was completely unchanged.
- Same failure with the Move subtool active while the lasso selection was preserved.
- Undo stack corrupted: "Ctrl+Z stepped the Y field back 1px at a time (240→241→242) instead of undoing the most recent edit".
- Mouse-dragging a vertex does move it and re-renders correctly.

Expected Result:
With vertices lasso-selected in vector edit mode, arrow keys should nudge exactly the selected vertices on canvas, the change should persist after exiting edit mode, and each nudge should be a proper undoable edit.

Estimate: L (5 points) — state/undo consistency issue, needs investigation across the edit pipeline

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_568fa02e-d3c3-4e32-90fc-61aa632eb1ae.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_6fd04e4f-f055-477d-be38-ea177401f2bc.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_c299753c-8735-4f76-88b0-27fc51df84dd.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_e2493adc-63a4-4865-af2b-073139a59f41.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_f2079e04-f0bb-4c9d-ac2f-f60395709b7f.txt`

Agent report (verbatim tail of failing run):

```
The final state is confirmed — the original zigzag is intact. Here's my complete report:

## Task Summary

**What worked:**
1. **Pen tool (P) + draw + commit** ✅ — Pressing P activated the Pen tool; clicking 5 alternating points created the zigzag; Enter/Escape committed it as "Vector 1" (280×100).
2. **Double-click to enter vector edit mode** ✅ — The vector edit toolbar appeared (Move, Lasso, Paint, Bend, Cut, More) with anchor points visible.
3. **Lasso subtool** ✅ — Activated successfully both via the toolbar button and the Q shortcut. Sweeping a freehand loop around the two top peaks drew a visible dashed lasso and selected exactly those two points (solid filled anchors) while the other three stayed unselected (hollow).

**What failed:**
4. **Arrow-key nudge** ❌ — With the two points lasso-selected, pressing ArrowUp did **not** move the selected points:
   - The canvas rendering never changed (verified by pixel-level zoom against the ruler).
   - Instead, the **layer's** Y field in the Design panel decremented 1px per press (250→240 after 10 presses) as if the whole layer were being nudged — while H stayed 100 and nothing moved on canvas.
   - On exiting vector edit mode (tried both Escape and Enter-commit), even that Y change was reverted to 250; the exported SVG path (`M1 101L71 1M71 1L141 101M141 101L211 1M211 1L281 101`) confirmed the geometry was completely unchanged.
   - Retried with the Move subtool active (selection preserved from the lasso) — same failure.
   - The phantom nudges also polluted the undo stack: Ctrl+Z stepped the Y field back 1px at a time (240→241→242) instead of undoing the most recent edit, confirming history/render desync.
   - Diagnostic: dragging a vertex with the mouse **does** move it and re-renders correctly, so the bug is specific to arrow-key nudging of vertex selections. (I used this to restore the zigzag to its original state afterward.)

Steps 1–3 went smoothly, but the final required operation — nudging the lasso-selected points upward with the arrow keys — is broken in this app: the selected points never move, the keypress mutates the layer position field instead (discarded on exit), and the undo history becomes inconsistent.

verdict: not-approve
```
