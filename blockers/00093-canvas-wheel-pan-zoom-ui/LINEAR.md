# DesignPen [canvas interactions]: 'canvas wheel pan zoom' fails QA — 5/5 runs report broken workflow (00093-canvas-wheel-pan-zoom-ui)

Description:
The Ctrl/Cmd+scroll zoom gesture on the WebGL canvas could not be exercised or verified. Plain mouse-wheel panning over the canvas works correctly, and the app's zoom commands work via the View menu ("Zoom In (Ctrl+=)"), but the prescribed Ctrl+scroll zoom gesture never reached the app: the automation tooling drops modifier keys from wheel events, so every modified scroll was delivered as a plain wheel event and just panned the canvas. Additionally, pressing Ctrl+= as a keyboard shortcut was intercepted by the browser as page zoom (125%) instead of reaching the app. The app's own ctrl+scroll zoom behavior therefore remains unverified; the failure may be an environment/tooling limitation rather than an app defect, but the requested interaction path is unusable in this QA context.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Scroll the mouse wheel over the canvas in several directions to pan the view (works — ruler coordinates shift).
3. Hold Ctrl (or Cmd) and scroll the mouse wheel over the canvas, expecting the canvas to zoom in.
4. Alternatively, press the app's Ctrl+= zoom shortcut on the keyboard.

Actual Result:

- Ctrl/Cmd/Shift + scroll is dispatched as a plain wheel event — modifiers are dropped entirely, so the canvas just pans and zoom stays unchanged. This was reproduced with "ctrl", "Control", "cmd", "shift", and "ctrl+cmd" modifier variants.
- The tooling's hold-key action rejects bare modifiers: "Unknown key can't be held: ctrl/Control".
- Pressing Ctrl+= via the key action was intercepted as browser page zoom (125%) instead of reaching the app, and had to be reset with Ctrl+0.
- Workaround: View menu > "Zoom In (Ctrl+=)" works correctly; invoking it four times stepped canvas zoom 100% → 125% → 156% → 195% → ~244%.
- Plain wheel panning works perfectly in every direction.

Expected Result:
Holding Ctrl (or Cmd) while scrolling over the canvas should zoom the canvas view in (app-level zoom, not browser page zoom), with the modified wheel event reaching the app so the session finishes noticeably tighter than it started.

Estimate: XS (1 point) — likely environment/tooling limitation, verify manually and re-scope

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_1d6621f2-9103-4f07-88fe-36a13a1e39c3.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_43ee5041-2651-4c61-8740-4b28c3bf9d8f.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_57bd5b83-7c1f-47ec-8deb-592d1323e760.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_8ab075d5-7479-4460-99ec-484c92b9a5ca.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_d342ae05-3edd-4704-9e30-b39bf100c81e.txt`

Agent report (verbatim tail of failing run):

```
Final state confirmed: the horizontal ruler now spans ~700–1040 across the canvas (with 50-unit gradations at ~122px spacing ≈ 244% zoom), compared to the initial view spanning ~100–820 at 100% zoom. The view is ~2.4× tighter than at the start, and the canvas was panned in multiple directions along the way.

**Summary of what happened:**

1. **Panning via scroll — worked perfectly.** Plain mouse-wheel scrolling over the canvas panned it smoothly in every direction I tried (down, right, up), confirmed by the ruler coordinates shifting each time.

2. **Ctrl/Cmd + scroll to zoom — could not be performed.** My browser-control tooling's `scroll` action silently ignores modifier keys: I tried attaching "ctrl", "Control", "cmd", "shift", and "ctrl+cmd" to scroll events, and every single one was dispatched as a plain wheel event (the canvas just panned, zoom unchanged). A diagnostic with shift+scroll confirmed modifiers are dropped entirely. The `hold_key` action also rejects holding bare modifier keys ("Unknown key can't be held: ctrl/Control"). Pressing the app's Ctrl+= zoom shortcut via the key action got intercepted as *browser page zoom* (125%) instead of reaching the app, which I had to reset with Ctrl+0.

3. **Workaround used for the end state:** The app's View menu exposes "Zoom In (Ctrl+=)", which works correctly — I invoked it four times, stepping the canvas zoom 100% → 125% → 156% → 195% → ~244%, so the session does finish zoomed in noticeably tighter than it started.

The app itself appears fine (scroll-panning works; its zoom commands work via the menu), but the specifically requested Ctrl+scroll zoom gesture was never actually delivered to the app because the automation tooling cannot synthesize modifier+wheel events — I had to fall back to the menu command, and the app's ctrl+scroll behavior itself went unverified. Since I hit this blocker on the prescribed interaction, I can't call the run fully smooth.

verdict: not-approve
```
