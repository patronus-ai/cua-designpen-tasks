# DesignPen [comments]: 'comment open thread' fails QA — 5/5 runs report broken workflow (00439-comment-open-thread-ui)

Description:
Closing and reopening a comment thread popover cannot be tested because no comment can be created: after activating the Comment tool (toolbar speech-bubble button or "C" shortcut) and clicking the canvas, a blue draft pin appears but the comment input popover/composer never renders. Full DOM/accessibility-tree inspection (including off-screen elements) shows no textarea, input, or contenteditable element ever mounts; keystrokes after pin placement are captured as global tool shortcuts (e.g., "o" switched to the Ellipse tool). As a control, the Text tool accepted typed text normally, proving the problem is specific to the comment composer rather than general input handling. Pressing Space on the focused pin actually cancelled the draft. With no comment ever submitted, the close/reopen-thread steps are impossible.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Activate the Comment tool via the speech-bubble toolbar button or the "C" shortcut.
3. Click the canvas to place a comment pin.
4. Attempt to type "open me later" in the composer and submit the comment.
5. Click an empty area of the canvas to close the thread popover, then click the comment's pin again to reopen the conversation.

Actual Result:

- Clicking the canvas places a blue draft comment pin (a "Draft comment" button appears in the accessibility tree), but no comment input popover/composer ever appears, so "open me later" cannot be typed or submitted.
- No textarea, input, or contenteditable element ever mounts anywhere in the full DOM/accessibility tree (including off-screen elements).
- Typing after pin placement is captured as global tool shortcuts (e.g., "o" switched to the Ellipse tool), confirming no composer input exists or has focus; pressing Space on the focused pin button cancelled the draft.
- Single-clicking, double-clicking, mouse-down-holding the pin (by coordinates and element reference), Enter on the pin, hovering, click-dragging, waiting for async loading, a full page reload, and commenting on an actual object (a test rectangle) all fail identically. As a control, the Text tool accepted typed text normally.
- The comments list remains "No comments"; the close-popover and reopen-via-pin steps are impossible.

Expected Result:
Placing a comment pin should open a composer so the message can be typed and submitted; clicking empty canvas should close the thread popover, and clicking the comment's pin again should reopen the conversation.

Estimate: S (2 points) — small handler/layout fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 completed runs failed (`verdict: not-approve`)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_56f71c17-02bc-473c-af76-3d5a8bfb454b.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_62835d68-a3d2-46d4-9cec-8d3e691f1a54.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_7ed88c34-c8b5-4d68-952d-5b442be08ccc.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_d75cdf8a-3491-4bee-91a7-b0802e3bdf22.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_defc836b-ce79-444b-8af9-7ebfb601e9fc.txt`

Agent report (verbatim tail of failing run):

```
I was unable to complete the task due to what appears to be a broken comment composer in this OpenPencil build. Here's a summary of what happened:

**What worked:**
- Activating the Comment tool (both via the speech-bubble toolbar button and the "C" shortcut) — the tool highlights and the Comments sidebar opens showing "Open 0 / Resolved 0 / All 0, No comments"
- Clicking the canvas with the Comment tool places a blue draft comment pin (a "Draft comment" button appears in the accessibility tree)

**What failed:**
- No comment input popover/composer ever appears after placing the pin, so there was no way to type "open me later" or submit it. I tried:
  - Single-clicking, double-clicking, and mouse-down-holding the pin (by coordinates and by element reference)
  - Pressing Enter/Space on the focused pin button (Space actually cancelled the draft)
  - Hovering, click-dragging, waiting several seconds for async loading, and a full page reload with a fresh retry
  - Commenting on an actual object (a test rectangle) instead of empty canvas — same result
  - Inspecting the full DOM/accessibility tree (including off-screen elements): no textarea, input, or contenteditable element ever mounts anywhere
  - Typing directly after pin placement — keystrokes are captured as global tool shortcuts (e.g., "o" switched to the Ellipse tool), confirming no composer input exists or has focus
- As a control, the Text tool accepted typed text normally, proving the problem is specific to the comment composer, not general input handling.

Because the comment could never be written or submitted, the follow-up steps (closing the thread popover by clicking empty canvas and reopening it via the pin) were also impossible. The comments list remained "No comments" throughout. I cleaned up my test artifacts before finishing.

The comment composer popover fails to render after placing a comment pin, blocking the entire task flow.

verdict: not-approve
```
