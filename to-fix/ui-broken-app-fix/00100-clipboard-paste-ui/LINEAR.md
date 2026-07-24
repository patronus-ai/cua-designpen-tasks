# DesignPen [clipboard / copy-paste]: 'right-click Copy' fails QA — 5/5 runs report broken workflow (00100-clipboard-paste-ui)

Description:
The canvas context-menu clipboard flow is broken: right-click > "Copy" does not actually place the selected object on the clipboard, so the subsequent right-click > "Paste here" produces nothing. The copy fails silently — no error toast, no new layer, and the Layers panel keeps showing only the single original rectangle. Multiple runs isolated the culprit with controlled comparisons: keyboard Ctrl+C/Ctrl+V works and pastes a duplicate, and "Paste here" works when the clipboard was populated by a keyboard Ctrl+C — but any paste (either "Paste here" or Ctrl+V) that follows a context-menu "Copy" pastes nothing. The context-menu Copy handler therefore needs to write to the same internal/DOM clipboard the keyboard path uses (or the menu item should be disabled). A secondary nit: when "Paste here" does work, it pastes at a fixed offset rather than at the clicked location.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Select the rectangle tool from the toolbar and drag on the canvas to draw one rectangle ("Rectangle 1").
3. Right-click the rectangle and choose "Copy" from the context menu (no error is shown at this step).
4. Right-click on empty canvas and choose "Paste here" (the item is enabled).

Actual Result:

- After "Paste here", nothing is pasted — no new shape appears and the Layers panel still shows only the single "Rectangle 1". No error message is shown. Reproduced multiple times, including with pixel-perfect clicks on the exact menu-item elements.
- Control tests confirm the copy source is the problem, not paste: keyboard Ctrl+C -> Ctrl+V pastes a duplicate, and "Paste here" pastes a duplicate when the clipboard was populated via Ctrl+C. Only context-menu "Copy" -> any paste yields nothing.
- Secondary: when "Paste here" works (after a keyboard copy), it pastes at a fixed offset rather than at the clicked "here" location.

Expected Result:
Right-click > Copy followed by right-click > "Paste here" should paste a copy of the rectangle at the clicked location, matching the behavior of the working Ctrl+C/Ctrl+V shortcuts, with a new layer appearing in the Layers panel.

Estimate: S (2 points) — small handler fix to route context-menu Copy through the same clipboard path the keyboard shortcut uses.

Evidence:

- QA job `db76a8af-97c9-41fb-bbba-42d2d887d5b8`, model `claude-opus-4-8` — 5 of 5 runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_a1cb84e8-5486-4e92-88bd-5e59cd217712.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_77bf552f-0530-4e02-bb1a-cf66216b3514.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_744da66b-15f4-490e-a3c4-a415eca2408a.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_21623757-86b4-4358-bf67-43edd02e76ca.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_df9b22e0-2d31-4d91-a9e2-cc23d5598ad7.txt`

Agent report (verbatim tail of failing run):

```
I have thoroughly tested the requested flow. Here is my summary.

## What I did
1. Drew one rectangle — Selected the rectangle tool and dragged out a 200 x 150 rectangle ("Rectangle 1"). This worked fine.
2. Copied it via right-click > Copy — Right-clicked the rectangle and selected "Copy" from the context menu (clicked the exact menu item).
3. Right-clicked on empty canvas and chose "Paste here" — The context menu appeared, "Paste here" was enabled, and I clicked it (using the exact menu item element).

## What went wrong
After "Paste here", no rectangle was pasted — the canvas and the Layers panel still showed only the single original "Rectangle 1". I reproduced this several times, including with pixel-perfect clicks on the exact menu elements.

To isolate the cause, I ran a controlled comparison:
- right-click Copy -> right-click Paste here = nothing pasted
- right-click Copy -> Ctrl+V = nothing pasted
- Ctrl+C -> right-click Paste here = pasted a duplicate
- Ctrl+C -> Ctrl+V = pasted a duplicate

This proves the defect is in the right-click context-menu "Copy" action: it does not actually place the object on the clipboard, so any subsequent paste (including "Paste here") produces nothing. The "Paste here" command itself works — but only when the copy was done with the keyboard (Ctrl+C). (I undid my diagnostic pastes, so the document is left with the single original rectangle.)

Because the task specifically requires copying via right-click > Copy, and that action is broken, the requested flow cannot be completed — right-click Copy followed by "Paste here" yields no duplicate.

verdict: not-approve
```
