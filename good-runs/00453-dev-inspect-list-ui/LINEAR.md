# DesignPen [dev mode]: 'dev inspect list' fails QA — 3/5 runs report broken workflow (00453-dev-inspect-list-ui)

Description:
In the DesignPen/OpenPencil design app's Dev Mode, the code panel's List view is missing position (X/Y) rows — its Layout section contains only size rows (Width — Fixed, Height — Fixed), so position values cannot be reviewed there at all. The core workflow itself works (draw rectangle, `</>` Dev Mode toggle, select, open code panel, switch the List/Code toggle to "List"), and the position is visible in the Design-mode panel (X: 204, Y: 300), but the Dev Mode List view and the Code/CSS view (which emits only `width`/`height`) both omit position. Additionally, at the default panel width the List values are unreadably truncated to "Fi..." with no hover tooltip, and some panel controls (the "AI" tab, the "100%" zoom indicator) are clipped off the right edge; the values are only readable after manually dragging the panel's resize divider.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Select the rectangle tool and drag on the canvas to draw a 120x48 rectangle.
3. Switch to Dev Mode via the `</>` toggle in the bottom toolbar.
4. Select the rectangle on the canvas ("Rectangle 1" appears in the Inspect panel).
5. Open the code panel (Code tab, Inspect sub-tab) and set the List/Code toggle to "List".
6. Review the Layout property rows for size and position values.

Actual Result:
- The List view's Layout section contains only size rows: Width — Fixed (120px), Height — Fixed (48px). No position rows (X/Y) appear anywhere in the Dev Mode List view; the rectangle's position (X: 204, Y: 300) is only visible back in the Design-mode panel, and the Code/CSS view likewise emits only `width`/`height` with no position properties.
- At the default panel width the List values are unreadably truncated to "Fi..." with no tooltip on hover, and some panel controls (the "AI" tab, the "100%" zoom indicator) are clipped off the right edge; values only become readable after manually dragging the panel's resize divider to widen it.
- Minor: pressing Escape (to close the unit dropdown) also deselected the rectangle, requiring re-selection.

Expected Result:
The Dev Mode code panel's List view should include position (X/Y) rows alongside the Width/Height rows so layout size and position can be reviewed there, and property values should be readable at the default panel width (no "Fi..." truncation without tooltips, no controls clipped off the right edge).

Estimate: S (2 points) — small handler/layout fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 3 of 5 runs failed (agent verdict: not-approve; 2 approved)
- Attempt transcripts:
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_034be78d-6ace-4100-a4ba-4a4c58f4dc46.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_25bc2894-eea7-4470-9d97-3a209757e8f6.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_3e7992d9-6836-475a-80be-5aacb9cabcf3.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_5c33b02f-9a6e-424e-a08a-22299f54aab8.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_d26c06fd-b236-4ecb-b8eb-6d451f5cbab0.txt`

Agent report (verbatim tail of failing run):

```
All steps are complete and the final state is verified. Here's a summary of what I did and found:

**Steps completed:**
1. **Drew a 120×48 rectangle** — selected the rectangle tool and dragged on canvas; size confirmed as exactly 120 × 48 (draw tooltip, Design panel W/H, box-model diagram "120 × 48", and dev-mode canvas badges "W Fixed 120px" / "H Fixed 48px").
2. **Switched to Dev Mode** via the `</>` toggle in the bottom toolbar — the toolbar switched to the green dev-mode style and the right panel switched to the Code/Inspect view.
3. **Selected the rectangle** — "Rectangle 1" shown in the Inspect panel with its layer properties.
4. **Code panel open** — the Code tab is active with the Inspect sub-tab showing the box model and code sections.
5. **Switched to List view** — the List/Code toggle is set to "List", showing the layout property rows.

**Review findings (the reason for my verdict):**
- The List view's Layout section contains **only size rows**: Width — Fixed (120px), Height — Fixed (48px). **No position rows (X/Y) appear anywhere in the Dev Mode List view**, even though the task called for reviewing "size and position values." The rectangle's position (X: 204, Y: 300) is only visible back in the Design-mode panel; the Code/CSS view likewise emits only `width`/`height` with no position properties. So position values could not be reviewed in the List view at all.
- Additionally, at the default panel width the List values were unreadably truncated to "Fi..." with no tooltip on hover, and some panel controls (the "AI" tab, the "100%" zoom indicator) were clipped off the right edge. I could only read the values after discovering and dragging the panel's resize divider to widen it.
- Minor: pressing Escape (to close the unit dropdown) also deselected the rectangle, requiring re-selection.

The core workflow (draw → Dev Mode → select → code panel → List view) functioned, but the List view is missing the position rows the task asked me to review, and the default panel width renders the property values unreadable without a manual resize.

verdict: not-approve
```
