# DesignPen [dev mode]: 'remove dev status' fails QA — 5/5 runs report broken workflow (00140-remove-dev-status-ui)

Description:
The canvas right-click context menu for a frame that is marked "ready for dev" grows taller than the 720px viewport, and its last item, "Remove dev status", renders below the bottom edge of the screen. The menu is not scrollable, clicking the off-screen item via its DOM reference silently does nothing (the menu closes and the dev badge remains), and arrow-key navigation does not move through the menu — the keypress leaks to the canvas and nudges the selected frame by 1px. The item is only reachable via a workaround such as zooming the browser to 80% so the whole menu fits on screen.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Press F to activate the frame tool and draw a top-level frame on the canvas (e.g. 300 × 250).
3. Right-click the frame and choose "Mark as ready for dev" — a green dev badge appears on the frame.
4. Right-click the frame again and try to click "Remove dev status" at the bottom of the context menu.

Actual Result:
- After the frame is marked ready for dev, the right-click context menu is taller than the 720px viewport, and the last item "Remove dev status" renders just below the bottom edge of the screen.
- The menu is not scrollable.
- Clicking the off-screen menu item via its DOM reference silently does nothing — the menu just closes and the green badge remains.
- Keyboard navigation with arrow keys does not navigate the menu; the keypress leaks to the canvas and nudges the selected frame by 1px (requiring an undo).
- The step could only be completed via a workaround: zooming the browser to 80% so the entire menu fit on screen, clicking "Remove dev status", then restoring 100% zoom and the frame's original position.

Expected Result:
The "Remove dev status" context menu item should be reachable at the normal 1280x720 viewport size — the menu should fit on screen, scroll, or support keyboard navigation — and clicking it should remove the green dev badge from the frame.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_1d55de23-b4f6-49cc-b3d0-f5577cb1069c.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_31400f4b-34ad-46b8-abcc-3b79e2ae29a3.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_60b3aef5-6576-454e-bad9-1cf057b01fbf.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_8685ecda-8961-4b87-9a9b-494bd848ca93.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_de6c1398-75a9-43dc-a9c5-d03feeaca14d.txt`

Agent report (verbatim tail of failing run):

```
All steps are complete and the UI is back at 100% zoom. Final state verified:
- **Frame 1** (300 × 250) was drawn as a top-level frame using the frame tool (F)
- Right-click → **Mark as ready for dev** worked — a green dev badge appeared on the frame
- Right-click → **Remove dev status** worked — the green badge is now gone

**Summary of how it went:**

The first two steps were smooth. However, removing the dev status hit a real problem: after marking the frame ready for dev, the right-click context menu grew taller than the 720px viewport, and the last item "Remove dev status" rendered just below the bottom edge of the screen. The menu was not scrollable, clicking the off-screen menu item via its DOM reference silently did nothing (the menu just closed and the badge remained), and attempting keyboard navigation with arrow keys didn't navigate the menu — instead the keypress leaked to the canvas and nudged the selected frame by 1px (which I had to undo). I could only complete the step by using a workaround: zooming the browser to 80% so the entire menu fit on screen, then clicking "Remove dev status", and afterwards restoring 100% zoom and the frame's original position.

So while the final result is correct, the "Remove dev status" menu item was effectively unreachable at the normal viewport size due to the context menu overflowing off-screen with no scrolling or keyboard support — a genuine UI bug/blocker that required a workaround.

verdict: not-approve
```
