# DesignPen [clipboard / copy-paste]: 'paste to replace' fails QA — 5/5 runs report broken workflow (00109-paste-to-replace-ui)

Description:
The context-menu "Paste to replace" action fails: after copying a circle via right-click > Copy, selecting a rectangle and choosing right-click > "Paste to replace" shows a red error banner "Clipboard access is blocked in this browser context" and the rectangle is not replaced. No paste path worked as a fallback — Ctrl+V and Edit > Paste both did nothing (Layers panel still shows only "Rectangle 1" and "Ellipse 1"). The clipboard read API is unavailable on the app's insecure HTTP origin, blocking all paste functionality including "Paste to replace".

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Select the Ellipse tool and drag on the canvas to draw a circle (e.g. 120x120 "Ellipse 1").
3. Right-click the circle and choose "Copy" (no error is shown).
4. Select the rectangle tool and draw a rectangle (e.g. 160x100 "Rectangle 1"), then select it.
5. Right-click the rectangle and choose "Paste to replace".

Actual Result:

- A red error banner appears: "Clipboard access is blocked in this browser context", and the rectangle is not replaced.
- Retrying the full copy → paste-to-replace flow produces the same error.
- Diagnostics: Ctrl+V and Main menu Edit > Paste also did nothing — the layers panel still shows only "Rectangle 1" and "Ellipse 1", with no circle copy replacing the rectangle. No paste operation works (clipboard read API unavailable on the insecure HTTP origin).

Expected Result:
"Paste to replace" on a selected rectangle, after copying a circle, should swap the rectangle out for a copy of the circle with no error.

Estimate: M (3 points) — scoped feature fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_04dabfc7-94a2-4bf8-a020-9f73e1676c9b.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_491a361e-d3d3-453f-889f-97dba1fa1efd.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_73757171-ec55-4fe6-b906-01ab2d56cb6f.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_9c533b11-c627-4b18-9947-d3151a47544b.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_c293729b-d48e-4910-95b4-682969b62310.txt`

Agent report (verbatim tail of failing run):

```
Paste via the Edit menu also did nothing — the layers panel still shows only "Rectangle 1" and "Ellipse 1", and the rectangle remains on the canvas unreplaced. The clipboard functionality is blocked in this environment, so "Paste to replace" cannot complete.

Summary of what I did and found:
1. ✅ Drew a 120×120 circle (Ellipse 1) using the Ellipse tool.
2. ✅ Right-clicked the circle and chose "Copy" — no error was shown.
3. ✅ Drew a 160×100 rectangle (Rectangle 1) and selected it.
4. ❌ Right-clicked the rectangle and chose "Paste to replace" — a red error banner appeared: **"Clipboard access is blocked in this browser context"**, and the rectangle was not replaced.
5. I retried the full copy → paste-to-replace flow a second time (same error), and also tried Ctrl+V and the app menu's Edit > Paste as diagnostics — no paste operation works; the document still contains the original Rectangle 1 and Ellipse 1, with no circle copy replacing the rectangle.

The core requested action failed: the app's paste functionality (including "Paste to replace") is blocked by the browser context (the clipboard read API is unavailable on this insecure HTTP origin), so the rectangle could not be swapped for a copy of the circle.

verdict: not-approve
```
