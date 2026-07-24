# DesignPen [grid layout]: 'grid layout enable' fails QA — 4/5 runs report broken workflow (00211-grid-layout-enable-ui)

Description:
Enabling Grid layout on a frame (Design panel > Layout > Flow, 4th "Grid" button) applies visually but is not persisted. Mid-task the page unexpectedly navigated to `about:blank`; after reloading (document restored as "snapshot"), the child squares kept their grid-snapped positions but the frame's Flow had reverted from Grid back to Freeform, so the Grid layout had to be re-applied. In addition, when a frame is selected — especially once Grid flow options appear — the right Design panel content overflows horizontally and gets clipped, hiding left-side labels/controls ("Layout", "Clip content", the X-position field; grid track labels show as "Fl..."). The Code panel also reports `display: inline-flex` for a grid frame instead of grid CSS.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Draw a frame (e.g. 400x400) with the frame tool.
3. Add four small 60x60 squares inside the frame with the rectangle tool.
4. Select the frame via the Layers panel.
5. In Design panel > Layout > Flow, click the Grid (4th) button — observe the panel clipping and that the squares reflow into a 2x2 grid.
6. Wait for / trigger the mid-task navigation to `about:blank`, then reload the app (document restores as "snapshot").
7. Re-select the frame and check its Flow setting.

Actual Result:

- Grid setting lost after reload: after the page unexpectedly navigated to `about:blank` and the app was reloaded (document restored as "snapshot"), the squares kept their grid-snapped positions but the frame's Flow had reverted from Grid back to Freeform (confirmed by both the layer icon and the panel) — the grid layout property was not persisted and had to be re-applied a second time.
- Design panel overflow/clipping bug: when a frame is selected, and especially once Grid flow options appear, the right Design panel content overflows horizontally and gets clipped, hiding left-side labels/controls ("Layout", "Clip content", the X-position field; grid track labels show as "Fl..."), requiring zoom and accessibility refs to operate it.
- Minor: the Code panel reports `display: inline-flex` for the grid frame instead of grid CSS.

Expected Result:
Switching a frame to Grid layout should persist across reload/snapshot restore, the Design panel should render its Layout/Grid controls without horizontal overflow or clipping, and the Code panel should report grid CSS for a grid frame.

Estimate: S (2 points) — small handler/layout fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 4 of 5 completed runs failed (1 approved)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_16515eef-4e37-465f-94e6-aa56d2bf8f8d.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_2febbe69-75ad-4947-b399-9306d48910c6.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_5209830e-412a-480d-ac0d-37464fa86a84.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_76b26b4e-2b27-4d36-95d8-df107ea19896.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_8b580f82-dca9-4872-8438-924eff94c254.txt`

Agent report (verbatim tail of failing run):

```
The final state is confirmed:

- **Frame 1** (400×400) exists and is selected, containing four 60×60 squares (Rectangle 1–4) as children
- The frame's layer icon shows the grid symbol, the **Grid** option in Design panel > Layout > Flow is active (highlighted blue), and grid track controls (Columns C1/C2, Rows R1/R2, each 1fr) are present
- The four squares are laid out in the 2×2 grid cells on canvas

**Summary of what I did:** Drew a 400×400 frame with the frame tool, added four 60×60 rectangles inside it with the rectangle tool, selected the frame via the Layers panel, and clicked the Grid (4th) button in Design panel > Layout > Flow. The grid applied correctly, reflowing the squares into a 2×2 grid.

**Problems encountered:**
1. **Design panel overflow/clipping bug:** When a frame is selected — and especially once Grid flow options appear — the right Design panel content overflows horizontally and gets clipped, hiding left-side labels/controls ("Layout", "Clip content", the X-position field, grid track labels show as "Fl..."). I had to use zoom and accessibility refs to operate it.
2. **Grid setting lost after reload:** Mid-task the page unexpectedly navigated to about:blank; after reloading the app (document restored as "snapshot"), the squares kept their grid-snapped positions but the frame's Flow had reverted from Grid back to Freeform (layer icon and panel both confirmed it). This indicates the grid layout property wasn't persisted, and I had to re-apply Grid flow a second time.
3. Minor: the Code panel reports `display: inline-flex` for the grid frame instead of grid CSS.

The task goal was ultimately achieved, but due to the persistence loss, unexpected blank-page navigation, and the clipped Design panel, it did not go smoothly.

verdict: not-approve
```
