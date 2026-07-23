# DesignPen [variables]: 'variable create number' fails QA — 5/5 runs report broken workflow (00348-variable-create-number-ui)

Description:
The unified "Corner radius" field's variable affordance in the right Design panel is unusable for binding a number variable. Its "Apply variable" diamond only appears while the number input is focused, and the resulting variable-picker popup closes on any mousedown (the input blurs before the click registers), so clicking a variable option never applies. Keyboard input also goes to the number input instead of the popup list (Down-arrow decrements the value, Enter commits a number), which accidentally mutates the radius. Binding a FLOAT variable like "radius-lg" only works via the workaround of toggling "Independent corner radii" mode, where each corner field has a persistent, working diamond. Additionally, the canvas fails to visually re-render manually entered radius values even though the model updates.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Open the Local variables dialog from the left panel Variables tab.
3. Create a collection ("New collection").
4. Use the "+ Add" menu > Number to create a FLOAT variable named "radius-lg" with value 24; close the dialog.
5. Draw a rectangle on the canvas (e.g. 200x150) and keep it selected.
6. Focus the unified "Corner radius" number field in the Design panel so its "Apply variable" diamond appears.
7. Click the diamond to open the variable-picker popup, then click the "radius-lg" option.
8. Alternatively, with the popup open, try keyboard navigation (Down-arrow, Enter) to select "radius-lg".

Actual Result:

- The variable-picker popup closes on any mousedown because the number input blurs before the click registers — clicking the "radius-lg" option never applies the binding.
- Keyboard keys go to the number input instead of the popup list: Down-arrow decremented the value and Enter committed a number, accidentally changing the radius to 9 during attempts.
- The "Apply variable" diamond on the unified field only appears while the input is focused, making the popup effectively unreachable.
- The canvas failed to visually re-render manually entered radius values even though the model updated.
- Binding succeeded only via a workaround: toggling "Independent corner radii" mode and binding "radius-lg" to each of the four corner fields individually, which have persistent working diamonds.

Expected Result:
The unified Corner radius field's "Apply variable" popup should stay open long enough to accept a mouse selection (and support keyboard selection), and choosing "radius-lg" should bind the radius to the variable and re-render the canvas immediately.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 completed runs failed (`verdict: not-approve`)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_33c2472c-0fed-4a7c-a074-37aec967b304.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_45e6eea5-1baa-4a5f-b72a-819040b21bd8.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_652d66cc-4c00-4348-9000-f266303774c9.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_8befa822-55de-469a-85d3-09c7603573d9.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_b5230788-dc21-4c1d-b813-d9673d646aba.txt`

Agent report (verbatim tail of failing run):

```
All four corners of the rectangle are visibly rounded with the 24px radius from the bound variable. The task's end state is fully achieved:

1. ✅ Opened the Local variables dialog from the left panel Variables tab
2. ✅ Created a collection ("New collection")
3. ✅ Used the + Add menu → Number to create a FLOAT variable "radius-lg" with value 24 (verified in the dialog)
4. ✅ Drew a rectangle (Rectangle 1, 200×150)
5. ✅ Bound its corner radius to the "radius-lg" token — all four corner fields show "24" with highlighted variable diamonds, the Code inspector confirms `border-radius: 24px` with "Modes: New collection / Auto (Mode 1)", and the canvas renders the rounding

However, I hit a genuine bug along the way: the **unified** "Corner radius" field's variable affordance is broken. Its "Apply variable" diamond only appears while the number input is focused, and the resulting variable-picker popup closes on any mousedown (the input blurs before the click registers), so clicking the "radius-lg" option never applies; keyboard keys also go to the number input instead of the popup list (Down-arrow decremented the value, Enter committed a number), making the popup completely unusable and accidentally changing the radius to 9 during attempts. The canvas also failed to visually re-render those manually-entered radius values even though the model updated. I could only complete the binding by toggling "Independent corner radii" mode, where each of the four corner fields has a persistent, working diamond affordance, and binding "radius-lg" to each corner individually.

The goal was reached, but only via a workaround because the primary unified radius field's variable picker is broken (popup closes before a selection can register and is keyboard-inaccessible), plus a canvas re-render lag for manual radius edits.

verdict: not-approve
```
