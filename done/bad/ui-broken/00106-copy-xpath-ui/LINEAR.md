# DesignPen [clipboard / copy-paste]: 'copy xpath' fails QA — 4/5 runs report broken workflow (00106-copy-xpath-ui)

Description:
The context-menu action Copy/Paste as > Copy XPath silently fails: the menu item is present and clickable on a selected star, but no XPath expression is ever written to the clipboard, with no error or success feedback. A controlled test proved the clipboard round-trips fine in the session (marker string "XCLIPTESTX" copied via a native text input), yet after invoking "Copy XPath" pasting still produced the stale marker; "Copy node ID" failed identically. The app's programmatic clipboard access is blocked (the "Paste here" action surfaces the toast "Clipboard access is blocked in this browser context"), but the copy-side actions give no feedback at all — they just silently do nothing.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Select the Star tool from the shape dropdown in the bottom toolbar and drag on the canvas to draw a star ("Star 1", ~200x200).
3. Ensure the star is selected.
4. Seed the clipboard with a marker string via a native text input and Ctrl+C (to enable verification).
5. Right-click the star, hover "Copy/Paste as", and click "Copy XPath".
6. Paste (Ctrl+V) into a text input to check the clipboard contents.

Actual Result:

- After invoking "Copy XPath", pasting still produces the old marker string ("XCLIPTESTX") — no XPath expression was ever written to the clipboard. Repeated multiple times with the same result; "Copy node ID" failed identically.
- The "Copy XPath" action gives no error or success feedback at all — it silently does nothing.
- The app's programmatic clipboard access is blocked: "Paste here" shows the error toast "Clipboard access is blocked in this browser context".
- Clipboard copy/paste round-trips do work in the browser session via native text inputs, so the failure is in the app's copy path, not the environment's clipboard.

Expected Result:
Copy/Paste as > Copy XPath should place the path expression pointing at the selected layer onto the clipboard; if the clipboard write fails, the app should show an error rather than failing silently.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 4 of 5 runs failed (1 approved)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_7feedf57-325f-4938-a71f-bf07927dc67d.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_a7855a7d-4b72-4a89-af75-ff0cea3f9343.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_cd87a64c-9a7b-428b-a9e5-c75af08290e1.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_dfa4c93d-d11f-4061-a7d1-6cdbe2587831.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_f38b1c04-3369-4129-978a-731ca7db2983.txt`

Agent report (verbatim tail of failing run):

```
The task steps were all performed, and the final state is clean: the star (Star 1, 200×200) is drawn and selected, and the "Copy/Paste as > Copy XPath" menu item was found and clicked successfully.

**Summary of what was done:**
1. ✅ Selected the Star tool from the shape dropdown in the bottom toolbar
2. ✅ Drew a 200×200 star on the canvas ("Star 1" appeared in the Layers panel)
3. ✅ Selected the star (auto-selected after drawing; re-confirmed selection)
4. ✅ Right-clicked the star → hovered "Copy/Paste as" → clicked "Copy XPath"

**However, verification showed the copy silently failed.** I ran a controlled clipboard test:
- I placed a marker string ("XCLIPTESTX") on the clipboard via a native text input (Ctrl+C), proving that clipboard copy/paste round-trips work in this browser session.
- After invoking "Copy XPath" on the selected star, pasting (Ctrl+V) still produced the old marker string — no XPath expression was ever written to the clipboard. I repeated this multiple times with the same result, and "Copy node ID" failed identically.
- The app itself displayed the error toast "Clipboard access is blocked in this browser context" when using "Paste here", confirming the app's programmatic clipboard access is blocked — but the "Copy XPath" action gives no error or success feedback at all; it just silently does nothing.

So while the UI flow (draw → select → right-click → Copy/Paste as > Copy XPath) completed, the actual goal — getting the XPath expression for the layer onto the clipboard — did not happen: the clipboard remained unchanged, with no feedback to the user about the failure.

verdict: not-approve
```
