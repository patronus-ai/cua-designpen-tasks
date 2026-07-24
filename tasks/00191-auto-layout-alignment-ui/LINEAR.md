# DesignPen [auto layout]: 'auto layout alignment' fails QA — 4/5 runs report broken workflow (00191-auto-layout-alignment-ui)

Description:
The auto-layout alignment 3x3 grid in the Design panel (Layout > Flow) does not work as a standalone control. When auto layout is enabled on a frame, the app auto-infers asymmetric padding from the children's original top-left positions (e.g. top 20, right 120, bottom 240, left 20), which consumes all free space inside the frame. Clicking the bottom-right alignment cell registers (the cell highlights) but has no visible effect on the canvas — the child stack stays pinned at the top-left. Additionally, enabling auto layout silently switches the frame to hug-contents sizing, so manually zeroing the padding shrinks the frame (300x300 to 180x60), requiring the user to re-enter W/H to restore its size.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Create a frame about 300x300 on the canvas.
3. Draw three 40x40 squares inside the frame (positioned near the top-left).
4. Select the frame and enable auto layout via Design panel > Layout > Flow (horizontal).
5. Observe the auto-inferred padding values in the Auto layout section.
6. In the auto-layout alignment 3x3 grid, click the bottom-right cell.

Actual Result:

- The bottom-right alignment cell highlights (click registers) but the change has no visible effect: the stack of squares stays pinned at the frame's top-left because the auto-inferred asymmetric padding (top 20, right 120, bottom 240, left 20) consumed all free space.
- To make the stack actually tuck into the bottom-right corner, the right and bottom padding had to be manually zeroed.
- Zeroing the padding exposed a second bug: the frame had silently switched to hug-contents sizing, shrinking from 300x300 to 180x60; W=300 and H=300 had to be re-entered to restore the frame's size.
- The end result was only achievable via these padding/dimension workarounds; the alignment click alone did not produce the expected behavior.

Expected Result:
Clicking the bottom-right cell of the auto-layout alignment grid should move the child stack flush into the frame's bottom-right corner, without the frame's auto-inferred padding blocking the alignment and without the frame silently switching to hug-contents sizing and losing its 300x300 dimensions.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 4 of 5 completed runs failed (1 approved)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_06c7bce1-19eb-4552-8ede-9171a221ccd3.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_55612697-91b4-4178-a2c3-016585b4a559.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_72331cee-adb0-4b9f-810a-50e29caa335b.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_aaa112a4-d482-467b-a702-872bb1eaa459.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_c910ddf4-fec1-43b3-8763-11759b2b057c.txt`

Agent report (verbatim tail of failing run):

```
The task is now complete. Final state achieved:

- **Frame 1**: 300×300 frame on the canvas
- **Contents**: three 40×40 rectangles (Rectangle 1/2/3) as children of the frame
- **Auto layout**: enabled via Design panel > Layout > Flow (horizontal →)
- **Alignment**: bottom-right cell of the 3×3 grid selected, and the stack of three squares sits flush in the frame's bottom-right corner (first square at X140/Y260, ending exactly at 300/300)

**How it went:** I did hit problems along the way. When I enabled auto layout, the app auto-inferred asymmetric padding (top 20, right 120, bottom 240, left 20) from the squares' original top-left positions. As a result, clicking the bottom-right alignment cell registered (the cell highlighted) but had **no visible effect** — the stack stayed pinned at the top-left because the padding consumed all free space. To get the stack to actually tuck into the bottom-right corner, I had to manually zero the right and bottom padding. Doing so exposed a second quirk: the frame had silently switched to hug-contents sizing, so it shrank from 300×300 to 180×60, and I had to re-enter W=300 and H=300 to restore the frame's size. Only after these workarounds did the alignment behave as described in the task.

The end result is correct, but the alignment click alone did not produce the expected "tuck into the corner" behavior and required padding/dimension workarounds.

verdict: not-approve
```
