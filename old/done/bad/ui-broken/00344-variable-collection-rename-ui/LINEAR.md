# DesignPen [variables]: 'variable collection rename' fails QA — 3/5 runs report broken workflow (00344-variable-collection-rename-ui)

Description:
The double-click rename flow for a variable-collection tab in the Local variables dialog has a focus bug. Double-clicking the collection tab visually opens the rename input, but keyboard focus is not moved into it — keystrokes never reach the field (the active element stays a plain DIV), and while in this unfocused edit state Escape does not cancel the editor and clicking elsewhere in the dialog does not dismiss it, leaving the tab stuck in edit mode. The rename can still be committed via a workaround (an extra click into the input after the double-click), so the feature works but the primary interaction is broken.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Open the Local variables dialog from the left panel Variables tab.
3. Create a collection using the folder-plus button in the dialog header ("New collection" appears with Mode 1).
4. Double-click the collection tab to enter rename mode.
5. Immediately type "Brand tokens" (without clicking again) and press Enter.
6. Also try pressing Escape or clicking elsewhere in the dialog while in this state.

Actual Result:
- After double-click, the rename input opens visually but "keyboard focus is not moved into it — typing immediately after double-click does nothing (keystrokes never reach the field; ... BackSpace left the text untouched), and the reported active element stays a plain DIV."
- While in this unfocused edit state, "Escape does not cancel the editor and clicking elsewhere in the dialog does not dismiss it — the tab stays stuck in edit mode."
- Workaround: clicking the input field an extra time after double-clicking makes typing and Enter work normally; the rename to "Brand tokens" then commits correctly (verified visually and in the accessibility tree as `tab "Brand tokens"`). Bug reproduced twice in the run.

Expected Result:
Double-clicking the collection tab should move keyboard focus into the rename input so typing works immediately, Escape should cancel the editor, and clicking elsewhere should dismiss it.

Estimate: S (2 points) — small handler/layout fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 3 of 5 completed runs failed (`verdict: not-approve`, 2 approved)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_0f208910-b167-4773-8baf-038c8a3519f0.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_66f1ca31-eb3c-4447-a058-06946bc04c3b.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_a16e4bd5-716d-4e36-944d-2b5ffd517ffd.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_d98cd226-b841-4207-9657-d82e61f4ab14.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_dbaf5390-79c2-4230-b5c9-c03e21dfa996.txt`

Agent report (verbatim tail of failing run):

```
The final state is verified: the Local variables dialog shows the collection tab named "Brand tokens" (committed, no longer in edit mode), with its "Mode 1" column and variable table ready.

**Summary of what I did:**
1. Opened the Local variables dialog via the left panel's **Variables** tab ✔
2. Created a collection using the folder-plus button in the dialog header ("New collection" appeared with Mode 1) ✔
3. Double-clicked the collection tab to enter rename mode, typed "Brand tokens", and committed with Enter ✔ — final name verified both visually and in the accessibility tree (`tab "Brand tokens"`).

**Problem encountered (reproduced twice):** the double-click rename flow has a focus bug. Double-clicking the collection tab visually opens the rename input, but keyboard focus is not moved into it — typing immediately after double-click does nothing (keystrokes never reach the field; I confirmed BackSpace left the text untouched), and the reported active element stays a plain DIV. Worse, while in this unfocused edit state, Escape does not cancel the editor and clicking elsewhere in the dialog does not dismiss it — the tab stays stuck in edit mode. The workaround is to click the input field an extra time after double-clicking, after which typing and Enter work normally and the rename commits correctly.

So the end goal was achieved, but only via a workaround for a genuine focus/usability bug in the double-click rename interaction.

verdict: not-approve
```
