# DesignPen [comments]: 'comment deep link open' fails QA — 4/4 runs report broken workflow (00432-comment-deep-link-open-ui)

Description:
Opening a comment via its direct link cannot be tested because the comment-composition UI is broken upstream: after activating the Comment tool (toolbar speech-bubble or "C" shortcut) and clicking the canvas, a blue draft pin appears but no text input box / compose popup ever appears. Repeated accessibility-tree dumps (including off-viewport elements) confirm the page contains no textarea/textbox/contenteditable for comments; the focused element after pin placement is always a plain button. Other inputs in the app work fine (position/color fields accept typing), so the defect is specific to the comment compose UI, and no error toasts appear. Since no comment can be created, the thread's "…" menu and its "copy direct link" option are unreachable and there is no URL to navigate to.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Activate the Comment tool via the speech-bubble icon in the bottom toolbar or the "C" keyboard shortcut.
3. Click on the canvas to place a comment pin.
4. Attempt to type "final copy pending" in the compose popup and submit it.
5. Open the thread's "…" menu, copy the direct link to the comment, and navigate the browser to the copied URL.

Actual Result:

- A blue draft comment pin appears at the clicked location each time, but no text input box / compose popup ever appears — there is nowhere to type "final copy pending" and no submit button.
- Single-click, double-click, right-click (only shows the generic shape context menu), click-and-hold, drag-release, and hovering on the pin all fail; Enter, Space, and Tab do nothing; the page contains no textarea/textbox/contenteditable for comments (confirmed via accessibility-tree dumps including off-viewport elements).
- The bug reproduces identically on empty canvas, on a rectangle, inside a frame, after fresh page reloads, in a fresh browser window, and at 80% browser zoom (no off-screen popup exists); no error toasts appear.
- No thread is ever created, so the "…" menu and "copy direct link" option are unreachable and there is no URL to open.

Expected Result:
Placing a comment pin should open a compose popup where the message can be typed and submitted; the resulting thread's "…" menu should offer a copy-link option, and navigating to that copied URL should open the app focused on that comment thread.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 4 of 4 completed runs failed (`verdict: not-approve`)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_348f9e94-81e3-44fd-a1cc-6f88fb941d74.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_38a5ff19-aca6-420e-8f6d-f1b7f50c4d79.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_5be59547-53f4-404b-bb1a-7d64a5ecf77d.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_9f8c6a92-d9e5-4057-9bf2-b171449f09fe.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_daeed905-d3a8-4612-8cc8-0f8261e663bc.txt`

Agent report (verbatim tail of failing run):

```
I was unable to complete the task due to what appears to be a broken comment-composition UI in the OpenPencil app. Here's a summary of what happened:

**What I did:**
1. **Activated the Comment tool** — both by clicking the speech-bubble icon in the bottom toolbar and via the "C" keyboard shortcut. The tool activated correctly (highlighted blue, Comments sidebar opened showing "Open 0 / Resolved 0 / All 0").
2. **Clicked on the canvas** to place a comment. A blue draft comment pin appeared at the clicked location each time — but **no text input box / compose popup ever appeared**, so there was nowhere to type "final copy pending" or any submit button to press.

**Troubleshooting I attempted (all unsuccessful):**
- Single-click, double-click, right-click (only showed the generic shape context menu), click-and-hold, drag-release, and hovering on the pin
- Pressing Enter, Space, and Tab after placing the pin; typing directly (the focused element was always a plain button — the page contained **no textarea/textbox/contenteditable for comments**, confirmed via repeated accessibility-tree dumps including off-viewport elements)
- Placing pins on empty canvas, on a rectangle, and inside a frame
- Fresh page reloads and a completely fresh browser window (bug reproduced identically)
- Zooming the browser out to 80% to reveal any off-screen popup (none existed)
- Verified other inputs in the app work fine (e.g., position/color fields accept typing), so it's specific to the comment compose UI; no error toasts appeared

Since the comment could never be composed or submitted, no thread was created — therefore the thread's "…" menu and its "copy direct link" option were unreachable, and there was no URL to navigate to. I cleaned up my test artifacts (removed the test rectangle/frame and dismissed draft pins) before finishing.

The core feature required for this task (the comment input popup after placing a pin) never rendered, blocking every subsequent step.

verdict: not-approve
```
