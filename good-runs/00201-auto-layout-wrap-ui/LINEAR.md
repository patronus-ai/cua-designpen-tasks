# DesignPen [auto layout]: 'auto layout wrap' fails QA — 3/5 runs report broken workflow (00201-auto-layout-wrap-ui)

Description:
Turning on Wrap in the auto-layout Flow controls is undermined by two app bugs. First, the right Design panel renders wider than the 1280px viewport, so the Wrap button is completely cut off-screen and only reachable by programmatically scrolling the panel horizontally; the gap-input labels also render overlapping/overflowing (displayed as "HoriVertigal gap"), making values unreadable. Second, a mid-task crash occurred: while clicking the width input, the tab unexpectedly navigated to `about:blank`, forcing a reload (the document was restored from a snapshot with no data loss). The wrap feature itself works once reached — `flex-wrap: wrap` is applied and rectangles visibly wrap.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Create a narrow frame about 220 wide.
3. Draw six small 60x24 rectangles inside the frame.
4. Select the frame and enable horizontal auto layout via Layout > Flow.
5. Click the frame width input (this is where the tab crashed to `about:blank` mid-task).
6. In the Flow controls, locate the Wrap button — note it is clipped off-screen at the panel's right edge and requires programmatic horizontal panel scrolling to reach; click it to turn Wrap on.

Actual Result:

- Mid-task crash/blank page: while clicking the width input, the tab unexpectedly went to `about:blank`; the app had to be re-navigated, after which the document reloaded from a snapshot (with no data loss).
- Right-panel clipping bug: the Design panel renders wider than the viewport, so the Wrap button was completely cut off-screen and only reachable by programmatically scrolling the panel horizontally.
- Gap-input labels render overlapping/overflowing ("HoriVertigal gap"), making values unreadable.
- The wrap itself did apply once the button was reached (`flex-wrap: wrap`, six rectangles wrapped into two rows of three).

Expected Result:
The Wrap button and gap fields in the Flow controls should be visible and clickable within the 1280x720 viewport without programmatic panel scrolling, labels should render legibly, and interacting with the width input should not crash the tab to `about:blank`.

Estimate: L (5 points) — state/undo consistency issue, needs investigation across the edit pipeline

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 3 of 5 completed runs failed (2 approved)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_0dd64888-475e-4871-9919-2331e2b57140.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_25ca95cf-76a3-4357-b25d-ced5faa8b671.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_8d5ea036-1f88-4e02-9136-e05384cb5a69.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_a9623930-7063-4cd1-bd42-c69c4c6681bf.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_dbc1b81c-b16c-4e3b-aecf-c34119e42f66.txt`

Agent report (verbatim tail of failing run):

```
The task is complete. Final state verified:

1. **Narrow frame (~220 wide)** ✓ — "Frame 1" is 220 × 100 (confirmed by the canvas size label and the W field showing 220; code inspect shows `width: 220px`).
2. **Six small 60×24 rectangles** ✓ — Rectangle 1–6 are children of Frame 1 in the Layers panel; spot-checked Rectangle 1 at exactly 60 × 24.
3. **Horizontal auto layout (Layout > Flow)** ✓ — the horizontal (→) Flow button is active, the Auto layout section appeared, and code inspect shows `display: flex`.
4. **Wrap ON in Flow controls** ✓ — the wrap toggle in the Flow row is highlighted, code inspect confirms `flex-wrap: wrap`, and the six rectangles visibly wrap into two rows of three inside the 220-wide frame (I also normalized padding/gaps to 10 so the wrap is clearly visible).

However, the session wasn't problem-free. Issues encountered:
- **Mid-task crash/blank page**: while clicking the width input, the tab unexpectedly went to `about:blank`; I had to re-navigate, after which the document reloaded from a snapshot (fortunately with no data loss).
- **Right-panel clipping bug**: the Design panel renders wider than the viewport, so the Wrap button was completely cut off-screen and only reachable by programmatically scrolling the panel horizontally; gap-input labels also render overlapping/overflowing ("HoriVertigal gap"), making values unreadable.

The end result is correct and verified, but because of the crash and UI rendering bugs hit along the way:

verdict: not-approve
```
