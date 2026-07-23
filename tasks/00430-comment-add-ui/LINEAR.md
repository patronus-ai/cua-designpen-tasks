# DesignPen [comments]: 'comment add' fails QA — 5/5 runs report broken workflow (00430-comment-add-ui)

Description:
Adding a comment via the Comment tool is impossible because the comment composer never renders. The Comment tool itself works (the bottom-toolbar speech-bubble button with tooltip "Comment (C)" highlights blue and the Comments panel opens), and clicking the canvas places a blue "Draft comment" pin, but no text input, textarea, contenteditable, or submit button is ever mounted in the DOM after the pin is placed — verified via full accessibility-tree dumps including off-viewport elements. Keystrokes fall through to global tool shortcuts (e.g. "t" switches to the Text tool and discards the draft), confirming no composer captures input. The bug reproduces after full page reloads, with the tool activated via toolbar or the "C" shortcut, on empty canvas and on top of shapes.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Activate the Comment tool by clicking the speech-bubble button in the bottom toolbar (tooltip "Comment (C)") or pressing "C".
3. Click an empty spot on the canvas to place a comment pin.
4. Attempt to type "header spacing needs review before handoff" into the composer and submit the comment.

Actual Result:

- A blue draft comment pin is placed (a "Draft comment" button appears in the DOM), but the composer never appears — no textarea, input, contenteditable, or submit button exists anywhere in the accessibility tree or page text.
- No editable element ever receives focus; letter keys instead trigger global tool shortcuts (e.g. "t" switched to the Text tool and discarded the draft).
- Plain clicks, slow mouse-down/up clicks, double-clicks, click-drags, clicking the pin directly, Enter, Space, Tab-focus, hovering, page reloads, and reduced browser zoom (checking for a mispositioned popover) all fail to surface a composer; menus and the context menu offer no alternate comment entry point.
- The comment can never be typed or submitted; the Comments panel still shows "Open 0 / No comments."

Expected Result:
After placing a comment pin with the Comment tool, a comment composer (text input with a submit control) should open so the message can be typed and submitted, creating a comment thread visible in the Comments panel.

Estimate: S (2 points) — small handler/layout fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 completed runs failed (`verdict: not-approve`)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_1367a053-3a8c-4665-bcce-652d000adafd.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_42d487db-f9c4-427c-81ed-a02dd843c8d9.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_44877578-6e15-468c-af45-375c5a436b08.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_479fea36-05aa-440a-8f5f-b55d0eb3250e.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_ee2462e0-87de-4fe3-9085-109d8f6fd673.txt`

Agent report (verbatim tail of failing run):

```
I've exhausted every reasonable approach. Here's a summary of what happened:

**What worked:**
1. ✅ **Activated the Comment tool** — clicked the speech-bubble button in the bottom toolbar (tooltip confirmed "Comment (C)"); the tool highlighted blue and the Comments panel opened on the right.
2. ✅ **Clicked an empty spot on the canvas** — a blue draft comment pin was placed (a "Draft comment" button appeared in the DOM, and the pin stayed anchored when the mouse moved away).

**What failed:**
3. ❌ **The composer never appeared.** After placing the pin, no text input/composer ever rendered. I verified this exhaustively:
   - Full accessibility tree dumps (including off-viewport elements) and page-text extraction showed no textarea, input, contenteditable, or submit button — only the pin itself.
   - Tried: plain clicks, slow mouse-down/up clicks, double-clicks, click-drags, clicking/double-clicking the pin directly (both by coordinates and element reference), Enter, Space, Tab-focus, hovering and waiting, and typing — no editable element ever received focus (letter keys instead triggered global tool shortcuts, e.g. "t" switched to the Text tool and discarded the draft).
   - Retried after a full page reload, with the tool activated via both the toolbar and the "C" shortcut, on empty canvas and on top of a test rectangle (the app's shape tools work fine, so the app isn't wholly broken). Also inspected the entire layout at reduced browser zoom for a mispositioned popover and checked menus/context menu for an alternate comment entry point — nothing.
4. ❌ Because no composer exists, I could not type "header spacing needs review before handoff" nor submit it. The Comments panel still shows "Open 0 / No comments."

I cleaned up the test rectangle, leaving the file in its original state.

**Conclusion:** The Comment tool activates and places a draft pin, but the comment composer never renders — an app bug that makes typing and submitting the comment impossible.

verdict: not-approve
```
