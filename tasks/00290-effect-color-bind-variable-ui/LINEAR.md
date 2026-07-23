# DesignPen [fills & color]: 'effect color bind variable' fails QA — 5/5 runs report broken workflow (00290-effect-color-bind-variable-ui)

Description:
The hex text input inside the color-picker popover (opened from a variable's swatch in the Variables panel) refuses keyboard focus: clicking it leaves focus on the trigger button, so a user cannot type a hex value such as FF0000. The agent reproduced this multiple times, while other inputs (the modal's search field, inline rename) accept click-focus normally, and could only proceed by setting the input's value programmatically. The rest of the workflow — Effects "+" to add a drop shadow, the variable affordance (diamond "+" icon) on the effect color row, and the variable picker — worked correctly and the shadow rendered red once the variable value was set.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Open the Variables panel and create a new collection with a color variable; rename it "Red".
3. Click the variable's color swatch to open the color-picker popover.
4. Click the hex text input inside the popover and try to type "FF0000".
5. (Remainder of workflow, works once the value is set programmatically:) draw a rectangle, click the "+" in the Effects section to add a Drop shadow, click the diamond "+" variable affordance on the effect's color row, and select "Red" in the variable picker.

Actual Result:
- Clicking the hex input in the variable color-picker popover does not focus it — focus stays on the trigger button, so typing a hex value is impossible (reproduced multiple times).
- Workaround: setting the input's value programmatically works, after which the value sticks correctly.
- The rest of the flow works: the binding is confirmed (affordance turns into a purple "Detach variable" icon, effect color shows FF0000, and the rectangle's shadow renders red on canvas).

Expected Result:
Clicking the hex input in the variable color-picker popover should give it keyboard focus so the user can type a hex value (e.g. FF0000) directly, like every other text input in the app.

Estimate: M (3 points) — scoped feature fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 completed runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_259b37e3-de3f-4273-b47a-944d6f34d670.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_47f3752e-7429-4ecd-ae07-7c1bf7431a8a.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_4e450da9-c3e9-4555-a7d1-8c5f8a09054b.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_8db547fc-0225-4037-bef4-49b3958fceeb.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_d0a9d011-551b-43ae-bb58-d0cfa43ab5d2.txt`

Agent report (verbatim tail of failing run):

```
All steps are complete. Here's a summary of what was accomplished:

1. **Color variable created**: Opened the Variables panel, created a new collection with a color variable, renamed it "Red", and set its value to pure red **FF0000** (verified: red swatch + FF0000 in the variables table).

2. **Rectangle drawn**: Used the rectangle tool to draw "Rectangle 1" (250 × 170) on the canvas.

3. **Drop shadow added**: Clicked the "+" in the Effects section, which added a **Drop shadow** effect (X 0, Y 4, Blur 4, Spread 0).

4. **Shadow color bound to variable**: Clicked the variable affordance (diamond "+" icon) on the effect's color row, which opened a variable picker listing "Red"; selected it. The binding is confirmed — the affordance turned into a purple "Detach variable" icon, the effect color shows FF0000, and the rectangle's shadow renders red on canvas.

**Problem encountered**: The hex text input inside the color-picker popover (opened from the variable's swatch) refuses keyboard focus — clicking it leaves focus on the trigger button, so typing a hex value is impossible (reproduced multiple times; other inputs like the modal's search field and inline rename accept click-focus normally). I had to work around it by setting the input's value programmatically, after which the value stuck correctly. The rest of the flow (Effects "+", variable binding affordance, variable picker) worked smoothly.

Because of that hex-input focus bug in the variable color picker, verdict: not-approve
```
