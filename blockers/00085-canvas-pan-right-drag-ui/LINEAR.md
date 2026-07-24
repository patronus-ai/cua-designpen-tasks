# DesignPen [canvas interactions]: 'canvas pan right drag' fails QA — 3/3 runs report broken workflow (00085-canvas-pan-right-drag-ui)

Description:
The "Right-click and drag to pan" feature could not be exercised or verified. Enabling the preference works (main menu → Preferences → "Right-click and drag to pan", checkmark confirmed), and the viewport can pan in general (scroll-wheel panned ~300px), but the right-button drag gesture itself never panned the view: `right_click` is an atomic press+release that opens the app's context menu, and no automation primitive exists to hold the right button while moving (no `right_click_drag` / `right_mouse_down` / `right_mouse_up`). The agent flags this as an automation-environment blocker rather than a confirmed app bug — but the feature's key verification (view panned by right-button drag) never happened, and the "Ctrl+click opens right click menus" preference also failed to produce a menu on ctrl+click (modifier keys on mouse actions are ignored).

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Open the main menu (OpenPencil logo, top-left) and go to Preferences.
3. Enable "Right-click and drag to pan" (verify the checkmark in the Preferences submenu).
4. Hold the right mouse button down on the canvas and drag a few hundred pixels.
5. Observe the rulers/viewport for panning.

Actual Result:
- A `right_click` (atomic press+release) opens the app's context menu — correct behavior for a click — and subsequent mouse movement of several hundred pixels never pans; rulers unchanged, verified multiple times.
- The automation tooling provides no way to hold the right mouse button during movement: no `right_click_drag` / `right_mouse_down` / `right_mouse_up` actions (schema rejects them); a `start_coordinate` passed to `right_click` is ignored.
- All workarounds blocked: modifier keys on mouse actions are ignored (the "Ctrl+click opens right click menus" preference produced no menu on ctrl+click); trusted CDP input via the local DevTools frontend failed (Chrome 149 rejects the debugger WebSocket origin, `--remote-allow-origins` not set); the hosted DevTools frontend is unreachable (no internet); `javascript:`/`data:` injection blocked by tool policy.
- General panning does work (a scroll-wheel diagnostic panned the view ~300px vertically, rulers shifting 100→400), so only the right-drag gesture is unverified.

Expected Result:
With the "Right-click and drag to pan" preference enabled, holding the right mouse button on the canvas and dragging should pan the view (rulers shift) instead of, or in addition to, showing the context menu on a plain right-click.

Estimate: XS (1 point) — likely environment/tooling limitation, verify manually and re-scope

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 3 of 3 completed runs failed (`verdict: not-approve`)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_02880065-34bb-4eba-bbb1-4b008fd89d19.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_90ec939f-3d53-4186-8430-61daf4969583.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_a9240d75-763f-4b3c-9275-4411addf7821.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_b4d73a01-0430-42fa-8e18-c627d751635b.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_f9ef79b1-249b-449e-9fd3-ade879f2fd57.txt`

Agent report (verbatim tail of failing run):

```
The context menu is dismissed and the app is in a clean final state. Here's a summary of the task:

## Summary

**What succeeded:**
1. ✅ Opened the main menu (OpenPencil logo, top-left) → **Preferences**
2. ✅ Enabled **"Right-click and drag to pan"** — verified twice via the checkmark in the Preferences submenu
3. ✅ Confirmed the canvas viewport *can* pan in general (a scroll-wheel diagnostic panned the view ~300px vertically, confirmed by the rulers shifting from 100→400)

**What failed — the right-button drag itself:**
The browser automation tooling provides no way to hold the right mouse button down while moving the cursor, so the requested gesture could not be performed:
- `right_click` is an atomic press+release: it opens the app's context menu (correct app behavior for a click), and subsequent mouse movement of several hundred pixels never pans — verified multiple times, rulers unchanged.
- There is no `right_click_drag` / `right_mouse_down` / `right_mouse_up` action (schema rejects them); only left-button drag primitives exist. A `start_coordinate` passed to `right_click` is ignored.
- Workarounds were all blocked: modifier keys on mouse actions are ignored (tested via the app's "Ctrl+click opens right click menus" preference — no menu appeared on ctrl+click; I restored that pref to off afterwards); dispatching trusted CDP input via the local DevTools frontend failed (Chrome 149 rejects the debugger WebSocket origin — `--remote-allow-origins` not set); the hosted DevTools frontend is unreachable (sandbox has no internet); and `javascript:`/`data:` injection is blocked by tool policy.

So the preference was enabled successfully, but I could not actually exercise/verify the right-click-drag panning feature — the view was never panned by a right-button drag. This is an automation-environment blocker rather than an observed app bug, but it means the task's key verification step could not be completed.

The right-drag pan gesture could not be performed because the automation tooling cannot hold the right mouse button during movement, and every workaround (CDP via DevTools, modifier emulation, JS injection) was blocked in this sandbox.

verdict: not-approve
```
