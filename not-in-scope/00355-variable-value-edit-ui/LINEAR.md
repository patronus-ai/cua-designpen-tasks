# DesignPen [variables]: 'variable value edit' fails QA — 5/5 runs report broken workflow (00355-variable-value-edit-ui)

Description:
The hex value input in the color-picker popover opened from a COLOR variable's mode-table cell (Local variables dialog) cannot be focused by clicking — single, double, and triple clicks, both by coordinates and directly on the element, leave keyboard focus on a button, so a user cannot type a new hex value such as FF0000. The agent could only edit the value programmatically (form_input), a workaround unavailable to real users, and confirmed the bug was reproducible by retesting at the end. Minor additional friction: the Variables dialog initially renders completely empty with no "Create variable" affordance until a collection is added, and Escape doesn't close the color picker (it deselects the canvas shape instead).

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Open the Local variables dialog from the left panel Variables tab and create a collection (the dialog is empty with no "Create variable" affordance until you do).
3. Create a COLOR variable named "surface" (any starting color); close the dialog.
4. Draw a rectangle and bind its fill to "surface" via the diamond icon in the Fill row.
5. Reopen the variables dialog and click the "surface" mode-table cell to open its color-picker popover.
6. Click the hex value input and attempt to type "FF0000".

Actual Result:

- The hex input cannot be focused by clicking — single, double, and triple clicks (by coordinates and directly on the element) all left keyboard focus on a button, making it impossible to type a new hex value like a normal user; reproducible on retest.
- The value could only be set programmatically (form_input); once set, the cell showed FF0000 with a red swatch and the bound rectangle updated to red, proving the binding itself works.
- The Variables dialog initially rendered completely empty with no "Create variable" affordance until a new collection was added.
- Escape didn't close the color picker; it deselected the canvas shape instead.

Expected Result:
Clicking the hex input in the variable's color-picker popover should focus it so the user can type a new value (e.g. FF0000), which commits to the variable and re-resolves bound fills on the canvas.

Estimate: S (2 points) — small handler/layout fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 completed runs failed (`verdict: not-approve`)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_0293827b-0de4-4c9b-a540-ca614c198e42.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_04aed558-8ad7-4192-ad32-9d7fb740f373.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_3329ff91-be9f-48a8-9097-aab87fc870d2.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_6f4f74d5-7737-4b02-838a-25188953c4fd.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_bfd72378-7dc3-4ce5-8a34-f5b8a7bed85c.txt`

Agent report (verbatim tail of failing run):

```
The task is complete. Final state verified:

- **Variable created**: A COLOR variable named "surface" exists in the Local variables dialog (in "New collection", Mode 1), initially black (000000).
- **Rectangle bound**: I drew a 200×150 rectangle and bound its fill to the variable via the diamond icon in the Fill row (binding confirmed by the purple variable chip and the generated CSS `background: var(--surface, #FF0000)` in the Code tab).
- **Value edited to red**: After reopening the variables dialog, the "surface" mode-table cell now shows FF0000 with a red swatch, and the rectangle on canvas updated to red accordingly, proving the binding works.

**Summary of how it went:** The overall flow worked, but I hit a real bug along the way: in the variable's color-picker popover (opened from the mode table cell), the hex value input cannot be focused by clicking — single, double, and triple clicks (both by coordinates and directly on the element) all left keyboard focus on a button, making it impossible to type a new hex value like a normal user would. I confirmed this was reproducible by retesting at the end. I only succeeded by setting the field's value programmatically (form_input), a workaround unavailable to real users. Additionally, minor friction: the Variables dialog initially rendered completely empty with no "Create variable" affordance until a new collection was added, and Escape didn't close the color picker (it deselected the canvas shape instead).

Because of the unfocusable hex input bug in the variable color picker (typing impossible, required a programmatic workaround), this did not go smoothly.

verdict: not-approve
```
