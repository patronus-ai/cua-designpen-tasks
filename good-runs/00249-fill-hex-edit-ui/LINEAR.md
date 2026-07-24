# DesignPen [fills & color]: 'fill hex edit' fails QA — 5/5 runs report broken workflow (00249-fill-hex-edit-ui)

Description:
At the 1280x720 viewport, the right Design panel is clipped and the hex input in the Fill row renders with essentially zero width — it is invisible and unclickable (only the fill swatch, a truncated opacity field showing "10…", and icons are visible). Clicking the hex input even via its DOM reference fails to give it focus; the only workaround is focusing the adjacent Opacity field and pressing Shift+Tab to reach the hidden input. Even then, typing was unreliable: one attempt mangled the value (fill briefly turned black/000000) and another dropped a keystroke ("FF00FF" registered as "F00FF"). The setting can eventually be committed, but the direct hex-edit-in-the-fill-row workflow is broken by the panel layout.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Draw a rectangle on the canvas.
3. In the right Design panel, locate the Fill row (do not open the full color picker).
4. Attempt to click the hex input in the Fill row and type FF00FF.
5. If the input cannot be focused, focus the adjacent Opacity field and press Shift+Tab to reach the hidden hex input, then type FF00FF and press Enter.

Actual Result:

- The hex input in the Fill row renders with essentially zero width at 1280x720 — completely invisible and unclickable; only the swatch, a truncated opacity field ("10…"), and icons are visible.
- Clicking the hex input via its DOM reference failed to give it focus.
- After reaching the input via Shift+Tab from the Opacity field: first attempt mangled the value (fill briefly turned black/000000); second attempt dropped a typed character ("FF00FF" registered as "F00FF"), requiring a manual fix before committing with Enter.

Expected Result:
The hex input in the Fill row should be visible, clickable, and focusable at the 1280x720 viewport, and typing FF00FF followed by Enter should set the fill without dropped keystrokes or intermediate wrong values.

Estimate: M (3 points) — scoped feature fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 completed runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_321085bd-34a7-4493-beb0-76cad13cc562.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_7815e641-1afc-4513-9c09-8831e5016f64.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_9c092c2f-005b-4340-8a2c-ab4ce10f869d.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_a4ab3287-7246-4898-8cb1-55c4916de1c8.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_b349adda-5618-408d-89c0-94491cd0d3ab.txt`

Agent report (verbatim tail of failing run):

```
The task is complete. Final state:
- **Rectangle drawn**: "Rectangle 1" (250×170) on the canvas
- **Fill set via hex input**: The hex input in the Fill row now contains "FF00FF", the fill swatch is magenta, and the rectangle renders in magenta (FF00FF) — all done without opening the full color picker

**Summary of how it went:** The rectangle drawing worked fine, but setting the hex value was problematic due to a UI bug. At this viewport size (1280×720), the right panel is clipped and the hex input in the Fill row is rendered with essentially zero width — it's completely invisible and unclickable (only the swatch, a truncated opacity field "10…", and icons are visible). Clicking the hex input via its DOM reference failed to give it focus. I had to work around this by focusing the adjacent Opacity field and pressing shift+Tab to reach the hidden hex input. Even then, my first attempt mangled the value (the fill briefly turned black/000000), and on the second attempt a typed character was dropped ("FF00FF" registered as "F00FF"), requiring a manual fix before committing with Enter. The end result is correct, but the hex input being invisible/unclickable in the fill row and the dropped keystroke were real problems.

verdict: not-approve
```
