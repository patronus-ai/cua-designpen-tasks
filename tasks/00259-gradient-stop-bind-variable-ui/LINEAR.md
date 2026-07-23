# DesignPen [fills & color]: 'gradient stop bind variable' fails QA — 3/5 runs report broken workflow (00259-gradient-stop-bind-variable-ui)

Description:
The hex text input inside the Variables panel's color picker will not accept keyboard focus. When setting a color variable's value, clicking the hex field (by coordinate, by element reference, and via double-click) leaves focus on a button, so typing a hex value like "00FF00" is impossible. Other text inputs in the app (variable name inline edit, modal search field) focus and accept typing normally, so this is a focus-handling bug specific to that picker's hex field. The rest of the flow — creating the variable, gradient fill, stop selection, and binding the stop via the diamond variable affordance on the stop row — works; the agent could only set the value by injecting it programmatically via a form-input mechanism.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Open the Variables panel and create a new collection.
3. Add a Color variable and rename it (e.g. "Green").
4. Open the variable's color picker and click its hex text input, then attempt to type 00FF00.
5. (Remaining workflow, which works once the value is set) Draw a rectangle, switch its fill from solid to a Linear gradient, select the gradient's first stop (0%), and click the diamond-shaped variable affordance on the stop's row to bind it to the "Green" variable.

Actual Result:

- The hex text input inside the variable color picker never accepted keyboard focus: repeated clicks by coordinate, by element reference, and double-click all left focus on a button, so typing "00FF00" was impossible.
- Other text inputs in the app (variable name inline edit, modal search field) focused and accepted typing normally.
- Workaround: the value was set programmatically via a form-input mechanism, which the app accepted; after that, the gradient fill, stop selection, and variable binding affordance all worked (stop shows 00FF00 with a purple "bound" diamond icon, canvas renders a green-to-white gradient, Code/Inspect tab references "New collection / Auto (Mode 1)").

Expected Result:
Clicking the hex input in the variable color picker should give it keyboard focus so the user can type a hex value (e.g. 00FF00) directly, like every other text input in the app.

Estimate: M (3 points) — scoped feature fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 3 of 5 completed runs failed (2 approved)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_12ae6309-a98d-4a5a-967d-59ac85984e1e.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_4931713f-928c-498f-83e9-a15c2dc7fa8f.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_76c8fb3f-2d4f-42cf-a2ed-3c3b8a3174c1.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_924975c2-fadc-4a8f-9df9-5d842d104195.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_e9ceb70c-9c77-441d-bcdb-9c385c5c88c5.txt`

Agent report (verbatim tail of failing run):

```
All steps are complete. Final state summary:

**What was accomplished:**
1. **Color variable created** — Opened the Variables panel, created a new collection, added a Color variable, renamed it "Green", and set its value to pure green **00FF00** (verified: green swatch + hex 00FF00 in the variables table, persisted after closing/reopening).
2. **Rectangle drawn** — A 300×200 rectangle ("Rectangle 1") on the canvas.
3. **Gradient fill applied** — Switched the rectangle's fill from solid to a **Linear gradient** (stops at 0% and 100%).
4. **First stop selected** — Selected the gradient's first stop (0%, its row highlighted and its handle active in the gradient bar).
5. **Stop bound to the variable** — Clicked the diamond-shaped **variable affordance on the first stop's row**, which opened a variable picker listing "Green"; selected it. The stop now shows 00FF00 with a purple "bound" diamond icon (vs. gray "+" on the unbound stop), the canvas renders a green→white gradient, and the Code/Inspect tab confirms the layer references "New collection / Auto (Mode 1)".

**Problem encountered:** While setting the variable's value, the hex text input inside the variable color picker would not accept keyboard focus — I clicked it repeatedly (by coordinate, by element reference, double-click), yet focus always remained on a button, so typing "00FF00" was impossible. Other text inputs in the app (variable name inline edit, modal search field) focused and accepted typing normally, so this looks like a focus-handling quirk/bug specific to that picker's hex field. I worked around it by setting the value programmatically via a form-input mechanism, which the app accepted correctly, and the rest of the flow (gradient, stop selection, variable binding affordance) worked flawlessly.

Since the task goal was fully achieved but I did hit a real problem requiring a workaround along the way:

verdict: not-approve
```
