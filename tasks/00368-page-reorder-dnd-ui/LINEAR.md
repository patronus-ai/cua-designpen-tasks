# DesignPen [pages]: 'page reorder dnd' fails QA — 5/5 runs report broken workflow (00368-page-reorder-dnd-ui)

Description:
Drag-and-drop reordering in the Pages panel list is broken: dragging a page row enters the drag state (row fades with a drag outline), but the drop never registers — no insertion indicator ever appears, the order never changes, and the row stays stuck in its "dragging" visual state after mouse release until a subsequent click resets it. There is also no alternative reorder path: the row's context menu offers only "Rename page" and "Delete page", and neither the main menu, the Actions palette, nor any keyboard combination provides a move/reorder command. Adding and renaming pages works fine and persists.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Click the "+" button in the Pages panel to add a second page ("Page 2").
3. Rename the new page to "Archive" (its name field is editable on creation; type "Archive" and confirm).
4. Press and drag the "Archive" row upward in the pages list and release it above "Page 1" (try the upper half of Page 1's row, its center, or the gap below the "PAGES" header).
5. Observe the list order and the dragged row's visual state after releasing.

Actual Result:

- The drag starts (row becomes faded with a drag outline) but the drop never registers: no insertion indicator is shown, the order never changes, and the row remains stuck in its "dragging" visual state after mouse release until a subsequent click resets it.
- All alternative approaches failed: standard drag gesture, slow press-move-release with pauses and small increments, various drop points, dragging Page 1 down instead, a two-stage drag, keyboard reordering (Space + arrows, Ctrl/Alt/Shift+Arrow combos), the row context menu (only "Rename page" and "Delete page"), the main menu and Actions palette (no reorder command), and a full reload retry.
- Final state: both pages exist but "Archive" still sits below "Page 1" in the original order.

Expected Result:
Dragging a page row in the Pages panel should show an insertion indicator and, on release, reorder the list so "Archive" sits above the original page.

Estimate: M (3 points) — scoped feature fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 completed runs failed (`verdict: not-approve`)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_45767b6f-773c-49e6-9758-1bf6b3952c7d.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_48e2295d-7505-4363-8beb-c7b14e107b31.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_79cf49b4-379e-45a0-890c-bdbd96703dd0.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_ab530764-7ade-41f0-b3f4-07c850143142.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_da30e12e-9cd8-4a0f-bc28-19eab4506f20.txt`

Agent report (verbatim tail of failing run):

```
I've completed my attempts. Here's a summary of the task:

**What succeeded:**
1. ✅ **Added a second page** — clicked the "+" button in the Pages panel, which created "Page 2".
2. ✅ **Renamed it to "Archive"** — the new page's name field was editable on creation; I typed "Archive" and confirmed. The rename persisted (verified even after a page reload).

**What failed:**
3. ❌ **Dragging the Archive row above "Page 1"** — I could not get the pages list to reorder. When dragging the row, the app enters a drag state (the row becomes faded with a drag outline), but the drop never registers: the list never shows an insertion indicator, the order never changes, and the row remains stuck in its "dragging" visual state even after the mouse button is released, until a subsequent click resets it.

I tried many approaches: a standard drag gesture, slow manual press–move–release with pauses and small increments, releasing at various drop points (upper half of Page 1's row, its center, the boundary gap below the "PAGES" header), dragging in the opposite direction (Page 1 down below Archive), a two-stage drag, keyboard-based reordering (Space + arrow keys, Ctrl/Alt/Shift+Arrow combos), the row's context menu (it only offers "Rename page" and "Delete page" — no move/reorder option), the app's main menu and Actions palette (no reorder command), and reloading the app for a clean retry. In every case the pages list stayed in the original order: "Page 1" first, "Archive" second.

The final state: both pages exist ("Page 1" and "Archive"), but "Archive" still sits **below** the original page because the drag-to-reorder interaction never completes — the drag starts and then hangs without ever accepting a drop, which appears to be a bug or broken drag-and-drop handling in the pages list.

verdict: not-approve
```
