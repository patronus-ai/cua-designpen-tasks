# DesignPen [fills & color]: 'fill detach style' fails QA — 4/5 runs report broken workflow (00332-fill-detach-style-ui)

Description:
The apply/detach paint-style flow itself works (create style, apply via the fill apply-styles popover, detach via "No style", recolor), but the surrounding UI is seriously broken. The page-level "Styles + → Color" menu item silently does nothing (no dialog, no style created). After using the apply-styles popover, an "Apply styles" tooltip got stuck on screen and the entire right design panel rendered shifted/clipped horizontally; while in that glitched state the app crashed to a blank page (about:blank) mid-task. The document was auto-restored from a snapshot after re-navigation, but the crash and silent menu failure are real bugs.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. With nothing selected, try the page-level "Styles + → Color" menu item — observe it does nothing (no dialog, no style created).
3. Draw a rectangle (200x150) on the canvas.
4. Create a paint style (e.g. "My Paint Style", color D4D4D4) via the fill color-picker's Libraries "+" → Create style flow.
5. Apply the style to the rectangle's fill via the fill "Apply styles" popover.
6. Observe the UI after using the popover: a stuck "Apply styles" tooltip and a horizontally shifted/clipped right design panel; continue interacting — the app can crash to about:blank.
7. Re-navigate to the app (document auto-restores from a snapshot named "snapshot").
8. Detach the style via the "No style" action in the apply-styles panel, then recolor the rectangle to #0000FF via the fill color picker's hex field.

Actual Result:

- The page-level "Styles + → Color" menu item silently did nothing (tried 3 times; no style created, no dialog opened) — the fill color-picker's Libraries "+" flow had to be used instead.
- After using the apply-styles popover, an "Apply styles" tooltip got stuck on screen and the entire right design panel rendered shifted/clipped horizontally.
- While the UI was in that glitched state, the app crashed to a blank page (about:blank) mid-task; after re-navigating, the document was auto-restored from a snapshot (file renamed "snapshot").
- The core detach flow worked once recovered: the fill reverted to a plain color preserving the value, was recolored to #0000FF, and "My Paint Style" kept its original gray (D4D4D4).

Expected Result:
The "Styles + → Color" menu creates a style, the apply-styles popover leaves no stuck tooltips or panel layout corruption, and the app never crashes to about:blank during the apply/detach workflow.

Estimate: L (5 points) — state/undo consistency issue, needs investigation across the edit pipeline

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 4 of 5 completed runs failed (1 approved)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_b79ed330-a47d-4580-9b6f-ef6c0e771cb3.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_c621c030-31d0-405c-befc-ebd17e9beff0.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_db8e9460-442b-4d60-b2f7-346cea5a6431.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_f36588d1-6659-4945-9116-97f908e690d2.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_fe269f14-7772-4b21-b5b3-d90c2049b644.txt`

Agent report (verbatim tail of failing run):

```
The task is now complete. Final verification confirms:
- **Fill row**: blue swatch (#0000FF) with plain hex/opacity inputs — no style linked (detached state)
- **Color styles**: "My Paint Style" still exists with its original gray color (D4D4D4)
- **Code tab**: background color confirmed as #0000FF

**Summary of what was done:**
1. Created a rectangle (200×150) on the canvas.
2. Created a paint style "My Paint Style" (color D4D4D4) via the fill's style popover (+ → Create style).
3. Explicitly applied the style to the rectangle's fill via the fill "Apply styles" popover (clicked "My Paint Style"; fill row then displayed the style name with a checkmark in the popover).
4. Detached the style using the detach action ("No style") in the same apply-styles panel — the fill reverted to a plain color while preserving the value.
5. Recolored the rectangle to pure blue #0000FF via the fill color picker's hex field, verified in the Code tab.

**Problems encountered along the way:**
- The page-level "Styles + → Color" menu item silently did nothing (tried 3 times, no style was created and no dialog opened) — I had to use the fill color-picker's Libraries "+" flow instead.
- After using the apply-styles popover, an "Apply styles" tooltip got stuck on screen and the entire right design panel rendered shifted/clipped horizontally.
- Most seriously, while the UI was in that glitched state, the app crashed to a blank page (about:blank) mid-task. After re-navigating, the document was auto-restored from a snapshot (file renamed "snapshot") with the rectangle and style intact, and I was able to finish all steps successfully.

Although the end state is fully correct, the silent menu failure, stuck-tooltip/panel-shift glitch, and the page crash are real bugs hit during the workflow.

verdict: not-approve
```
