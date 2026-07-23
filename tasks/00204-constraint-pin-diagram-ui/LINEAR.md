# DesignPen [constraints]: 'constraint pin diagram' fails QA — 5/5 runs report broken workflow (00204-constraint-pin-diagram-ui)

Description:
The constraint pin diagram in the Design panel's Position/Constraints section is not interactive: this build of OpenPencil has no clickable pin-diagram widget. The only pin diagram present is a tiny crosshair icon that acts solely as an open/close toggle for the Constraints section — clicking any part of it, including the right-pin segment, just toggles the section — and otherwise only displays pin state. Right/Bottom constraints can only be set via the two Constraints dropdowns. Additional quirks: the right properties panel is clipped at the 1280px viewport (some controls hidden unless the panel is scrolled horizontally), and double-clicking an already-selected ellipse silently enters vector-edit mode and converts it to a Vector node.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Create a frame (e.g. 300x400).
3. Draw a small circle (~48x48) in the frame's bottom-right area (a floating-action-button mock).
4. Select the circle (single click; note that double-clicking an already-selected ellipse silently converts it to a Vector node).
5. In the Design panel Position section, click the pin toggle to open the constraints controls.
6. Attempt to click the right pin and the bottom pin in the constraint pin diagram (the crosshair icon).

Actual Result:

- Clicking the pin diagram (crosshair icon) does not set constraints: clicking any part of it, including the right-pin segment, just toggles the Constraints section open/closed. The diagram is display-only for pin state; there is no clickable pin-diagram widget anywhere in the UI (verified via full accessibility tree including off-screen elements, horizontal panel scrolling, hover popovers, canvas hit-testing, and menus).
- Right/Bottom constraints had to be set via the two Constraints dropdowns instead.
- The right properties panel is clipped at the 1280px viewport; some controls are hidden unless the panel is scrolled horizontally.
- Double-clicking the already-selected ellipse silently entered vector-edit mode and converted it to a Vector node, requiring the ellipse to be deleted and recreated.

Expected Result:
The constraint pin diagram should be an interactive widget where clicking the right and bottom pins sets the selected node's constraints to Right and Bottom, matching the documented workflow, without requiring the dropdown workaround.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 completed runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_0eb54bb4-b5ba-46ff-ab0e-39e481562ff6.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_81937cbf-c6b3-48af-9386-ca7607f035e2.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_97aafd16-2d56-4af5-ac23-5b0c1505b239.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_98e8ebf2-4446-453d-bd73-61f66be5bfb4.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_dc0a0bdb-76f5-4ee6-aafd-1e1b41627f05.txt`

Agent report (verbatim tail of failing run):

```
The final state is fully verified:

- **Frame 1** (300 × 400) exists on the page
- **Ellipse 1** — a 48 × 48 circle — sits in the frame's bottom-right area (32px from the right edge, 32px from the bottom edge; confirmed by the Inspect tab's "distance to parent right: 32 / bottom: 32"), making a proper floating-action-button mock
- With the circle selected, I opened the constraints controls via the **pin toggle** in the Position section
- The constraints are now **Right** and **Bottom** — the pin/crosshair indicator shows the right and bottom pins highlighted blue, and the canvas shows the dashed constraint stubs on the circle's right and bottom sides

**Summary of how it went:** Creating the frame and circle worked fine, and the Position-section pin toggle did open the Constraints controls. However, the specific interaction described — clicking right/bottom pins inside a "constraint pin diagram" — was not possible as described: this build of OpenPencil has **no clickable pin-diagram widget**. The only pin diagram is the tiny crosshair icon, which acts solely as an open/close toggle for the section (clicking any part of it, including the right-pin segment, just toggles the section) and otherwise only *displays* pin state. I verified this thoroughly (full accessibility tree including off-screen elements, horizontal panel scrolling, hover popovers, canvas hit-testing, menus). I achieved the requested end state by selecting "Right" and "Bottom" in the two Constraints dropdowns instead. Two further annoyances: the right properties panel is clipped at the 1280px viewport (some controls hidden unless the panel is scrolled horizontally), and double-clicking the already-selected ellipse silently entered vector-edit mode and converted it to a Vector node (I recovered by deleting and recreating the ellipse cleanly).

Because the literal "click the right and bottom pins in the constraint pin diagram" interaction doesn't exist in this UI and I had to use the dropdown equivalents, plus the panel-clipping and vector-conversion quirks encountered along the way:

verdict: not-approve
```
