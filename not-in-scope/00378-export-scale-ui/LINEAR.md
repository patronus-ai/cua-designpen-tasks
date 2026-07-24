# DesignPen [export]: 'export scale' fails QA — 5/5 runs report broken workflow (00378-export-scale-ui)

Description:
In the right-hand properties panel's Export section, the export scale preset dropdown button is almost entirely hidden underneath the format (PNG) dropdown at the 1280x720 viewport — the panel renders extremely cramped, only ~3px of the preset button is visible, and clicking it by element reference opens the wrong (format) menu. Related fallout: pressing Escape to close the wrong menu deselects the shape, and a Tab+Enter keyboard workaround unexpectedly triggered vector edit mode, converting the rectangle to a VECTOR and dropping the export setting (recovered via Ctrl+Z). The scale could ultimately be set to 2x only by clicking the tiny visible sliver of the preset button.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Draw a small 32 by 32 square with the rectangle tool (canvas badge shows "32 × 32").
3. With the square selected, click the "+" in the Export section of the properties panel to add an export setting (a PNG format row with Export button and preview appears).
4. Try to open the export scale input's preset dropdown (0.5x / 0.75x / 1x / 1.5x / 2x / 3x / 4x) and select "2x".

Actual Result:

- The scale preset dropdown button is almost entirely hidden underneath the format (PNG) dropdown because the properties panel renders extremely cramped at this viewport width; clicking the preset button by element reference opened the wrong (format) menu, and only ~3px of the preset button was visible to click.
- Pressing Escape to close the wrong menu deselected the shape.
- A Tab+Enter keyboard workaround unexpectedly triggered vector edit mode, converting the rectangle to a VECTOR and dropping the export setting; Ctrl+Z was needed to recover.
- Setting the scale to 2x succeeded only by clicking the tiny visible sliver of the preset button (checkmark then moved from 1x to 2x).

Expected Result:
The export scale preset dropdown should be fully visible and clickable next to the format dropdown, so selecting a 2x preset works with a normal click.

Estimate: S (2 points) — small handler/layout fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 completed runs failed (`verdict: not-approve`)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_638c11aa-5371-45b6-9265-b161c2917ffa.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_65e58b1f-8768-4687-9d6b-88929ebefc26.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_8d9a2dd8-43fd-4528-8647-bde146460829.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_b72c0375-54a5-4bd6-82bf-c846d1ab428b.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_d5b85194-c1bf-4799-8cd2-00777b2d78ac.txt`

Agent report (verbatim tail of failing run):

```
The task is now complete. Final state verified:

1. **32×32 square drawn** — "Rectangle 1" created on the canvas with W=32, H=32 (canvas badge showed "32 × 32")
2. **Selected** — selection handles visible, layer highlighted, properties panel showing the rectangle
3. **Export setting added** — via the "+" in the Export section (PNG format row with Export button and preview appeared)
4. **Scale set to 2x via the preset** — opened the scale input's preset dropdown (0.5x / 0.75x / 1x / 1.5x / 2x / 3x / 4x) and clicked "2x"; reopening the menu confirmed the checkmark moved from 1x to 2x

**Issues encountered along the way:** The right-hand properties panel renders extremely cramped at this viewport width, causing a UI bug where the export scale's preset dropdown button is almost entirely hidden underneath the format (PNG) dropdown — clicking it by element reference opened the wrong (format) menu, and only ~3px of the preset button was visible to click. Additionally, pressing Escape to close the wrong menu deselected the shape, and an attempted keyboard workaround (Tab+Enter) unexpectedly triggered vector edit mode, converting the rectangle to a VECTOR and dropping the export setting — I had to undo (Ctrl+Z) to recover. I ultimately completed all steps successfully by clicking the tiny visible sliver of the preset button, but the overlapping/clipped export controls are a genuine UI bug that nearly blocked the task.

verdict: not-approve
```
