# DesignPen [comments]: 'comment reply' fails QA — 5/5 runs report broken workflow (00440-comment-reply-ui)

Description:
In the DesignPen/OpenPencil design app, the Comment tool's composer never renders after placing a comment pin, so no comment can ever be written, submitted, or replied to. Activating the Comment tool (toolbar speech-bubble button or the "C" shortcut) works and clicking the canvas places a blue draft pin (a "Draft comment" button appears in the DOM), but no textarea, textbox, or contenteditable comment input ever mounts anywhere on the page — verified via repeated full accessibility-tree reads including off-viewport elements. Typing after placement fails ("no editable element is focused") and keystrokes instead trigger global tool shortcuts; clicking the pin either does nothing or the canvas overlay intercepts the event and re-creates the draft pin. The Comments panel permanently shows "No comments" (Open 0 / Resolved 0 / All 0), so the reply flow is completely unreachable.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Activate the Comment tool via the speech-bubble button in the bottom toolbar (or press "C"); the Comments sidebar opens.
3. Click anywhere on the canvas to place a comment pin — a blue draft pin appears.
4. Attempt to type "does this work?" into the comment composer.
5. Attempt to submit the comment, then click the pin to open its thread.
6. Attempt to type "yes, approved" in the thread's reply composer and submit the reply.

Actual Result:
- After placing the pin, no text input/composer ever renders — not on screen and not anywhere in the DOM (no textarea, textbox, or contenteditable related to comments exists on the page).
- Typing immediately after placing the pin fails with "no editable element is focused"; character keys instead trigger the app's global tool shortcuts (at one point switching to vector-edit mode).
- Clicking the pin (normal click, double-click, slow mouse-down/up, element-reference click) either does nothing or the canvas overlay intercepts the event and re-creates the draft pin (confirmed by the button remounting in the DOM).
- Keyboard-focusing the draft pin button through the tab order and pressing Enter/Space does nothing; hovering, right-click (shows only the generic canvas context menu), toggling Comments panel filters, and a full page reload all fail identically.
- The Comments panel permanently shows "No comments" / Open 0 / Resolved 0 / All 0, so no thread ever exists to reply to.

Expected Result:
Placing a comment pin with the Comment tool should open a comment composer (text input plus submit control) so the user can type and submit the comment. Clicking the resulting pin should open the thread with a reply composer that accepts and submits a reply.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed (agent verdict: not-approve)
- Attempt transcripts:
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_10bd0472-789d-477c-9be3-707928f30ed1.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_23bf8dc0-b048-47d8-803a-ebe5904be44b.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_4455ac14-f1aa-412f-8c47-6567f5d25a9c.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_6ac5f2f5-d4bc-45da-b740-7531ca364d72.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_ce424a0d-c8d0-4a39-9e99-371aceed850e.txt`

Agent report (verbatim tail of failing run):

```
I've exhausted every reasonable path, and the comment flow is broken in this app. Here's a summary of what I did and found:

**What worked:**
- Activating the Comment tool (via the toolbar speech-bubble button and via the "C" shortcut) — the tool highlights and the Comments sidebar opens.
- Clicking the canvas with the Comment tool places a blue draft comment pin (a "Draft comment" button appears in the DOM).

**What's broken — the comment composer never appears:**
- After placing the pin, no text input/composer ever renders — not on screen and not anywhere in the DOM. I verified this repeatedly with full accessibility-tree reads (including off-viewport elements): there is no textarea, textbox, or contenteditable related to comments anywhere on the page.
- Attempting to type immediately after placing the pin fails with "no editable element is focused"; character keys instead trigger the app's global tool shortcuts (at one point dropping me into vector-edit mode).
- Clicking the pin (normal click, double-click, slow mouse-down/up, element-reference click) either does nothing or the canvas overlay intercepts the event and simply re-creates the draft pin (confirmed by the button remounting in the DOM).
- Keyboard-focusing the draft pin button through the tab order and pressing Enter/Space did nothing.
- Other attempts: hovering the pin, right-click (only shows the generic canvas context menu), Enter as a global shortcut, placing the pin on an object vs. empty canvas, toggling Comments panel filters, and a full page reload — all with the same result.
- The Comments panel permanently shows "No comments" / Open 0 / Resolved 0 / All 0, confirming nothing can ever be submitted.

Because the composer never opens, I could not type "does this work?" or submit the comment — and therefore no pin/thread exists to click, so the reply "yes, approved" could not be entered or submitted either. The entire requested flow is blocked by this app bug (the draft pin is created, but the comment input UI never mounts).

I cleaned up my test artifacts (deleted the test rectangle and discarded draft pins) before finishing.

The task did not go smoothly: the comment composer never renders after placing a pin with the Comment tool, making it impossible to write, submit, or reply to a comment.

verdict: not-approve
```
