# DesignPen [canvas interactions]: 'canvas pinch zoom' fails QA — 5/5 runs report broken workflow (00086-canvas-pinch-zoom-ui)

Description:
The pinch-zoom gesture (Ctrl+scroll on the canvas) could not be performed: modifier keys are silently dropped from the environment's scroll action, so Ctrl+scroll arrives as a plain wheel event which pans the canvas instead of zooming (zoom stayed at 100%). The app's Ctrl+= zoom-in shortcut is intercepted by the harness as browser page zoom before reaching the app, and bare `=` / `+` keys do nothing. The end goal (zoom noticeably above default) was only achievable via the app's own zoom UI (Zoom in button and the zoom percentage field). This is largely an automation-environment modifier limitation, but the app also offers no reachable keyboard path to zoom in.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Hold Ctrl and scroll on the canvas (the trackpad-pinch equivalent) to zoom in.
3. Observe the zoom indicator (top right) and the rulers.
4. Alternatively try the app's zoom-in shortcut Ctrl+= (shown in its menu), and bare `=` / `+` keys.

Actual Result:
- `scroll` with modifier text `"ctrl"`, `"Control"`, and `"meta"`: in every case the modifier was silently dropped and the event arrived as a plain wheel scroll, which panned the canvas instead of zooming (verified via rulers; zoom stayed 100%).
- Keyboard `ctrl+=` was intercepted by the harness as browser page zoom (went to 125%, reset with `ctrl+0`) and never reached the app.
- App-level `=` / `+` keys did nothing.
- Fallback that worked: the app's own zoom control — "Zoom in" (100% → 125%) and typing 250% in the zoom field — reached 250% zoom, confirmed by the zoom indicator and rulers (~800+ canvas units across → ~250).

Expected Result:
Ctrl+scroll (pinch) over the canvas should zoom the canvas view in around the cursor, raising the zoom indicator noticeably above the default 100%.

Estimate: XS (1 point) — likely environment/tooling limitation, verify manually and re-scope

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 completed runs failed (`verdict: not-approve`)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_29c5e06a-776f-4f8e-a7df-4427d7a618fd.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_4b8ebfbe-08a1-4a34-8691-04b60f5c91c1.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_ceffb6d2-a278-42f6-be3a-1edbd227e506.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_de2e8319-d194-4c2d-a02c-16a42d287484.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_eda5f0cc-b44e-4bbb-8efd-4ef7a237f567.txt`

Agent report (verbatim tail of failing run):

```
The canvas is now zoomed to 250% — noticeably closer than the default 100%. The zoom indicator (top right) reads 250%, and the rulers confirm it: the viewport that originally showed ~800+ canvas units across now shows only ~250 units.

**Summary of what happened:**

1. **Attempted the requested pinch gesture (Ctrl+scroll) first**, multiple ways:
   - `scroll` with modifier text `"ctrl"`, `"Control"`, and `"meta"` — in every case the modifier was silently dropped and the event arrived as a plain wheel scroll, which **panned** the canvas instead of zooming (verified via rulers; zoom stayed 100%). This environment's scroll action simply cannot carry modifier keys.
   - Keyboard `ctrl+=` (the app's zoom-in shortcut shown in its menu) was intercepted by the harness as **browser page zoom** (it went to 125%, which I reset to 100% with `ctrl+0`) and never reached the app.
   - App-level `=` / `+` keys did nothing.
2. **Fallback:** Used the app's own zoom control (the handler a pinch would drive) — clicked "Zoom in" (100% → 125%), then entered 250% in the zoom field. Final canvas zoom: **250%**.

So the end goal (canvas noticeably closer than default zoom) was achieved, but the literal pinch/Ctrl+scroll gesture could not be performed: the environment's scroll primitive doesn't support modifier keys, and Ctrl+= is consumed as browser-level zoom before reaching the page. I had to substitute the app's zoom menu/percentage input for the gesture.

verdict: not-approve
```
