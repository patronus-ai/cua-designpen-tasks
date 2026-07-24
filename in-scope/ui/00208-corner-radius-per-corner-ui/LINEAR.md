# DesignPen [general UI]: 'corner radius per corner' fails QA — 4/4 runs report broken workflow (00208-corner-radius-per-corner-ui)

Description:
The per-corner radius feature itself works — the "Independent corner radii" toggle in the Appearance section shows the 2x2 corners grid and the values apply and render correctly — but the app crashes while using it. Immediately after the first click on the top-left corner input, the tab unexpectedly navigated to `about:blank` (blank page), forcing a reload of the app; state persisted only because the project was restored under the name "snapshot". There is also a cosmetic bug where the right panel's content overflows/scrolls horizontally after toggling independent corners, requiring the user to scroll it back into view.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Draw a rectangle on the canvas (e.g. 250x170).
3. In the Appearance section of the Design panel, click the "Independent corner radii" toggle (the 2x2 corners grid appears).
4. Click the top-left corner input in the corners grid — the tab crashes to `about:blank` on the first click.
5. Reload the app, re-select the rectangle, and set top-left radius to 24 and bottom-right radius to 8, leaving top-right and bottom-left at 0.

Actual Result:

- Immediately after the first click on the top-left corner input, the tab unexpectedly went blank (navigated to `about:blank`), forcing a reload of the app. State persisted across the reload (the rectangle and the enabled independent-corners toggle survived, with the project reappearing under the name "snapshot").
- After the reload, the corner values could be set and rendered correctly (top-left 24, bottom-right 8, others 0).
- Minor cosmetic issue: the right panel's content overflowed/scrolled horizontally after toggling independent corners and had to be scrolled back into view.

Expected Result:
Clicking a corner-radius input in the corners grid should focus the field and accept a value without crashing the tab to `about:blank`, and toggling independent corners should not cause the right panel content to overflow horizontally.

Estimate: L (5 points) — state/undo consistency issue, needs investigation across the edit pipeline

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 4 of 4 completed runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_0a1cd1d1-67d0-4e83-96fe-bec73b83162a.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_2784480c-6b03-4c95-8686-d92867a65a65.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_38cf3635-b907-43d4-b382-95a8eddac23c.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_8d396471-9595-4216-8f81-c1fc9cb56a69.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_ccc07798-5fdf-44c1-9a3f-d55eb38bf5f1.txt`

Agent report (verbatim tail of failing run):

```
All four corners verified on canvas: top-left has a large rounded corner (24), top-right and bottom-left are sharp (0), and bottom-right has a small rounded corner (8). The task steps are complete:

1. ✅ **Rectangle drawn** — a 250 × 170 rectangle ("Rectangle 1") on the canvas
2. ✅ **Independent corners enabled** — clicked the "Independent corner radii" toggle in the Appearance section (icon turned blue and the 2×2 corners grid appeared)
3. ✅ **Corner values set** — top-left = 24, top-right = 0, bottom-left = 0, bottom-right = 8, all confirmed both in the panel inputs and visually on the canvas rendering

**Summary of how it went:** The core feature flow itself worked correctly — the toggle exists in the Appearance section, the corners grid appeared, and the values applied and rendered properly. However, I did hit one anomaly mid-task: immediately after my first click on the top-left corner input, the tab unexpectedly went blank (navigated to about:blank), forcing me to reload the app. Fortunately all state persisted (the rectangle and the enabled independent-corners toggle survived, with the project reappearing under the name "snapshot"), and I was able to re-select the rectangle and complete and verify everything successfully. There was also a minor cosmetic issue where the right panel's content overflowed/scrolled horizontally after toggling independent corners, which I had to scroll back into view.

Because of that unexpected mid-task page blank requiring a reload, the session did not go entirely smoothly, even though the end result is fully correct.

verdict: not-approve
```
