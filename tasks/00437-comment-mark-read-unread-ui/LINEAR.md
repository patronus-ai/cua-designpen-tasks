# DesignPen [comments]: 'comment mark read unread' fails QA — 5/5 runs report broken workflow (00437-comment-mark-read-unread-ui)

Description:
Marking a comment thread as unread is unreachable because comment creation is broken: with the Comment tool active, clicking the canvas creates a "Draft comment" pin but the composer (text box + submit button) is never mounted in the DOM — inspection of the full accessibility tree (including off-viewport/hidden elements) shows no textarea, input, dialog, or popover, only the pin button and an invisible "Place comment" cursor-hint element. Typing consistently reports "no editable element is focused (active element: BUTTON)" and keystrokes are captured by global tool shortcuts (e.g., "R" switched to Rectangle and cancelled the draft). The agent also noted a related rendering defect: the right sidebar is clipped at the window edge (the "All" comments filter tab is cut off), suggesting broken layout/positioning in this build.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Activate the Comment tool (speech-bubble icon in the bottom toolbar).
3. Click on the canvas to place a comment pin.
4. Attempt to type "review the tokens" in the composer and submit the comment.
5. Click the pin to open the thread, open the thread's "…" menu, and choose the option to mark the thread as unread.

Actual Result:

- A blue draft pin appears at the click location (the DOM confirms a "Draft comment" button is created), but the comment composer (text box + submit button) never appears, so "review the tokens" cannot be typed or submitted.
- Typing consistently reports "no editable element is focused (active element: BUTTON)"; keystrokes are captured by global tool shortcuts (e.g., "R" switched to Rectangle and cancelled the draft), proving no hidden input exists.
- The full accessibility tree (including off-viewport/hidden elements) never contains a textarea, input, dialog, or popover — only the pin button and an invisible "Place comment" cursor-hint element.
- Clicking, double-clicking, long-pressing, dragging, hovering, right-clicking the pin, Enter/Space/Ctrl+Enter/Tab, fresh page reloads, a new browser window, browser zoom changes, placing the pin on empty canvas vs. on a shape, drag-to-region commenting, app menus, the Ctrl+K actions palette, and the Comments sidebar all fail; the "Open" counter stays at 0.
- Related rendering defect observed: the right sidebar is clipped at the window edge (the "All" comments filter tab is cut off).
- The thread, its "…" menu, and the "Mark as unread" option are unreachable.

Expected Result:
Placing a comment pin should open a composer so the message can be typed and submitted; the resulting thread's "…" menu should include a mark-as-unread option that flags the thread as unread.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 completed runs failed (`verdict: not-approve`)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_0aa25efc-b971-48f8-9c19-ce15bf963944.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_26781615-1d18-49a2-8180-59d80a3a1f96.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_282c9384-d018-4d41-9802-d86568353117.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_3fb5329c-c08f-4bb8-9923-4fb42a466934.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_3ff3110a-dbe1-4bb6-932e-8a98ca7561df.txt`

Agent report (verbatim tail of failing run):

```
I've thoroughly tested the comment feature and must report that the task could not be completed due to an app defect. Here's a summary of what happened:

**What I did:**
1. **Activated the Comment tool** (speech-bubble icon in the bottom toolbar) — this worked: the tool highlighted and the Comments sidebar opened (showing "Open 0 / Resolved 0 / All 0", "No comments").
2. **Clicked on the canvas** to place a comment — a blue draft pin appeared at the click location (the DOM confirms a "Draft comment" button is created).
3. **The comment composer (text box + submit button) never appeared.** Without it, there was no way to type "review the tokens" or submit the comment.

**Troubleshooting I attempted (all unsuccessful):**
- Clicking, double-clicking, long-pressing, dragging, hovering, and right-clicking the draft pin; clicking it via element reference; pressing Enter, Space, Ctrl+Enter, and Tab while it was focused.
- Typing directly — the browser consistently reported *"no editable element is focused (active element: BUTTON)"*, and keystrokes were still captured by global tool shortcuts (e.g., "R" switched to Rectangle and cancelled the draft), proving no hidden input exists.
- Inspecting the full accessibility tree (including off-viewport/hidden elements): no textarea, input, dialog, or popover is ever mounted — only the pin button and an invisible "Place comment" cursor-hint element.
- Fresh page reloads, a brand-new browser window, browser zoom changes to reveal off-screen UI, placing the pin on empty canvas vs. on a drawn shape, drag-to-region commenting, app menus (File/Edit/View/Preferences), the Ctrl+K actions palette, and the Comments sidebar itself — none provided any way to compose a comment. The "Open" counter stayed at 0 the whole time.
- I also noticed a related rendering defect: the right sidebar is clipped at the window edge (the "All" comments filter tab is cut off), suggesting broken layout/positioning in this build.

Because the composer never renders, the comment could not be created, so the subsequent steps (clicking the pin to open the thread, opening the thread's "…" menu, and choosing "Mark as unread") were unreachable. I cleaned up my test artifacts (deleted the test rectangle; draft pins were discarded).

**What went wrong:** The Comment tool places a draft pin, but the comment input/composer UI never appears (it is never mounted in the DOM), making it impossible to type or submit a comment — a blocking bug in the app's commenting feature.

verdict: not-approve
```
