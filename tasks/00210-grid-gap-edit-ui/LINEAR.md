# DesignPen [grid layout]: 'grid gap edit' fails QA — 3/5 runs report broken workflow (00210-grid-gap-edit-ui)

Description:
Enabling Grid layout on a frame (Design panel > Layout > Flow, 4th "grid" option) breaks the right-hand properties panel rendering: the newly added Grid controls overflow the panel horizontally and the whole panel content shifts/clips at the left edge (labels truncated to "...out", "...nce"; gap fields half-hidden behind the canvas). Browser zoom does not fix it — proper rendering was only recovered by programmatically scrolling an element into view, meaning a normal user would likely be stuck with an unreadable panel. The gap fields themselves work (values persist after re-select), but they are icon-only with no text labels or tooltips and their "Gap" label area is clipped, so distinguishing column gap vs. row gap vs. padding required empirical testing via the Inspect panel's box model.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Create a frame (e.g. 400x300) with the Frame tool.
3. With the frame selected, in the right panel's Layout section click the 4th Flow option (grid icon) to enable Grid layout.
4. Observe the right-hand properties panel rendering immediately after Grid is enabled.
5. In the Grid controls, set the column gap field (horizontal gap icon) to 20 and the row gap field (vertical gap icon) to 12.

Actual Result:

- Immediately after enabling Grid flow, the right-hand properties panel broke visually: the Grid controls overflowed the panel horizontally and the whole panel content shifted/clipped on the left edge (labels truncated to "...out", "...nce"; gap fields half-hidden behind the canvas). Browser zoom did not fix it; proper rendering was only recovered by programmatically scrolling an element into view.
- The gap fields have no text labels or tooltips (icon-only, and the "Gap" label area was clipped), so which field was column gap vs. row gap vs. padding had to be determined empirically by testing a value and checking the Inspect panel's box model.
- The Grid option button in the Flow row is partially clipped off the right edge of the panel even in the normal state.
- The gap values themselves did apply and persisted after re-selecting the frame.

Expected Result:
Enabling Grid layout should not break the properties panel layout; the Grid gap controls should render fully within the panel with readable labels (or tooltips) so the column-gap and row-gap fields are identifiable and editable without workarounds.

Estimate: S (2 points) — small handler/layout fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 3 of 5 completed runs failed (2 approved)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_115e111d-94b9-4154-95bf-08d8c436c296.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_168be03b-99de-4369-a05c-6f53d0bc99fd.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_40d21062-1e6e-47c2-abf5-34ca58285e77.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_6a806456-7003-4238-b936-8ac1e4212a9e.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_969d1ae9-eff0-484b-8f33-042e752127ad.txt`

Agent report (verbatim tail of failing run):

```
All steps are complete and verified. Here's a summary of what was done:

**Task execution:**
1. **Created a frame** — Selected the Frame tool and drew "Frame 1" (400×300) on the canvas.
2. **Enabled Grid layout via Layout > Flow** — In the right panel's Layout section, clicked the 4th Flow option (grid icon); the frame became a grid with Columns (C1: 1fr, C2: 1fr) and Rows (R1: 1fr).
3. **Set gaps in the Grid controls** — Set the column gap field (⟷ horizontal gap icon) to **20** and the row gap field (↕ vertical gap icon) to **12**. Both values persisted after re-selecting the frame, and I verified the gap fields are distinct from the padding fields below them (confirmed via the Code/Inspect box-model test, then reverted the test padding to 0).

**Problems encountered:**
- Immediately after enabling Grid flow, the right-hand properties panel broke visually: the newly added Grid controls overflowed the panel horizontally and the whole panel content shifted/clipped on the left edge (labels truncated to "...out", "...nce"; gap fields half-hidden behind the canvas). Browser zoom didn't fix it; I only recovered proper rendering by programmatically scrolling an element into view. A normal user would likely be stuck with an unreadable panel.
- The gap fields have no text labels or tooltips (icon-only, and the "Gap" label area was clipped), so I had to empirically determine which field was column gap vs. row gap vs. padding by testing a value and checking the Inspect panel's box model.
- Minor: the Grid option button in the Flow row is partially clipped off the right edge of the panel even in the normal state.

The requested end state was achieved (frame with Grid layout, column gap = 20, row gap = 12), but the panel-clipping rendering bug after enabling Grid was a genuine usability problem requiring workarounds.

verdict: not-approve
```
