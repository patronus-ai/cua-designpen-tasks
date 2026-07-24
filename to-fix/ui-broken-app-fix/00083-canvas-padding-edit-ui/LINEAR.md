# DesignPen [auto-layout canvas]: 'on-canvas padding editor' fails QA — 1/5 runs report broken workflow (00083-canvas-padding-edit-ui)

Description:
The on-canvas padding band for auto-layout frames is not rendered when the frame's padding is 0 (the default for a freshly created auto-layout frame). With a new auto-layout frame selected, hovering just inside the left edge shows no padding band or highlight, and double-clicking the inner-left edge simply deselects the frame instead of opening the on-canvas padding editor popover. The documented flow (select frame → hover left padding band → double-click → edit value) is therefore impossible on a default frame. The agent could only reach the popover after first setting a non-zero padding (20) via the properties panel — only then did the left padding band render (blue hatched strip with a drag handle), after which hover, double-click, and setting the value to 40 all worked correctly. Either a zero-width hit-zone should still be hoverable/clickable at 0 padding, or the band rendering has a missing minimum hit area.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Draw a frame (e.g., 300x250) and enable auto-layout on it, then draw a rectangle inside it. Leave padding at its default of 0.
3. Select the frame (e.g., via the Layers panel).
4. Hover along the inside of the frame's left edge, where the left padding band should appear.
5. Double-click the inner-left edge to open the on-canvas padding editor popover.

Actual Result:

- At the default 0 padding, no padding band renders on the left edge (the 0-padding bottom edge likewise shows no band); hovering produces no highlight.
- Double-clicking the inner-left edge deselects the frame instead of opening the padding editor popover.
- Workaround: after setting left padding to a non-zero value (20) via the properties panel, the band renders and hover/double-click/popover/value entry all work (value set to exactly 40).

Expected Result:
With an auto-layout frame selected, the left padding band (or at least a hoverable hit zone) should be available even when padding is 0, so double-clicking it opens the on-canvas padding editor popover without requiring a properties-panel workaround.

Estimate: M (3 points) — hit-zone/rendering fix for the zero-padding case in one canvas overlay component

Evidence:

- QA job `db76a8af-97c9-41fb-bbba-42d2d887d5b8`, model `claude-opus-4-8` — 1 of 5 runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_9b4b889e-68f5-438d-863f-0b1f57ec78ae.txt`

Agent report (verbatim tail of failing run):

```
The final state is verified: **Left padding = 40**, with Top = 0, Right = 0, and Bottom = 0. The rectangle inside the auto-layout frame is now inset 40px from the left edge.

## Summary

Here's what I did and what I found:

1. **Built the auto-layout frame with a rectangle** — Created "Frame 1" (300×250), enabled auto-layout (horizontal flow), and drew "Rectangle 1" inside it. This worked smoothly. ✓
2. **Selected the frame** — Selected Frame 1 via the Layers panel. ✓
3. **Hover the padding band on the left edge** — ⚠️ **This is where I hit a problem.** On the freshly-built frame (which defaults to **0 padding**), there was **no padding band to hover** along the left edge. Hovering anywhere just inside the left edge produced no band/highlight, and when I double-clicked the inner-left edge as instructed, it simply **deselected the frame** instead of opening any editor. I confirmed this is the tool's behavior (the 0-padding bottom edge likewise showed no band).
4. **Workaround** — To make the band appear, I had to first set a small non-zero padding (20) via the properties panel. Only then did the left padding band render (a blue hatched strip with a drag handle).
5. **Double-click → popover → set 40** — With the band now visible, hovering highlighted it, double-clicking opened the on-canvas padding editor popover (showing the left-padding icon and value), and I set the value to exactly **40**. ✓ I then reset the incidental right padding back to 0 for a clean result.

**What went wrong:** The task's described flow assumes a hoverable padding band exists on the left edge of the selected auto-layout frame, but on a default 0-padding frame no such band is rendered — hovering reveals nothing and double-clicking just deselects the frame. I could only complete the step after introducing non-zero padding via the properties panel (a workaround not part of the described instructions). The on-canvas padding editor popover itself worked correctly once a band existed, and the left padding is now exactly 40.

verdict: not-approve
```
