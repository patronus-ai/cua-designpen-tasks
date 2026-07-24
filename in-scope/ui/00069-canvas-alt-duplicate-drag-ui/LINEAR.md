# DesignPen [canvas interactions]: 'canvas alt duplicate drag' fails QA — 3/5 runs report broken workflow (00069-canvas-alt-duplicate-drag-ui)

Description:
Alt+drag duplication of a shape on the canvas could not be triggered: every Alt-modified drag variant behaved as a plain move — the square just moved with no copy peeling off. The agent's controlled experiments showed the automation layer silently drops modifier keys on all drag-type mouse actions (shift+click multi-selects correctly, but an otherwise-identical shift-drag and shift on granular mouse down/up do not), so Alt never reaches the app during a drag; the app also showed no alt-duplicate behavior on any drag variant that could be produced. The intended end state was only reachable via the right-click → Duplicate (Ctrl+D) menu plus a normal drag. Note this may be an automation-harness modifier-stripping issue rather than (or in addition to) an app bug, and 2 of 5 runs did approve.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Select the rectangle tool and draw a 100x100 square (e.g. Rectangle 1 at X=154, Y=250).
3. Hold Alt/Option, press the left mouse button on the square, and drag it about 200px to the right.
4. Release the mouse and check whether a copy was created (Layers panel / canvas) while the original stayed in place.

Actual Result:
- `left_click_drag` with an `alt` modifier: the square just moved, no copy peeled off.
- Granular `left_mouse_down` → `mouse_move` → `left_mouse_up` with `alt` on every event: plain move again.
- Ending the drag with an alt-modified click so the final mouseup carries altKey: plain move (and it even skipped the undo history).
- `hold_key` with Alt mid-drag: rejected by the tooling ("Unknown key can't be held: alt").
- Tapping `key: alt` mid-drag: no copy spawned; it also switched the active tool to Text as a side effect.
- Controlled experiments proved the automation layer silently drops modifier keys on all drag-type mouse actions (shift+`left_click` multi-selects, but shift on any drag variant does not), so Alt can never reach the app during a drag; no alt-duplicate behavior was observed on any producible drag variant.
- Fallback that worked: right-click → Duplicate (Ctrl+D), then a normal drag 200px right — original at (154, 250), copy at (354, 250), both 100x100.

Expected Result:
Holding Alt/Option while dragging a selected shape should peel off a duplicate that follows the drag while the original stays in place, without needing the Duplicate menu command.

Estimate: XS (1 point) — likely environment/tooling limitation, verify manually and re-scope

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 3 of 5 completed runs failed (`verdict: not-approve`; 2 approved)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_04dcf587-0376-47ae-8aed-ae587dfe5d74.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_34ce7cc6-29b0-40e6-b583-821872971acd.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_8f4267a3-f68b-4e5e-8b72-2abe41ef7c12.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_a73f80b5-2dd1-42ce-90a8-9c5b414c2fc0.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_ff95691b-b1be-48ce-9947-f25717909af2.txt`

Agent report (verbatim tail of failing run):

```
Both squares are now side by side: the original at (154, 250) and the copy at (354, 250) — a 200px offset, both exactly 100×100.

**Summary of what happened:**

1. **Drawing the square — worked.** I selected the rectangle tool and drew Rectangle 1, verified as exactly 100×100 at X=154, Y=250.

2. **Alt-drag duplicate — could not be performed as a gesture.** I attempted it many ways:
   - `left_click_drag` with an `alt` modifier → the square just moved (no copy peeled off)
   - Granular `left_mouse_down` → `mouse_move` → `left_mouse_up` with `alt` on every event → plain move again
   - Ending the drag with an alt-modified click so the final mouseup carries altKey → plain move (and it even skipped the undo history)
   - `hold_key` with Alt mid-drag → rejected by the tooling ("Unknown key can't be held: alt")
   - Tapping `key: alt` mid-drag → no copy spawned; worse, it switched the active tool to Text as a side effect
   
   I then ran controlled experiments that isolated the cause: shift+`left_click` correctly multi-selects (modifiers DO work on plain clicks), but an otherwise-identical zero-distance shift-drag and shift on granular mouse down/up do NOT multi-select — proving the automation layer silently drops modifier keys on all drag-type mouse actions. Alt therefore can never reach the app during a drag, making the requested "hold Alt and drag" gesture physically impossible with the available tools (I also confirmed the app shows no alt-duplicate behavior on any drag variant I could produce).

3. **Fallback — achieved the intended end state.** I used the app's own right-click → Duplicate (Ctrl+D), then dragged the copy 200px to the right with a normal drag. Result: original Rectangle 1 untouched at (154, 250), and copy Rectangle 2 at (354, 250) — exactly 200px to the right, same 100×100 size, matching what an alt-drag copy would have produced.

The final document state matches the goal, but the specific interaction requested (Alt held during drag causing a copy to peel off) could not be executed — modifier keys are stripped from drag actions by the automation harness, so the alt-drag duplication never triggered and I had to fall back to menu-based Duplicate + move.

verdict: not-approve
```
