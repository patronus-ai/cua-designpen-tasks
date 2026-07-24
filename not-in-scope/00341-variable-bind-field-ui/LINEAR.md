# DesignPen [variables]: 'variable bind field' fails QA — 4/5 runs report broken workflow (00341-variable-bind-field-ui)

Description:
The variable picker popup used to bind a properties-panel field (e.g. a rectangle's W field) to a variable is completely inert. The diamond "Apply variable" affordance on the W field works and opens the picker (showing a Search box, the "card-width" option, and a "+ Create number variable from 200" row), but the popup dismisses on any pointerdown — including clicks on its own options and search box — so a selection can never complete, and keyboard focus never leaves the numeric W input (arrows change the width value, typed text goes to the field, Tab closes the popup). Variable creation itself works fine; the bug is specific to this picker (other popups/dropdowns in the app work normally) and reproduces after reload.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Open the Local variables dialog from the left panel Variables tab.
3. Create a collection via the folder-plus icon ("New collection").
4. Via "+ Add" → Number, create a FLOAT variable, rename it "card-width", set its value to 240.
5. Close the dialog and draw a rectangle on the canvas.
6. In the properties panel, hover or right-click the W (width) field to reveal the diamond "Apply variable" button and click it to open the variable picker popup.
7. Click the "card-width" option in the popup (or its Search box, or the "Create variable…" row).

Actual Result:
- The popup "dismisses on **any pointerdown** — including clicks on the 'card-width' option itself, the popup's own Search box, the 'Create variable…' row, and even the anchor W input — so a selection click can never complete (the option unmounts before the click registers)." Reproduced via normal clicks, ref clicks, hover-then-click, mousedown-hold-release, press-drag-release, right/middle-button clicks.
- "Keyboard never reaches the popup": focus stays in the numeric W input — arrows increment/decrement the width, Enter commits the number, Tab blurs and closes the popup, typed text goes to the W field, not the popup's search.
- Programmatically setting the search value also dismissed it; drag-and-drop from the Variables dialog and right-click menus on the variable row offered no apply path.
- Reproduces identically after a full page reload; other popups (width-mode menu, Add-variable type menu, rename/delete menus) work normally.
- Final state via Code tab: `width: 200px` — no `var(--card-width)` binding.

Expected Result:
Clicking "card-width" in the variable picker (or selecting it via keyboard) should bind the rectangle's width to the variable, setting the width to 240 and showing the binding (e.g. `var(--card-width)` in the Code tab) instead of the popup closing without effect.

Estimate: M (3 points) — scoped feature fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 4 of 5 completed runs failed (`verdict: not-approve`, 1 approved)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_21127497-1cb2-43d5-95f8-727c6e1f4895.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_283aeeed-0b0d-4bb8-a122-3883341b1389.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_474a0b1e-8e60-48e8-876b-b5fd023dd753.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_8e18a96e-8dae-4d00-a853-f7bdf97bfc66.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_ffdd7dde-0832-462d-b2ac-82cffbbc8624.txt`

Agent report (verbatim tail of failing run):

```
I've exhausted every feasible interaction path. Here's the final report:

## What was completed successfully
1. **Variables dialog** — opened from the left panel's Variables tab.
2. **Collection** — created via the dialog's folder+ icon ("New collection").
3. **Number (FLOAT) variable** — added via "+ Add" → Number, renamed to **card-width**, value set to **240** (verified in the dialog as `# card-width | 240`, and it persisted across a page reload).
4. **Rectangle** — drawn on canvas ("Rectangle 1", 200×150, appears in Layers and the Design panel).

## What failed: binding width → card-width (app bug)
The W field's variable affordance works up to a point: hovering/right-clicking the W field reveals a diamond "Apply variable" button, and clicking it opens the variable picker popup showing a Search box, the "card-width" option (pre-highlighted), and "+ Create number variable from 200". However, **the popup is completely inert**:

- It dismisses on **any pointerdown** — including clicks on the "card-width" option itself, the popup's own Search box, the "Create variable…" row, and even the anchor W input — so a selection click can never complete (the option unmounts before the click registers). Verified via normal clicks, accessibility-ref clicks, hover-then-click, mousedown-hold-release, press-drag-release, and right/middle-button clicks.
- **Keyboard never reaches the popup**: focus stays in the numeric W input — Down/Up arrows decrement/increment the width value (I had to restore 200 repeatedly), Enter just commits the number, Tab blurs and closes the popup, and typed text goes to the W field, not the popup's search.
- Programmatically setting the popup's search value also dismissed it; drag-and-dropping the variable from the Variables dialog onto the W field, and right-click context menus on the variable row in the dialog, offered no "apply" path either.
- The bug reproduced identically after a full page reload. Other popups/dropdowns in the app (width-mode menu, Add-variable type menu, rename/delete menus) work normally, so this is specific to the variable picker.
- Final state confirmed via the Code tab: `width: 200px` — no `var(--card-width)` binding; canvas still shows 200 × 150.

Steps 1–4 of the task are done, but step 5 (binding the rectangle's width to "card-width") is impossible to complete: the variable picker popup closes on any click/keypress without ever applying the selected variable.

verdict: not-approve
```
