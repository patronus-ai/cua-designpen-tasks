# DesignPen [clipboard / copy-paste]: 'comment copy link' fails QA — 4/4 runs report broken workflow (00431-comment-copy-link-ui)

Description:
Copying a direct link to a comment is unreachable because comment creation itself is broken: after placing a draft pin with the Comment tool, the comment composer/input never renders. No text field, textarea, contenteditable, or submit/post control appears anywhere in the DOM (confirmed via full accessibility-tree inspection with `filter='all'`), so no comment can ever be created — the Comments panel counts stay at "Open 0 / Resolved 0 / All 0". Consequently the comment pin/thread, its "…" menu, and the copy-link option never come into existence. Right-clicking the pin only shows a generic object menu (Copy/Cut/Paste/Delete, no comment actions), and the "Actions/⌘K" palette is also non-functional.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Activate the Comment tool (speech-bubble icon in the bottom toolbar).
3. Click the canvas to place a comment pin.
4. Attempt to type "check the logo alignment" in the composer and submit the comment.
5. Click the pin to open the thread, open the thread's "…" menu, and choose the copy-link option.

Actual Result:

- Clicking the canvas places a blue draft comment pin (DOM shows `button "Draft comment"`) and the Comments panel opens with filter tabs (Open/Resolved/All), but the comment composer/input never renders — no text field, textarea, contenteditable, or submit/post control appears anywhere.
- Typing is rejected — "no editable element is focused"; letter keys act as tool shortcuts (e.g. "h" switches to Hand tool and discards the draft).
- Right-clicking the pin only shows a generic object menu (Copy/Cut/Paste/Delete), with no comment actions; the main menu "Actions/⌘K" is non-functional; page reloads (including cache-busted), zoom changes, and every other probed UI surface expose no comment-creation path.
- Comment counts remain "Open 0 / Resolved 0 / All 0"; no comment is ever created, so the thread's "…" menu and copy-link option are unreachable.

Expected Result:
Placing a comment pin should open a composer where the message can be typed and submitted; clicking the resulting pin should open the thread, whose "…" menu should offer a copy-link option that copies a direct link to the comment to the clipboard.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 4 of 4 completed runs failed (`verdict: not-approve`)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_13e3d4d6-d285-4dc3-8304-3a1e06b6ebda.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_8b524a6a-b08e-4f65-a8fc-172135f833bd.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_a187a174-80e6-4bdb-be4d-3d37ac6badab.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_a214fd9d-9a91-42dc-b9ea-987f92d1166c.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_c261f822-8ba3-498c-991c-efee1df81fcc.txt`

Agent report (verbatim tail of failing run):

```
Clicking ref_46 produced no visible change (no dropdown, no dialog, counts still 0). The investigation is now fully complete — every plausible path has been exhausted.

## Final Report

**What I attempted:** Place a comment saying "check the logo alignment" with the Comment tool, submit it, open the thread via its pin, and use the thread's "…" menu to copy a direct link.

**What worked:**
- Activating the Comment tool (speech-bubble icon in the bottom toolbar) ✓
- Clicking the canvas places a blue draft comment pin (DOM shows `button "Draft comment"`) ✓
- The Comments panel in the right sidebar opens and shows filter tabs (Open/Resolved/All) ✓

**What failed (blocking bug):** The comment composer/input never renders. After placing the draft pin, no text field, textarea, contenteditable, or submit/post control appears anywhere — confirmed repeatedly via screenshots and full accessibility-tree/DOM inspection (`filter='all'`). I exhaustively tried:
- Clicking, double-clicking, right-clicking the pin (right-click only shows a generic object menu: Copy/Cut/Paste/Delete, no comment actions)
- Keyboard interaction: Enter/Space on the focused pin button, Tab-focus walking, direct typing (rejected — "no editable element is focused"; letter keys act as tool shortcuts, e.g. "h" switches to Hand tool and discards the draft)
- Placing pins on empty canvas and inside a frame; hover, press-hold, and drag-release placement
- Page reloads (including cache-busted), browser zoom changes, the main menu (Actions/⌘K is non-functional), the Comments sidebar, Present/Share/avatar buttons, and an unlabeled top-bar button — none expose a composer or comment-creation path
- Comment counts remained "Open 0 / Resolved 0 / All 0" throughout; no comment was ever created

Because the composer never appears, the comment text could not be entered or submitted, so the pin/thread, its "…" menu, and the copy-link option never came into existence. The task is blocked by what appears to be a broken/unimplemented comment composer in this build of the app.

The comment composer UI fails to render after placing a draft pin, making it impossible to type or submit the comment and reach any of the subsequent steps.

verdict: not-approve
```
