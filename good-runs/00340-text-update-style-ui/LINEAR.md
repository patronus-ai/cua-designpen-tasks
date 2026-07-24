# DesignPen [text & typography]: 'text update style' fails QA — 5/5 runs report broken workflow (00340-text-update-style-ui)

Description:
Creating a shared text style is impossible in this build, which blocks the whole apply-then-edit workflow. The only creation entry point — Design panel (nothing selected) → Styles → "+" (Add style) — opens a menu with Text / Color / Effect / Layout guide, but clicking any item simply closes the menu with no style created, no style row in the Styles list, no editor popover, and no error; the menu items don't even show hover highlighting. Consequently the TextStylesMenu (four-dot "Apply styles" button next to Typography) only ever shows "No style" / "No text styles" with a permanently disabled "Update style", so no style can be applied to the "Intro"/"Outro" layers and the TextStyleEditorPopover can never be opened. Secondary issue: reloading the app wipes the document (no persistence).

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Create two text layers named "Intro" and "Outro".
3. Deselect everything; in the Design panel Styles section, click "+" (Add style) and click "Text" to create a shared text style.
4. Observe: the menu closes with no style created; reproduces via coordinates, accessibility refs, double-click, explicit mouse down/up, keyboard, and with the "Color" and "Effect" items as controls.
5. Select a text layer and open the TextStylesMenu (four-dot "Apply styles" button next to Typography) to apply the style to both layers.
6. Attempt to open the TextStyleEditorPopover to change the style's font size to 40.
7. (Secondary) Reload the app and observe the document is wiped.

Actual Result:
- "Clicking **any** of these items ... simply closes the menu — no style is created, no style row appears in the Styles list, no editor popover opens, and no error is shown. The menu items don't even show hover highlighting."
- The TextStylesMenu only ever shows "No style" (checked), "No text styles", and a permanently disabled "Update style" — no create option, nothing to apply to the two layers.
- The TextStyleEditorPopover could never be opened, so changing font size to 40 was impossible.
- No alternative creation path exists (canvas context menu, main menu, Assets, Tools, Variables; "Libraries" is disabled).
- Additional: "reloading the app wiped the document (the original 'Intro'/'Outro' layers were lost ...), i.e., no persistence."

Expected Result:
The Styles "+" (Add style) → "Text" action should create a shared text style; the TextStylesMenu should then let it be applied to both "Intro" and "Outro" layers, and the TextStyleEditorPopover should open to edit the style (e.g. set font size 40) with the change propagating to both layers.

Estimate: M (3 points) — scoped feature fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 completed runs failed (`verdict: not-approve`)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_0324052d-d973-4ba5-8402-2d7041ff443d.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_0dea8066-8f5f-4267-a2e3-e5fd0a66e270.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_29b06b0c-a135-46fd-b00a-fdda523b3227.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_3bc02698-62e2-4f7e-838b-430dc4020c46.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_838d79c8-bfdc-4144-8750-bfefaa61c6e1.txt`

Agent report (verbatim tail of failing run):

```
I've exhausted all plausible paths for creating a text style. Here's my final report:

## Task Summary

**What I accomplished:**
- ✅ Created two text layers named "Intro" and "Outro" (both visible on canvas and in the Layers panel).

**What failed — blocking bug:**
- ❌ **Creating a shared text style is impossible in this build.** The only creation entry point is the Design panel (with nothing selected) → Styles → "+" (Add style), which opens a menu with Text / Color / Effect / Layout guide. Clicking **any** of these items (I tried "Text" repeatedly via coordinates, accessibility refs, double-click, explicit mouse down/up, and keyboard; also tried "Color" and "Effect" as controls) simply closes the menu — no style is created, no style row appears in the Styles list, no editor popover opens, and no error is shown. The menu items don't even show hover highlighting.
- ❌ The **TextStylesMenu** (four-dot "Apply styles" button next to Typography on a selected text layer) only ever shows "No style" (checked), "No text styles", and a permanently disabled "Update style" — it offers no way to create a style, so nothing could be applied to the two layers.
- ❌ Consequently the **TextStyleEditorPopover** could never be opened, so changing the style's font size to 40 was impossible.
- I also verified there is no alternative creation path via the canvas context menu, main menu (File/Edit/View/Object/Text/Arrange), Assets panel, Tools panel, or Variables; "Libraries" is disabled.
- Additional issue: reloading the app wiped the document (the original "Intro"/"Outro" layers were lost and I had to recreate them), i.e., no persistence.

The core of the task (create a shared text style, apply it to both layers via the TextStylesMenu, then edit it to font size 40 in the TextStyleEditorPopover) is blocked by the non-functional "Add style" action, so the task could not be completed.

verdict: not-approve
```
