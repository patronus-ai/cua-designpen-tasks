# DesignPen [variables]: 'variable collection create' fails QA — 5/5 runs report broken workflow (00342-variable-collection-create-ui)

Description:
The variable-collection workflow itself is completable end to end (create "Theme" collection, add COLOR variable "brand" = #FF00FF, bind a rectangle's fill to the token via the fill picker's Libraries → Variables tab), but the flow is riddled with genuine bugs. A red error toast "Uncaught TypeError: Cannot read properties of undefined (reading 'subTree')" repeatedly pops up during normal interactions (selecting the rectangle tool, opening the fill picker, switching to the Code tab, opening/closing the Variables dialog), and the hex value input inside the variable's color picker cannot be focused by clicking — typing the hex value is impossible without a programmatic workaround. The toast also does not intercept pointer events, so a click aimed at its close button passed through and created a rectangle underneath.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Open the Local variables dialog from the left panel Variables tab.
3. Create a new collection via the folder-plus button (or empty-state action) and rename it to "Theme".
4. Use the Add menu → Color to create a COLOR variable and rename it to "brand".
5. Open the variable's color picker and try to click into the hex value input to type "FF00FF".
6. Draw a rectangle on the canvas (watch for the error toast while selecting the rectangle tool).
7. Bind the rectangle's fill to the "brand" token via the fill picker's Libraries → Variables tab, and check the Code tab.

Actual Result:
- A red error toast — "Uncaught TypeError: Cannot read properties of undefined (reading 'subTree')" — repeatedly popped up during normal interactions (selecting the rectangle tool, opening the fill picker, switching to the Code tab, opening/closing the Variables dialog), firing multiple times with a ×2 counter.
- The hex value input inside the variable's color picker could not be focused by clicking (single/double/triple clicks left focus on a button, and Tab closed the picker), so typing "FF00FF" directly was impossible; the value had to be set programmatically. A normal user would likely be stuck there.
- A click aimed at the error toast's close button passed through it and created a rectangle on the canvas underneath (the toast doesn't intercept pointer events).
- Despite the bugs, all requested artifacts ended up correctly wired: Theme collection → brand = #FF00FF → rectangle fill bound to the token (`background: var(...)`, "Background colors: brand", mode "Theme").

Expected Result:
The workflow should complete without uncaught exceptions: no TypeError toasts during normal interactions, the hex input in the variable color picker should be focusable and typeable, and toasts should intercept pointer events so clicks on them don't fall through to the canvas.

Estimate: M (3 points) — scoped feature fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 completed runs failed (`verdict: not-approve`)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_5aa76bf1-a5ad-44c2-b802-d8fe19ef06a3.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_6cb637e0-7321-47fd-9f12-4c02f4e6222f.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_b078a7f0-4f33-4edc-a808-ac0226b12ee2.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_b55a15bd-9f5c-405d-af72-514bf10ffda2.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_be744f5d-a27e-4831-81eb-cbe9afbdc83d.txt`

Agent report (verbatim tail of failing run):

```
The task is now complete. Let me summarize the final state:

**What was accomplished:**
1. ✅ Opened the Local variables dialog from the left panel's Variables tab
2. ✅ Created a new collection via the folder-plus button and renamed it to "Theme"
3. ✅ Used the Add menu → Color to create a COLOR variable, renamed it to "brand", and set its value to #FF00FF (confirmed in the dialog: magenta swatch + "FF00FF" in Mode 1)
4. ✅ Drew a rectangle ("Rectangle 1", 100×100) on the canvas
5. ✅ Bound its fill to the "brand" token via the fill picker's Libraries → Variables tab (the token showed a checkmark, the Fill row shows the variable-bound diamond indicator, and the Code/Inspect panel confirms `background: var(...)` with "Background colors: brand" and mode "Theme")

**Problems encountered along the way:**
- A red error toast — "Uncaught TypeError: Cannot read properties of undefined (reading 'subTree')" — repeatedly popped up during normal interactions (selecting the rectangle tool, opening the fill picker, switching to the Code tab, opening/closing the Variables dialog, firing multiple times with a ×2 counter). It didn't permanently block the flow, but it's a recurring uncaught exception.
- The hex value input inside the variable's color picker could not be focused by clicking (single/double/triple clicks left focus on a button, and Tab closed the picker), so typing "FF00FF" directly was impossible; I had to set the field value programmatically as a workaround. A normal user would likely be stuck there.
- Minor: a click aimed at the error toast's close button passed through it and created the rectangle on the canvas underneath (the toast doesn't intercept pointer events).

All requested artifacts exist and are correctly wired up (Theme collection → brand = #FF00FF → rectangle fill bound to the token), but I hit genuine app bugs along the way: recurring uncaught TypeError toasts and a hex input in the variable color picker that couldn't be focused/typed into, requiring a programmatic workaround.

verdict: not-approve
```
