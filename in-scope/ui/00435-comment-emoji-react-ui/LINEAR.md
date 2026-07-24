# DesignPen [comments]: 'comment emoji react' fails QA — 4/4 runs report broken workflow (00435-comment-emoji-react-ui)

Description:
Adding an emoji reaction to a comment message is impossible because comment creation is broken: the Comment tool activates and clicking the canvas places a blue draft pin (visible on screen and as a "Draft comment" button in the accessibility tree), but the composer/text input never renders or mounts — no textbox, textarea, or editable element exists anywhere in the DOM, page text, or visually. Typing fails with "no editable element is focused", any subsequent canvas click dismisses the draft, and keyboard letters still trigger tool shortcuts, proving no composer ever captures input. Since no comment thread/message is ever created (Comments panel stays at "Open 0 / Resolved 0 / All 0"), the add-reaction (👍) step is also impossible.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Select the Comment tool (speech-bubble icon in the bottom toolbar).
3. Click the canvas to place a comment pin.
4. Attempt to type "ready for handoff" in the composer and submit the comment.
5. Click the pin to open the thread, then use the add-reaction button on the message to add a thumbs-up (👍) emoji reaction.

Actual Result:

- A blue draft pin appears at the click location, but the comment composer/text input never appears — no textbox, textarea, or editable element anywhere in the DOM/accessibility tree, page text, or visually (verified via screenshots, zoomed inspection, `read_page` with filter "all", `get_page_text`, and `find`).
- Typing fails ("no editable element is focused"), so "ready for handoff" can never be entered.
- Clicking the pin (by coordinates and element ref), double-click, right-click (only the generic canvas context menu), Enter/Space, Tab-focus traversal, hovering, slow clicks, drags, Escape/re-place cycles, panning, browser zoom-out, collapsing/expanding sidebars, and multiple full page reloads all fail; any subsequent canvas click dismisses the draft, and keyboard letters still trigger tool shortcuts.
- The Comments panel count stays at 0 — no thread or message ever exists, so the add-reaction (👍) step is impossible.

Expected Result:
Placing a comment pin should open a composer so "ready for handoff" can be typed and submitted; clicking the pin should open the thread, and the message's add-reaction button should let the user attach a 👍 emoji reaction to it.

Estimate: S (2 points) — small handler/layout fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 4 of 4 completed runs failed (`verdict: not-approve`)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_36f9a08a-5762-4680-9f5b-21cfd59e2591.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_597a7ff0-d440-4779-8bc6-595a40c85b19.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_6437d2f7-851d-477c-96aa-399cb8ed051c.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_a73040c7-ddc1-4bd4-9aa7-60d212c412f4.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_ff5c3f12-acd2-4b2e-8366-61abdac1ec4f.txt`

Agent report (verbatim tail of failing run):

```
I have now exhaustively re-verified the issue after a clean reload. The evidence is conclusive, so I'll finalize my report.

**What I did and found:**

1. **Selected the Comment tool** (speech-bubble icon in the bottom toolbar) — it activates correctly (highlights blue, Comments panel opens showing "Open 0 / Resolved 0 / All 0 — No comments").
2. **Clicked the canvas to place a comment** — a blue draft pin appears at the click location (visible on screen and as a "Draft comment" button in the accessibility tree), **but the comment composer/text input never appears**. There is no textbox, textarea, or editable element anywhere in the DOM/accessibility tree, page text, or visually (verified via screenshots, zoomed inspection, `read_page` with filter "all", `get_page_text`, and `find`).
3. Because no input exists, typing fails ("no editable element is focused"), so the text "ready for handoff" could never be entered and no comment could be submitted.
4. I tried every plausible workaround across this session: clicking the pin (by coordinates and by element ref), double-click, right-click (only shows the generic canvas context menu), Enter/Space on the pin, Tab-focus traversal, hovering, slow clicks, drags, Escape/re-place cycles, panning, browser zoom-out to reveal off-screen UI, collapsing/expanding sidebars, multiple full page reloads, and probing for invisible off-screen composers. In every case the pin is only a draft: any subsequent canvas click dismisses it, keyboard letters still trigger tool shortcuts (proving no composer captures input), and the Comments panel count stays at 0 — no comment thread is ever created.

**Conclusion:** The task could not be completed due to an app bug in OpenPencil — the Comment tool places a draft pin but its composer UI never renders/mounts, so there is no way to enter or submit the comment text. Consequently the pin/thread with a message never exists, and the add-reaction (👍) step is also impossible.

The comment composer never appeared after placing a comment pin, so the comment "ready for handoff" could not be typed or submitted, and no thread/message existed to react to with 👍.

verdict: not-approve
```
