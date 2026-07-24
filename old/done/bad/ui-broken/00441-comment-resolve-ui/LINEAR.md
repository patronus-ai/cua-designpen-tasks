# DesignPen [comments]: 'comment resolve' fails QA — 5/5 runs report broken workflow (00441-comment-resolve-ui)

Description:
In the DesignPen/OpenPencil design app, the Comment tool's draft editor/composer UI fails to render after placing a comment pin, which blocks comment creation, submission, thread opening, and resolution. Activating the Comment tool (speech-bubble icon in the bottom toolbar) works and clicking the canvas places a blue draft pin, but no comment input/editor ever renders — neither next to the pin nor in the sidebar — verified via screenshots, full accessibility-tree reads (including off-viewport elements), and text extraction. Because no comment can be entered or submitted, the resolve step (opening the thread via the pin and clicking its checkmark button) is unreachable. The agent also noted layout bugs in this build: the right sidebar is clipped at the app's right edge (the "All" tab is cut off) and pins get misplaced at non-100% browser zoom.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Activate the Comment tool via the speech-bubble icon in the bottom toolbar; the Comments sidebar opens (Open 0 / Resolved 0 / All 0, "No comments").
3. Click anywhere on the canvas to place a comment pin — a blue draft pin appears.
4. Attempt to type "fix the padding" into the comment composer and submit it.
5. Attempt to click the pin to open its thread.
6. Attempt to click the thread's checkmark (resolve) button to mark the conversation as resolved.

Actual Result:
- After placing the pin, no comment input/editor ever renders — neither next to the pin nor in the sidebar; there is no textarea, input, or submit button anywhere in the DOM.
- Typing after placement fails — no editable element ever receives focus ("no editable element is focused"), and keystrokes instead trigger global tool shortcuts (e.g., "f" switched to the Frame tool and discarded the draft).
- Clicking, double/triple-clicking, press-and-hold, hovering, and keyboard-activating (Enter/Space) the draft pin do nothing; clicks on the canvas merely alternate between placing and discarding the draft; Escape or switching tools discards it.
- Page reload, placing pins at many positions (empty canvas and inside a frame), the right-click context menu, the main menu ("Actions…" is unresponsive), Present mode, and browser zoom changes all fail to reveal a composer.
- The sidebar permanently shows "No comments" (Open 0), so the resolve checkmark is unreachable.
- Additional layout bugs: the right sidebar is clipped at the app's right edge (the "All" tab is cut off), and pins get misplaced at non-100% browser zoom.

Expected Result:
Placing a comment pin with the Comment tool should open a composer so the user can type and submit "fix the padding". Clicking the resulting pin should open the thread, and clicking the thread's checkmark button should mark the conversation as resolved (moving it to the Resolved filter).

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed (agent verdict: not-approve)
- Attempt transcripts:
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_4afe721c-1086-4a1c-8c24-65eef39e99ba.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_594db205-7f55-49ea-9b8b-8f7112a16aa5.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_8490d000-8c40-4001-8f28-01cf710c829d.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_d3153eb7-975f-4360-8e01-df563a701191.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_ed9cd1b3-a72f-4162-8e22-7aefcc1f3357.txt`

Agent report (verbatim tail of failing run):

```
I've exhaustively tested the Comment tool flow, and the comment composer never appears, making the task impossible to complete. Here's a summary of what I did and found:

**What worked:**
- Activating the Comment tool (speech-bubble icon in the bottom toolbar) — it highlights and opens the Comments sidebar (Open 0 / Resolved 0 / All 0, "No comments").
- Clicking the canvas with the Comment tool places a blue draft pin (a "Draft comment" button appears in the accessibility tree).

**What's broken:**
- After placing the pin, **no comment input/editor ever renders** — neither next to the pin nor in the sidebar. I verified via screenshots, zooming into the pin area, full accessibility-tree reads (including off-viewport elements), and text extraction: there is no textarea, input, or submit button anywhere in the DOM.
- Typing after placement fails — no editable element ever receives focus ("no editable element is focused"), and keystrokes instead trigger global tool shortcuts (e.g., "f" switched to the Frame tool and discarded the draft).
- Clicking, double/triple-clicking, press-and-hold, hovering, and keyboard-activating (Enter/Space) the draft pin do nothing; clicks on the canvas merely alternate between placing and discarding the draft. Escape or switching tools discards it.
- I also tried: a fresh page reload, placing pins at many canvas positions (empty canvas and inside a frame I created), the right-click context menu, the main menu ("Actions…" is unresponsive), Present mode, and browser zoom changes to reveal mispositioned UI — no comment composer exists anywhere. Incidentally, the right sidebar is clipped at the app's right edge (the "All" tab is cut off), and pins get misplaced at non-100% browser zoom, suggesting layout/positioning bugs in this build.

Because the comment text can never be entered or submitted, no comment thread or pin ever gets created (the sidebar permanently shows "No comments", Open 0), so the subsequent steps — opening the thread via the pin and clicking the checkmark (resolve) button — are unreachable.

What went wrong: the Comment tool's draft editor/composer UI fails to render after placing a comment pin, blocking comment creation, submission, thread opening, and resolution.

verdict: not-approve
```
