# DesignPen [strokes]: 'stroke apply style' fails QA — 5/5 runs report broken workflow (00335-stroke-apply-style-ui)

Description:
Creating a paint style via the Styles section "+" with nothing selected is broken: the "+" opens the Text/Color/Effect/Layout guide menu, but selecting "Color" (or "Text") simply closes the menu — no creation dialog ever appears and no style is created. The menu also does not capture keyboard focus (typeahead keys leak through to global shortcuts, e.g. "c" activated the Comments tool). The downstream part of the workflow works: the "+" inside the stroke color-picker's Libraries popover opens a working "Create style" dialog, and applying the style via the Stroke apply-styles popover succeeds — though in that dialog the Value field is not directly editable and only inherits the current stroke color.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Press Escape / click empty canvas so nothing is selected.
3. In the properties panel Styles section, click "+" to open the add-style menu.
4. Click "Color" (bug also reproduces with "Text").
5. Observe: menu closes with no creation dialog and no style created (Styles list empty, "No paint styles" in the libraries popover, Assets empty); reproduces with coordinate clicks, ref clicks, hover-then-click, double-click, separate mousedown/mouseup, keyboard navigation/typeahead, page reload, with/without document content.
6. (Workaround path) Draw a circle with the ellipse tool, add a stroke, set stroke color to #0000FF, and use the "+" inside the stroke color-picker's Libraries popover to create "Brand/Blue"; note the Create-style dialog's Value field is not directly editable.
7. Apply "Brand/Blue" via the Stroke apply-styles popover — this part works.

Actual Result:
- Styles "+" (nothing selected) → "Color" is a silent no-op: "selecting 'Color' simply closes the menu: no creation dialog ever appears and no style is created". "Text" is equally dead.
- The menu does not capture keyboard focus: "pressing 'c' for typeahead even leaked through to the global Comments-tool shortcut".
- In the stroke color-picker's Create style dialog, "the Value field is not directly editable either — it only inherits the current stroke color".
- The rest of the flow works via workaround: "Brand/Blue" was created (#0000FF) and correctly applied to the circle's stroke via the Stroke apply-styles popover (Code tab shows `border: 1px solid #00F`).

Expected Result:
Clicking "Color" (or any item) in the Styles section "+" menu with nothing selected should open the style-creation dialog and produce a new paint style, with the dialog's Value field editable.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 completed runs failed (`verdict: not-approve`)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_48d573a1-a7f4-44d3-9fee-8eda391b5a0a.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_989117ec-2573-44b0-a053-9053d5df2099.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_a23d4068-fbd1-4a49-bc00-f566f428370a.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_b8a200dd-ad99-42d4-a46e-5d997888fca7.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_fa466a3c-dee3-4799-949a-59f2190171c7.txt`

Agent report (verbatim tail of failing run):

```
All steps are now complete. Final state verified:

- **Paint style "Brand/Blue"** exists in the file (visible under Styles → "Color styles" when nothing is selected) with value **#0000FF**
- **Circle** drawn with the Ellipse tool (Ellipse 1, 200×200)
- **Stroke** added to the circle, and **"Brand/Blue" is applied to the stroke** via the Stroke apply-styles popover (Libraries tab showed the style with a checkmark; the stroke row shows the linked style name, and the Code tab confirms `border: 1px solid #00F` / border color `#0000FF`)

**Summary of what went wrong:**

The first required step — creating the paint style via the **Styles section "+" with nothing selected** — is broken in this app. Clicking "+" opens the Text/Color/Effect/Layout guide menu, but selecting **"Color"** simply closes the menu: no creation dialog ever appears and no style is created (confirmed by the empty Styles list, "No paint styles" in the libraries popover, and empty Assets). I retried extensively: coordinate clicks, accessibility-ref clicks, hover-then-click, double-click, separate mousedown/mouseup, keyboard navigation/typeahead, a page reload, and with/without content in the document — always a no-op (the "Text" option is equally dead; pressing "c" for typeahead even leaked through to the global Comments-tool shortcut, showing the menu doesn't capture keyboard focus).

I completed the task only via a workaround: I drew the circle, added a stroke, set the stroke color to #0000FF, and used the "+" inside the stroke color-picker's Libraries popover, whose "Create style" dialog works (note: in that dialog the Value field is not directly editable either — it only inherits the current stroke color). I then detached and re-applied "Brand/Blue" explicitly via the Stroke apply-styles popover, which worked correctly.

Because the specified style-creation flow (Styles section "+", nothing selected → Color) is non-functional and required a workaround, this cannot be approved.

verdict: not-approve
```
