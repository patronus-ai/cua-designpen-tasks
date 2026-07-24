# DesignPen [variables]: 'variable mode add' fails QA — 5/5 runs report broken workflow (00351-variable-mode-add-ui)

Description:
Variable modes in the Local variables dialog are broken in several ways, the critical one being that "Set as default" on a mode column's context menu never propagates: a rectangle whose width is bound to a FLOAT variable ("gutter", 200 in Mode 1 / 320 in a new "Dark" mode) stays at 200 after Dark is made default — the canvas does not re-resolve variables live — and the default-mode flag is not persisted, reverting to Mode 1 on every reload. Additional bugs: a newly added mode column does not render in the variables table until a full page reload (edits can hit the wrong mode), the "Apply variable" popup closes on any mousedown while the W input is focused, uncaught errors surface as toasts ("e?.focus is not a function", "Uncaught TypeError: Cannot read properties of undefined (reading 'subTree')"), and variable rows expose no delete affordance.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Open the Local variables dialog from the left panel Variables tab.
3. Create a collection ("New collection").
4. Add a FLOAT/Number variable "gutter" with value 200 in the default mode (Mode 1); close the dialog.
5. Draw a rectangle and bind its width (W field) to "gutter" via the Apply-variable affordance — it should snap to 200.
6. Reopen the variables dialog and add a second mode via the "+" in the mode header; rename it to "Dark".
7. Set "gutter" to 320 in the Dark column.
8. Open Dark's column context menu and click "Set as default".
9. Observe the bound rectangle on canvas; then reload the page and reopen the dialog to check the default mode.

Actual Result:

- Critical: "Set as default" never propagates to the canvas — the bound rectangle stays at 200 x 120 (its Modes info still shows "Auto (Mode 1)"); the canvas does not re-resolve variables live.
- The default-mode flag is not persisted: after any reload the default reverts to Mode 1 (set three times, lost each time).
- A newly added mode column does not render in the variables table until a full page reload, which caused an edit intended for Mode 2 to initially hit Mode 1.
- The "Apply variable" popup closes on any mousedown while the W input has focus, so binding clicks don't register; binding only worked by triggering the apply-variable button via the accessibility ref with focus elsewhere.
- Renaming the mode via Enter appears to fail in the table UI (header stays stale) even though the rename actually commits.
- Uncaught errors surfaced as toasts: "e?.focus is not a function" and "Uncaught TypeError: Cannot read properties of undefined (reading 'subTree')"; Escape unexpectedly closed the entire dialog.
- A stray "New number" variable could not be deleted — rows expose no delete/context-menu affordance (right/left-click only opens inline editors).

Expected Result:
Setting a mode as default should immediately re-resolve bound variables on the canvas (rectangle width jumps to 320) and the default-mode choice should persist across reloads. New mode columns should render without a page reload, and the dialog should be free of uncaught errors.

Estimate: S (2 points) — small handler/layout fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 completed runs failed (`verdict: not-approve`)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_0c48bcac-5091-45f0-9cad-9c157c3bd713.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_1e718926-ff85-48e8-8513-9e9b090a8e8b.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_5da000ca-f2f1-4686-b90c-6323f0567c63.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_76ec3cfa-b25c-41f0-b428-8b62ee2de42f.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_a61465ab-ddb1-41cc-8458-49cda8b86d1a.txt`

Agent report (verbatim tail of failing run):

```
All task steps have been executed. Here is the final summary:

**Completed steps:**
1. ✅ Opened the Local variables dialog from the left panel Variables tab
2. ✅ Created a collection ("New collection")
3. ✅ Added a FLOAT/Number variable "gutter" with value 200 in the default mode (Mode 1)
4. ✅ Drew a rectangle and bound its width to "gutter" — it snapped to 200 (Code tab confirmed `width: var(--gutter, 200px)`)
5. ✅ Added a second mode via the "+" in the mode header and renamed it to "Dark"
6. ✅ Set "gutter" to 320 in the Dark column (persists correctly)
7. ✅ Clicked "Set as default" on Dark's column context menu — in-session the data model updated (Dark's menu loses "Set as default", Mode 1's menu gains it)

**Problems encountered (app bugs):**
- The "Apply variable" popup closes on any mousedown while the W input has focus, so binding clicks don't register; I had to trigger the apply-variable button via the accessibility ref with focus elsewhere to bind at all.
- A newly added mode column does not render in the variables table until a full page reload, which also caused an edit intended for Mode 2 to initially hit Mode 1.
- Renaming the mode via Enter appears to fail in the table UI (header stays stale) even though the rename actually commits.
- Several uncaught errors surfaced as toasts: "e?.focus is not a function" and "Uncaught TypeError: Cannot read properties of undefined (reading 'subTree')"; Escape unexpectedly closed the entire dialog.
- **Critical:** the "Set as default" change never propagates to the canvas — the bound rectangle stays at 200 × 120 (its Modes info still shows "Auto (Mode 1)"), the canvas doesn't re-resolve variables live, and the default-mode flag is not persisted: after any reload the default reverts to Mode 1 (I set it three times and verified loss each time). So the bound rectangle never follows the new Dark mode (expected width 320).
- A stray "New number" variable created during debugging could not be deleted — rows expose no delete/context-menu affordance (right/left-click only opens inline editors).

The configuration (collection, gutter = 200/320, Dark mode, binding) is in place and Dark is set as default in the current session, but the core expected behavior — the rectangle following the new default mode to 320 — is broken by the app's persistence/refresh bugs.

verdict: not-approve
```
