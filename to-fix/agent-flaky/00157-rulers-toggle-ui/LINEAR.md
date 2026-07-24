# DesignPen [view & UI toggles]: 'rulers toggle' fails QA — 5/5 runs report broken workflow (00157-rulers-toggle-ui)

Description:
The "Rulers" checkbox in the zoom dropdown (top-right of the editor) is cosmetic — it is not wired to ruler visibility. Unchecking it removes the checkmark but the rulers stay rendered along the canvas edges, even after forcing a canvas redraw by panning (the ruler numbers update, proving a re-render happened while the option was off). Additionally, the zoom dropdown button ("100%") is clipped off-screen behind the avatar/Share area at 1280px viewport width and only becomes visible after scrolling the header bar, and Escape does not close the dropdown menu.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Locate the zoom dropdown ("100%") in the top-right corner of the editor — note it may be clipped off-screen behind the avatar/Share area and require scrolling the header bar to reveal.
3. Open the dropdown; it shows Zoom in/out, Zoom to fit, presets (50/100/200%), plus "Rulers" and "Multiplayer cursors" options. Observe "Rulers" is already checked by default and rulers are visible.
4. Uncheck "Rulers".
5. Observe the canvas edges; pan the canvas to force a redraw.

Actual Result:
- "Rulers" is already checked by default and rulers are already visible, so there is nothing to "turn on".
- Unchecking "Rulers" removes the checkmark, but the rulers stay visible on the canvas — even after forcing a canvas redraw by panning (ruler numbers updated, proving a re-render happened while the option was off). The checkbox is not wired to ruler visibility.
- The zoom dropdown button was clipped off-screen at 1280px width, and Escape did not close the menu.

Expected Result:
Toggling the "Rulers" checkbox should show/hide the measurement rulers along the canvas edges — unchecking it should remove the rulers, checking it should render them.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_00d91d8d-1338-4649-8425-6cbccda7ba0d.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_2197fb09-1ebf-48fe-831c-f213aab2fcd0.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_5193d894-da58-4303-90a1-e9d0d7661a66.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_b925033e-571e-4ae4-9ff9-308d67e6ee73.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_d54169d3-94bc-47ed-bdd2-0fe93e2ce134.txt`

Agent report (verbatim tail of failing run):

```
I've completed the task and verified the final state. Here's a summary of what happened:

**What I did:**
1. Located the zoom dropdown ("100%") in the top-right corner of the editor — note that at this viewport width it was initially clipped off-screen behind the avatar/Share area and only became visible after scrolling the header bar.
2. Opened the dropdown, which shows Zoom in/out, Zoom to fit, presets (50/100/200%), plus "Rulers" and "Multiplayer cursors" options.
3. Found that **"Rulers" was already checked by default**, and rulers were already visible along the canvas edges — so there was nothing to actually "turn on."
4. To verify the control works, I unchecked it: the checkmark disappeared, **but the rulers stayed visible on the canvas**, even after forcing a canvas redraw by panning (the ruler numbers updated, proving a re-render happened while the option was off). The checkbox appears cosmetic — it isn't wired to ruler visibility.
5. I re-checked "Rulers" and confirmed the checkmark persists, leaving the requested end state: checkbox checked ✓ and rulers displayed along the top and left canvas edges.

**Problems encountered:**
- The "Rulers" checkbox was already checked on first open (task premise of "turning on" didn't hold).
- Bug: toggling the "Rulers" checkbox has no effect on the canvas — rulers remain rendered even when the option is unchecked, so the setting doesn't actually control ruler visibility.
- Minor quirks: the zoom dropdown button was clipped off-screen at 1280px width, and Escape did not close the menu.

While the final state matches what was requested (Rulers checked, rulers visible), the feature itself is broken — the checkbox doesn't genuinely control the rulers.

verdict: not-approve
```
