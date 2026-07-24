# DesignPen [preferences]: 'pref snap to objects' fails QA — 3/5 runs report broken workflow (00183-pref-snap-to-objects-ui)

Description:
Snap-to-objects can intermittently fail to commit the snapped position on mouse release: on the first snap-drag right after shape creation, the pink snap guides and snapped preview displayed correctly during the drag, but releasing the mouse committed the square at the raw pointer position (X=203, Y=101 — a 3px gap) instead of the shown snapped position (X=200, Y=100). During that same drag the Position panel displayed stale coordinates (280,130) instead of live values, suggesting a transient state glitch on the first drag after creation. Subsequent drags, including deliberate 2-3px-off-target release tests, committed the snap correctly, so the failure is intermittent and tied to the first drag. The "Snap to objects" preference itself (on by default) is fine.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Open Main menu (logo) > Preferences and confirm "Snap to objects" is checked (on by default).
3. Draw a rectangle with the R tool and set exact values in the Design panel: X=100, Y=100, W=100, H=100.
4. Draw another 100x100 square nearby (e.g. at X=280, Y=130).
5. Immediately drag the second square toward the first until pink snap guides appear (shared edge, top/bottom/center alignment) and the preview shows it flush against the first square's right edge, then release with the pointer 2-3px off the exact target.
6. Check the committed X/Y in the Design panel; also watch the Position panel during the drag.

Actual Result:
- On the very first snap-drag after shape creation, the snap guides and snapped preview displayed correctly while dragging, but on mouse release the square was committed at the raw pointer position X=203, Y=101 — a 3px gap, ignoring the shown snap.
- During that drag the Position panel displayed stale coordinates (280,130) instead of live values.
- The drag had to be redone; all subsequent snap releases (including two deliberate reproduction tests releasing 2-3px off target, one with an identical pause before release) committed the snapped position (200,100) correctly — the issue was intermittent and not reproducible afterward.

Expected Result:
Releasing the mouse while the snap guides and snapped preview are showing should always commit the displayed snapped position (left edge flush at x=200, no gap), including on the first drag after shape creation, and the Position panel should show live coordinates during the drag.

Estimate: M (3 points) — scoped feature fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 3 of 5 runs failed (2 approved)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_523241e4-cc15-4510-8367-6cb8d30a780a.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_5b08702e-f221-48e3-98fd-706474e04a49.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_c71c5a25-13d1-4743-812f-5f13f963fb8d.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_cf37e06d-ac9d-432b-a9d7-e325f528a22c.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_d8f567f9-29f3-4538-8c5d-1704a6d2e1de.txt`

Agent report (verbatim tail of failing run):

```
The task is complete. Final state verified:

**What was done:**
1. **Preference check:** Opened Main menu (logo) > Preferences and confirmed "Snap to objects" was already enabled (checkmark shown by default) — left it untouched.
2. **First square:** Drew a rectangle with the R tool, then set exact values in the Design panel: X=100, Y=100, W=100, H=100.
3. **Second square:** Drew another 100×100 square nearby at X=280, Y=130.
4. **Snap drag:** Dragged the second square toward the first; pink snap guides appeared (shared edge, top/bottom/center alignment) and it snapped flush against the first square's right edge. Final verified position: X=200, Y=100, 100×100 — its left edge exactly touches the first square's right edge at x=200, no gap (the two squares render as one seamless 200×100 block). I also verified snap commit works by releasing 2–3px off target in follow-up drags — both committed to exactly (200,100).

**Problem encountered:** On the very first snap-drag, the snap guides and snapped preview displayed correctly while dragging, but on mouse release the square was committed at the raw pointer position X=203, Y=101 — a 3px gap, ignoring the shown snap. During that drag the Position panel also displayed stale coordinates (280,130) instead of live values, suggesting a transient state glitch on the first drag right after shape creation. I had to redo the drag; all subsequent snap releases (including two deliberate reproduction tests releasing 2–3px off target, one with an identical pause before release) committed the snapped position correctly, so the issue was intermittent and not reproducible afterward. The end result is correct, but the snap-on-release did visibly fail once despite guides indicating a snap.

verdict: not-approve
```
