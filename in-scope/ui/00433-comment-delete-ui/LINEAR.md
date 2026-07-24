# DesignPen [comments]: 'comment delete' fails QA — 5/5 runs report broken workflow (00433-comment-delete-ui)

Description:
Deleting a comment thread cannot be exercised because no comment can ever be created: after selecting the Comment tool (tooltip "Comment (C)") and clicking the canvas, a blue draft pin appears and the Comments panel opens, but the comment composer (text input bubble) never appears. DOM/accessibility-tree inspection shows the only comment-related elements that ever exist are the "Place comment" cursor hint and the "Draft comment" pin button — no textarea/input/contenteditable is ever created. Letter keys after focusing the pin just trigger global tool shortcuts (e.g. "h" switched to the Hand tool). Because the panel permanently shows "No comments", the delete flow (pin click → thread "…" menu → Delete → confirm) is unreachable.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Select the Comment tool via the toolbar speech-bubble icon (tooltip "Comment (C)") or the "C" shortcut.
3. Click on the canvas to place the first comment; attempt to type "keep this note" and submit.
4. Click elsewhere on the canvas to place a second comment; attempt to type "delete this note" and submit.
5. Click the pin of the second comment, open the thread's "…" menu, choose Delete, and confirm in the dialog.

Actual Result:

- Placing a pin shows a blue draft pin and opens the Comments panel ("Open 0 / Resolved 0 / All 0"), but the comment composer (text input bubble) never appears, so neither "keep this note" nor "delete this note" can be typed.
- No textarea/input/contenteditable is ever created; the only comment-related elements in the DOM are the "Place comment" cursor hint and the "Draft comment" pin button.
- Single-click, double-click, click-and-drag, right-click (only the generic canvas context menu), separate mouse-down/mouse-up, clicking the pin repeatedly, Enter/Space/Tab, letter keys (which trigger global tool shortcuts, e.g. "h" switched to the Hand tool), main menu, command palette, Tools panel, Comments sidebar, browser zoom-out, full page reload, and a fresh browser window all fail identically.
- The panel permanently shows "No comments", so the delete steps (pin click, "…" menu, Delete, confirmation dialog) are impossible.

Expected Result:
Placing a comment pin should open a text-entry bubble so each comment can be typed and submitted; clicking a comment's pin should open its thread, whose "…" menu should offer Delete with a confirmation dialog that removes the thread.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 completed runs failed (`verdict: not-approve`)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_150da55b-4ab5-47bf-a789-3b9116b17253.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_647af468-ce42-4581-8005-6a86fdd9f50d.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_65c9a619-418e-4049-9151-bfeeecaa26da.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_8be266ad-4fe8-4659-ae12-49e0595510f2.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_a0d3d5b2-93e4-4495-9af6-b1832d2f7b85.txt`

Agent report (verbatim tail of failing run):

```
I have exhausted all reasonable approaches. Here is a summary of what happened:

**What I attempted:**
1. Selected the Comment tool (verified via its tooltip "Comment (C)") both by clicking the toolbar speech-bubble icon and via the "C" keyboard shortcut.
2. Clicked on the canvas to place a comment — a blue draft pin appears on the canvas, and the right-hand Comments panel opens ("Open 0 / Resolved 0 / All 0").
3. From there, the comment composer (text input bubble) **never appears**, so there is no way to type "keep this note" or "delete this note".

**Everything I tried to get a text input to appear:**
- Single-click, double-click, click-and-drag, right-click (only shows the generic canvas context menu), and separate mouse-down/mouse-up on both empty canvas and on top of a frame I drew
- Clicking the placed "Draft comment" pin repeatedly, by coordinates and by element reference; hovering it; pressing Enter/Space/Tab/letter keys after focusing it (letter keys just trigger global tool shortcuts, e.g. "h" switched to the Hand tool)
- DOM inspection with the accessibility tree (including off-viewport elements), page-text extraction, and AI element search — the only comment-related elements that ever exist are the "Place comment" cursor hint and the "Draft comment" pin button; **no textarea/input/contenteditable is ever created**
- Checked the main menu (File/Edit/View/Object/...), the command palette shortcut, the Tools panel, the Comments sidebar (scrolling, tabs), and browser zoom-out to look for off-screen popups
- Full page reload and a completely fresh browser window — identical broken behavior in both

**Result:** Because the comment composer popup never opens, no comment can be submitted (the panel permanently shows "No comments"). Consequently, neither of the two requested comments could be created, and the follow-up steps (clicking the second comment's pin, opening the thread's "…" menu, choosing Delete, and confirming) were impossible since no comment thread ever exists.

The app's Comment feature is broken: placing a comment pin never opens the text-entry bubble, making it impossible to create any comment, so none of the requested steps could be completed.

verdict: not-approve
```
