# DesignPen [text & typography]: 'text align vertical' fails QA — 5/5 runs report broken workflow (00298-text-align-vertical-ui)

Description:
The vertical text alignment toggles (align-top / align-middle / align-bottom) in the Typography → Alignment row of the properties panel update and persist their UI state but have no effect on canvas rendering: text stays pinned to the top of a fixed-height text box regardless of the selected toggle. The Code tab confirms the state never reaches the output — the generated CSS shows only `width: 85px; height: 200px;` with no vertical alignment property. As a secondary issue, the vertical alignment toggles overflow the properties panel and are clipped/hidden by default, requiring horizontal scrolling of the alignment row to reach them.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Create a text layer with the text "Bottom shelf" using the Text tool.
3. Switch the layer's resizing mode to "fixed size" and set its height to 200px via the Dimensions H field, so the box is much taller than the ~17px text.
4. In the Typography → Alignment row of the properties panel, horizontally scroll the alignment row to reveal the clipped vertical alignment toggles (align-top / align-middle / align-bottom).
5. Click the align-bottom toggle.
6. Observe the canvas; optionally check the Code tab for the generated CSS.

Actual Result:
- The align-bottom toggle becomes selected/highlighted and the selection persists across deselecting and re-selecting the layer, but the text "Bottom shelf" remains pinned to the top of the 200px-tall box.
- Align-middle also does not move the text.
- Panning the canvas to force a re-render, deselect/re-select, and entering/exiting text edit mode make no difference.
- The Code tab shows only `width: 85px; height: 200px;` with no vertical alignment property applied.
- Minor UX issue: the vertical alignment toggles overflow the properties panel and are clipped/hidden by default, requiring horizontal scrolling of the alignment row to reach them.

Expected Result:
Selecting align-bottom (or align-middle) should visibly reposition the text within its fixed-height box on the canvas and emit the corresponding vertical alignment in the generated code, and the toggles should be visible in the panel without horizontal scrolling.

Estimate: M (3 points) — scoped feature fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 completed runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_34c9e119-e7b6-4627-b346-1b05e8c7dc51.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_49935c00-7e6d-44e4-8080-a7f7d030a1e6.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_5cf42c14-3df1-4eff-b32d-178f026617b1.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_89671db7-e838-448a-92f9-8fe9f7672419.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_c90f1cc4-aad2-43d8-9e1f-0ead446366af.txt`

Agent report (verbatim tail of failing run):

```
I completed all the requested steps, but encountered a functional bug. Here's a summary:

**What I did:**
1. ✅ Created a text layer with the text "Bottom shelf" using the Text tool
2. ✅ Switched the layer's resizing mode to "fixed size" and set its height to 200px via the Dimensions H field (box became 85 × 200, much taller than the ~17px text)
3. ✅ Located the vertical alignment toggles in the Typography → Alignment row of the properties panel (they were initially cut off and required horizontal scrolling of the alignment row to reveal: align-top / align-middle / align-bottom icons)
4. ✅ Clicked the align-bottom toggle — it became selected/highlighted, and the selection state persists across deselecting and re-selecting the layer

**The problem:** The vertical alignment has no visual effect on the canvas. The text "Bottom shelf" remains pinned to the **top** of the 200px-tall box, even though the align-bottom toggle is active. I verified this thoroughly:
- Tried align-middle too — the text also didn't move
- Panned the canvas to force a full re-render — text still top-aligned
- Deselected/re-selected the layer and re-entered/exited text edit mode — no change
- Checked the Code tab — the generated CSS shows only `width: 85px; height: 200px;` with no vertical alignment property applied

Additionally, a minor UX issue: the vertical alignment toggles overflow the properties panel and are clipped/hidden by default, requiring horizontal scrolling of the alignment row to reach them.

The toggle's state updates and persists in the UI, but the actual text rendering never aligns to the bottom of the box, so the feature does not work as intended.

verdict: not-approve
```
