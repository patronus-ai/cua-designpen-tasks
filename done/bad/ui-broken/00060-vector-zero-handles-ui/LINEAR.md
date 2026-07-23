# DesignPen [vector editing]: 'vector zero handles' fails QA — 4/4 runs report broken workflow (00060-vector-zero-handles-ui)

Description:
There is no handle-zeroing action in the right-hand vector edit panel. With a smooth point (or a handle endpoint) selected in vector edit mode, the panel only offers a Mirroring radiogroup ("No mirroring", "Mirror angle", "Mirror angle and length") and a Radius field — none of which zero the direction handles (mirroring options change the constraint mode but leave handle geometry intact, verified via SVG output). The action is also absent from tooltips, the "..." object menu, the app's main menu (its "Vector" submenu is permanently disabled), and the edit toolbar's "More" menu. The goal was only achievable via a workaround: selecting each direction-handle endpoint and pressing Delete. Several secondary bugs were hit along the way (Move-tool click silently inserting an anchor, stale selection after undo causing Delete to remove the whole vector, and a stale Code-panel SVG view during edit mode).

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Press P and draw a curvy path using click-drag points to create smooth vertices (e.g. a 4-point wave).
3. Press Enter to commit, then exit the editor ("Vector 1" created).
4. Double-click the path to enter vector edit mode (floating Move/Lasso/Paint/Bend/Cut toolbar appears).
5. Select one of the smooth points (e.g. a crest anchor) — point-level controls appear in the right-hand Design panel.
6. Look in the right-hand vector edit panel for an action to zero out the point's direction handles; also check tooltips, the "..." object menu, the main menu's Vector submenu, and the edit toolbar's "More" menu.

Actual Result:
- The described "handle action" does not exist in the right-hand vector edit panel. With a point or handle endpoint selected, the panel only offers a Mirroring radiogroup ("No mirroring", "Mirror angle", "Mirror angle and length") and a Radius field; clicking each mirroring option changes the constraint mode but leaves handle geometry intact (confirmed via SVG output).
- The action is absent everywhere else checked: accessibility tree (including hidden elements), tooltips, the "..." object menu, the main menu (the "Vector" submenu is permanently disabled), and the edit toolbar's "More" menu.
- Workaround required: selecting each direction-handle endpoint and pressing Delete zeroed both handles and committed correctly.
- Secondary bugs: a single Move-tool click on a path segment silently inserted an extra anchor point; after an undo inside edit mode the selection state was stale and Delete removed the entire vector object; the Code panel's SVG view shows stale path data while vector edit mode is active, only refreshing after committing.

Expected Result:
The right-hand vector edit panel should expose a handle action that, for the selected smooth point, zeroes out both direction handles (turning it into a sharp corner), with the change reflected in the path geometry.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 4 of 4 completed runs failed (`verdict: not-approve`)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_24b868e0-4799-40fd-8b68-314967e05972.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_68862854-39f5-4777-b217-de4459f43482.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_75c44536-4b09-427e-9a6e-e9011d987bb7.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_95118019-2b45-41c0-b280-14ba9c05651a.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_9e77b670-86d9-4a65-8c5e-508ce4a4077a.txt`

Agent report (verbatim tail of failing run):

```
The task is complete to the extent the app allows. Final state: a committed curvy path ("Vector 1") whose crest point — originally a smooth drag-created point — now has both direction handles zeroed (sharp corner), verified in the generated SVG where both control points adjacent to the crest anchor (131,1) coincide with the anchor: `M1 101C41 41 131 1 131 1M131 1C131 1 211 151 281 151M281 151C351 151 361 1 431 1`.

**Summary of what happened:**
1. ✅ Drew a 4-point curvy wave with the Pen tool using click-drag smooth vertices and committed it (Enter, then exited the editor).
2. ✅ Double-clicked the path to enter vector edit mode (floating Move/Lasso/Paint/Bend/Cut toolbar appeared).
3. ✅ Selected a smooth point (the crest anchor), which revealed point-level controls in the right-hand Design panel.
4. ❌ **The described "handle action" does not exist in the right-hand vector edit panel.** With a point (or a handle endpoint) selected, the panel only offers a *Mirroring* radiogroup ("No mirroring", "Mirror angle", "Mirror angle and length") and a *Radius* field — verified exhaustively via the accessibility tree (including hidden elements), tooltips, the "..." object menu, the app's main menu (its "Vector" submenu is permanently disabled), and the edit toolbar's "More" menu. None of these zero the handles (confirmed via the SVG output: clicking each mirroring option changes the constraint mode but leaves handle geometry intact). I had to achieve the goal with a canvas workaround instead: selecting each direction-handle endpoint and pressing Delete, which zeroed both handles; the result committed correctly.

**Other bugs hit along the way:** a single Move-tool click on a path segment silently inserted an extra anchor point (required undo); after an undo inside edit mode the selection state was stale and a Delete keypress deleted the entire vector object instead of the selected handle (recovered via undo); and the Code panel's SVG view shows stale path data while vector edit mode is active, only refreshing after committing.

Because the core instructed interaction — a handle-zeroing action in the right-hand vector edit panel — is missing from the app and the goal was only achievable through a workaround (plus the unexpected point-insertion, stale-selection deletion, and stale Code panel issues), the task did not go smoothly.

verdict: not-approve
```
