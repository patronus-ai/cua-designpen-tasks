# DesignPen [auto layout]: 'auto layout cross gap' fails QA — 4/4 runs report broken workflow (00192-auto-layout-cross-gap-ui)

Description:
Setting the cross-axis (vertical) gap on a wrapped auto-layout frame is broken along multiple fronts in the Design panel's Flow controls. The right-hand properties panel is clipped at the 1280px viewport so the Wrap button is completely hidden off-screen (reachable only via programmatic DOM horizontal scrolling), and the Horizontal/Vertical gap input fields never display their committed values — they keep showing overlapping placeholder text. Worse, a single click on the Vertical gap field navigated the app to `about:blank` (page crash). The generated CSS in the Code tab also omits `row-gap`/`gap`, so the applied gap can only be verified through canvas geometry, not through any UI readout. Enabling auto layout additionally silently resized the frame (300 to 460 wide) and produced odd auto-derived paddings (150/86).

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Create a frame about 300 wide.
3. Draw five small 60x24 "chip" rectangles inside the frame.
4. Select the frame and enable horizontal auto layout via Layout > Flow.
5. Observe that the frame is silently resized (300 to 460 wide) with odd auto-derived paddings (150/86); reset width to 300 and paddings to 10 if needed.
6. In the Flow controls, locate the Wrap button — note it is clipped off-screen and requires horizontally scrolling the panel via DOM scrolling; click it to turn Wrap on.
7. Click the Vertical (cross-axis) gap field and enter 40.

Actual Result:

- Clicking the Vertical gap field once caused the app to navigate to `about:blank` (page crash); after reloading, the document was preserved (renamed "snapshot").
- The right-hand properties panel is clipped at the 1280px viewport: the Wrap button was completely hidden off-screen and only reachable via programmatic horizontal DOM scrolling; the gap fields render with overlapping placeholder text.
- The Horizontal/Vertical gap input fields never display their committed values (they keep showing placeholders), and the generated CSS in the Code tab omits `row-gap`/`gap` entirely — the applied 40 gap could only be verified through canvas geometry and child positions.
- Enabling auto layout silently resized the frame (300 to 460 wide) and produced odd auto-derived paddings (150/86) that had to be manually reset.

Expected Result:
The Wrap toggle and gap fields should be visible and reachable in the panel at a 1280px viewport, entering 40 in the Vertical gap field should not crash the page, the field should display its committed value, and the Code tab CSS should include the corresponding `row-gap`/`gap`. Enabling auto layout should not silently resize the frame or invent large paddings.

Estimate: L (5 points) — state/undo consistency issue, needs investigation across the edit pipeline

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 4 of 4 completed runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_36d70c06-386d-4145-a21b-e95ea3f51adb.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_4b497bfa-7680-48ee-a8dd-eefd5efe49fa.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_5b6b9d2c-5afb-4c70-91fb-15df9225d8ac.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_78d01223-e917-4277-8ea8-6e4a8132661b.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_b5913437-0003-4608-925f-0d9f91bbb44a.txt`

Agent report (verbatim tail of failing run):

```
The task is complete. Final state verified:

**What was accomplished:**
1. **Frame created** — "Frame 1" at 300 wide (300 × 120), containing five chip rectangles (Rectangle 1–5), each exactly 60 × 24.
2. **Horizontal auto layout enabled** — via Layout > Flow, the "→" (horizontal) flow button is active; Code panel confirms `display: flex`.
3. **Wrap turned on** — the Wrap toggle in the Flow controls is active; Code panel confirms `flex-wrap: wrap`, and the chips visibly wrap (4 chips on row 1, the 5th on row 2).
4. **Cross-axis (vertical) gap set to 40** — confirmed geometrically: Rectangle 5 sits at y = 74 inside the frame (10 top padding + 24 row height + **40 gap**), and row spacing on canvas measures exactly 40.

**Problems encountered along the way:**
- The right-hand properties panel is clipped at this 1280px viewport: the Wrap button was completely hidden off-screen (I had to horizontally scroll the panel via DOM scrolling to find and click it), and the gap fields render with overlapping placeholder text.
- Clicking the Vertical gap field once caused the app to navigate to `about:blank` (page crash); after reloading, the document was preserved (renamed "snapshot").
- The Horizontal/Vertical gap input fields never display their committed values (they keep showing placeholders), and the generated CSS in the Code tab omits `row-gap`/`gap` entirely — the applied 40 gap could only be verified through canvas geometry and child positions, not through the UI fields.
- Enabling auto layout also silently resized the frame (300→460 wide) and produced odd auto-derived paddings (150/86), which I had to manually reset (width back to 300, paddings to 10).

The end result is correct, but the app exhibited several bugs and the workflow was far from smooth.

verdict: not-approve
```
