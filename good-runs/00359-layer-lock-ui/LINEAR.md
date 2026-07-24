# DesignPen [layers panel]: 'layer lock' fails QA — 5/5 runs report broken workflow (00359-layer-lock-ui)

Description:
The hover-revealed row controls (lock and hide icons) in the Layers panel do not render visually. When hovering a layer row (e.g. "Rectangle 1"), no lock or hide icon ever appears — verified in both selected and unselected states with zoomed screenshots, and the buttons are absent from the accessibility tree — yet the buttons are actually present and functional: their tooltips ("Hide" and "Lock") pop up when hovering the exact spots where the icons should be, and clicking the invisible lock button successfully locks the layer (the padlock then renders correctly in the locked state). A real user cannot see the control they are supposed to click, making layer locking undiscoverable through normal use.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Select the rectangle tool and draw a large 800 by 600 rectangle as a background.
3. Hover the "Rectangle 1" row in the Layers panel and look for the lock/hide icons on the right side of the row.
4. Hover the spot at the right side of the row where the lock icon should be (a "Lock" tooltip appears) and click there.

Actual Result:

- No lock or hide icon ever renders on hover of the layer row, in either selected or unselected state; the buttons are also absent from the accessibility tree.
- The invisible buttons are present and functional: tooltips "Hide" and "Lock" pop up when hovering their exact positions, and clicking the invisible lock position locks the layer.
- Once locked, the closed padlock icon renders correctly on the row, and clicking the rectangle on canvas no longer selects it (Design panel stays on "Page").

Expected Result:
Hovering a layer row in the Layers panel should visually reveal the lock and hide icons so the user can see and click the lock control to lock the layer.

Estimate: S (2 points) — small handler/layout fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 completed runs failed (`verdict: not-approve`)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_20ed947e-8bb5-4d09-8987-eadbb2d41741.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_5193fb17-65f8-464e-9503-2b0612719e01.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_6828277d-d808-40f8-a72a-6358b468f0bd.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_9794ca57-f3d1-49fb-a755-0bb43c3731e3.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_f2f584b2-8595-445c-a5a7-98a7f3048eaa.txt`

Agent report (verbatim tail of failing run):

```
The task is complete. Here's a summary of what happened:

**What was accomplished:**
1. **Drew the rectangle**: Selected the rectangle tool and dragged on the canvas to create an 800×600 rectangle (confirmed via the "800 × 600" size badge and W=800/H=600 in the Design panel), covering the canvas as a background.
2. **Hovered the layer row**: Hovered over the "Rectangle 1" row in the Layers panel.
3. **Clicked the lock icon**: Clicked the lock control at the right side of the row. The layer is now locked — confirmed by the persistent closed padlock icon on the row, and by the fact that clicking the rectangle on canvas no longer selects it (the Design panel stays on "Page").

**Problem encountered:**
The hover-revealed controls on the layers panel row did not render visually. When hovering the "Rectangle 1" row, no lock or hide icon ever appeared (verified with zoomed screenshots in both selected and unselected states, and the buttons were absent from the accessibility tree). The buttons were actually present and functional — but invisible: I only discovered them because their tooltips ("Hide" and "Lock") popped up when hovering the exact spots where the icons should be. I clicked the invisible lock button at the position where its "Lock" tooltip appeared, which successfully locked the layer (the padlock icon then rendered correctly in the locked state). A real user would not be able to see the lock icon they're supposed to click, so this is a genuine UI rendering bug, even though I was able to work around it and complete the locking.

verdict: not-approve
```
