# DesignPen [comments]: 'comment edit message' fails QA — 5/5 runs report broken workflow (00434-comment-edit-message-ui)

Description:
Editing a comment message is unreachable because the comment composer never opens after placing a pin. With the Comment tool active, clicking the canvas creates a blue draft pin, but accessibility-tree dumps (including off-viewport elements) show only a `button "Draft comment"` pin and a "Place comment" cursor hint — no textbox/textarea/contenteditable anywhere in the DOM. Attempting to type reports "no editable element is focused (active element: BUTTON)", and single letters trigger global tool shortcuts (e.g. "t" switched to the Text tool, cancelling the draft). The agent also found the "Actions… ⌘K" palette fails to open. Since no comment can be typed or submitted, there is no thread to open, no "…" menu, and no Edit/save step possible.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Select the Comment tool (speech-bubble icon in the bottom toolbar).
3. Click the canvas to place a comment pin.
4. Attempt to type "the buton color is off" in the composer and submit the comment.
5. Click the pin to open the thread, open the message's "…" menu, choose Edit, correct the text to "the button color is off", and save the edit.

Actual Result:

- A blue draft pin appears at the click point, but the comment composer (text input with a submit button) never opens; there is nowhere to type "the buton color is off".
- Accessibility-tree dumps right after placing the draft show only a `button "Draft comment"` pin and a "Place comment" cursor hint — no textbox/textarea/contenteditable anywhere in the DOM.
- Typing reports "no editable element is focused (active element: BUTTON)"; single letters trigger global tool shortcuts (e.g. "t" switched to the Text tool, cancelling the draft).
- Visual zoom on the pin area and zooming the whole page out to 51% show no mis-positioned off-screen popup; clicking/double-clicking/long-pressing the pin, Enter/Space, hovering, separate mouse-down/up, click-drag placement, placing on a rectangle or inside a frame, toggling the Comments sidebar, full page reloads, a fresh browser window, the right-click context menu, and the main menu all fail. The "Actions… ⌘K" palette also fails to open.
- The comment count stays at 0; the edit steps (thread, "…" menu, Edit, save) are impossible.

Expected Result:
Placing a comment pin should open a composer so the message can be typed and submitted; opening the thread and choosing Edit from the message's "…" menu should allow correcting the text and saving the updated message.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 completed runs failed (`verdict: not-approve`)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_039474d1-143a-4251-b2f4-c58b9552170a.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_48968d26-5e45-4f50-92ad-7db9fd333a8c.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_8df2cfe9-5a5e-4323-a5ea-ef8086d03033.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_de379679-4524-44af-9b6b-14eb484ea0dd.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_e1fb3381-8067-4e00-bd06-9642c7e23f04.txt`

Agent report (verbatim tail of failing run):

```
I've exhausted every plausible interaction path. Here is a summary of what happened:

**What I attempted**

1. **Selected the Comment tool** (speech-bubble icon in the bottom toolbar) — it activated correctly and the Comments sidebar opened ("No comments", Open 0).
2. **Clicked the canvas** to place a comment. A blue draft pin appears at the click point, but **the comment composer (text input with a submit button) never opens**, so there is nowhere to type "the buton color is off" or submit it.
3. I verified the composer truly doesn't exist rather than being merely invisible:
   - Accessibility-tree dumps (including off-viewport elements) right after placing the draft show only a `button "Draft comment"` pin and a "Place comment" cursor hint — **no textbox/textarea/contenteditable anywhere in the DOM**.
   - Attempting to type reports "no editable element is focused (active element: BUTTON)"; single letters instead trigger global tool shortcuts (e.g. "t" switched to the Text tool, cancelling the draft).
   - Visual zoom on the pin area and zooming the whole page out to 51% (to reveal any mis-positioned off-screen popup) show nothing.
4. **Workarounds tried, all unsuccessful:** clicking / double-clicking / long-pressing the pin, Enter/Space on the focused pin, hovering the pin, separate mouse-down/up, click-drag placement, placing the pin on a rectangle and inside a frame (in case comments need an object — I created and later deleted these test shapes), toggling the Comments sidebar/tabs, full page reloads, a fresh browser window, right-click context menu, and the main menu (File/Edit/View/Object… and the "Actions… ⌘K" palette, which also fails to open). No "add comment" input ever appears, and the comment count stays at 0.

**Consequence:** since the comment can never be typed or submitted, there is no pin thread to open, no "…" menu, and no Edit/save step possible. The entire requested flow is blocked by this app defect (the draft pin is created, but the comment input popup fails to render).

The task could not be completed: the Comment tool's composer never appears after placing a pin, making it impossible to enter or submit the comment text, and therefore impossible to perform the subsequent edit steps.

verdict: not-approve
```
