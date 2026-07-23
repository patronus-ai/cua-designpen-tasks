# DesignPen [strokes]: 'stroke per side weight' fails QA — 3/4 runs report broken workflow (00281-stroke-per-side-weight-ui)

Description:
Selecting "Custom" from the "Stroke sides" menu in the right-hand Design panel causes the panel content to overflow and auto-scroll horizontally, clipping the left column of controls — including the Top and Bottom per-side weight inputs, which end up hidden behind the canvas edge and not clickable. The panel had to be scrolled back programmatically (scroll_to an element) to reveal the full 2x2 per-side weight grid before values could be entered; even after that, the "Stroke sides" button remains partially cut off at the panel's right edge in Custom mode. The per-side weight feature itself works once the controls are reachable (values apply and render as graduated border thicknesses), so this is a layout overflow bug in the stroke section.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Draw a rectangle on the canvas using the rectangle tool.
3. Click "+" in the Stroke section of the Design panel to add a border (black inside stroke).
4. Click the "Stroke sides" button and select "Custom" from the menu (All/Top/Bottom/Left/Right/Custom).
5. Observe the Design panel layout immediately after selecting Custom.
6. Attempt to click the Top and Bottom inputs in the 2x2 per-side weight grid and enter top 1, right 2, bottom 3, left 4.

Actual Result:

- Immediately after selecting "Custom", the right-hand Design panel's content overflows and auto-scrolls horizontally, clipping the left column of controls; the Top and Bottom per-side weight inputs are hidden behind the canvas edge and not clickable.
- The panel had to be scrolled back programmatically (scroll_to an element) to reveal the full grid before the values could be entered.
- Even after that, the "Stroke sides" button remains partially cut off at the panel's right edge in Custom mode.
- Once reachable, the inputs work: Top 1 / Right 2 / Bottom 3 / Left 4 were confirmed in the panel and the rectangle renders with graduated border thicknesses.

Expected Result:
Choosing "Custom" in the stroke side menu should display the full per-side weight grid within the panel without horizontal overflow, auto-scrolling, or clipped controls, so all four side inputs and the "Stroke sides" button are visible and clickable.

Estimate: M (3 points) — scoped feature fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 3 of 4 completed runs failed (1 approved)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_64b1f4c2-13c4-4fd6-8514-568c5c7a8871.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_8e03db1a-b316-4bd0-b89c-f1ea4c03beae.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_d36a3cf1-55de-4bc7-b189-312f1135c4fd.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_e54f6ea0-3661-4258-8c63-fb285c0cf630.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_e82b36b6-efcd-4d44-87ed-2d6e5c6e2b41.txt`

Agent report (verbatim tail of failing run):

```
All steps of the task were completed:

1. **Drew a rectangle** — created a 300×200 rectangle on the canvas using the rectangle tool.
2. **Added a border** — clicked "+" in the Stroke section, which added a black inside stroke.
3. **Opened the stroke side menu and chose Custom** — clicked the "Stroke sides" button and selected "Custom" from the menu (All/Top/Bottom/Left/Right/Custom).
4. **Entered per-side weights** — in the 2×2 per-side weight grid: Top = 1, Right = 2, Bottom = 3, Left = 4. The values are confirmed in the panel, and the canvas rectangle visibly renders with graduated border thicknesses (thin top, thicker right, thicker bottom, thickest left).

However, I did hit a UI bug along the way: immediately after selecting "Custom", the right-hand Design panel's content overflowed and auto-scrolled horizontally, clipping the left column of controls — including the Top and Bottom per-side weight inputs, which were hidden behind the canvas edge and not clickable. I had to programmatically scroll the panel back (scroll_to an element) to reveal the full grid before I could enter the values. Even after that, the "Stroke sides" button remains partially cut off at the panel's right edge in Custom mode, confirming a layout overflow issue in the stroke section. The feature itself works, but the panel layout glitch required a workaround.

verdict: not-approve
```
