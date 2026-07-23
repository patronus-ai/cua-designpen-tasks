# DesignPen [text & typography]: 'text style create' fails QA — 5/5 runs report broken workflow (00339-text-style-create-ui)

Description:
Saving a text layer's look as a shared text style is impossible because both creation entry points are broken. In the Styles create panel (right panel → Styles → "+" / "Add style"), clicking "Text" simply closes the menu — no naming dialog opens and no style is created ("Color" is equally unresponsive, and menu items don't highlight on hover), while the adjacent "Export +" button works normally, proving clicks register elsewhere. The TextStylesMenu (⠿ icon next to Typography with text selected) contains only "No style", a "No text styles" placeholder, and a permanently disabled "Update style" — no create option. A secondary issue: the document does not persist across a page reload (the first "Release notes" layer was wiped).

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Create a text layer with the text "Release notes" using the Text tool.
3. In the Typography section, set font family to Montserrat and font size to 28.
4. In the right panel, go to Styles → "+" ("Add style") and click "Text" to save the look as a style named "Heading/Release".
5. Observe: the menu closes and nothing happens; reproduces with coordinate clicks, accessibility-ref clicks, double-clicks, slow mouse-down/up, keyboard navigation, before and after a page reload.
6. With the text selected, open the TextStylesMenu (⠿ icon next to Typography) and look for a create-style option.
7. (Secondary) Reload the page and observe the document does not persist.

Actual Result:
- Styles "+" → "Text" "simply closes the menu and does nothing — no naming dialog opens and no style is created"; "Color" is equally unresponsive; menu items don't highlight on hover. The adjacent "Export +" button works, so clicks register fine elsewhere.
- The TextStylesMenu only contains "No style" (checked), a "No text styles" placeholder, and a permanently disabled "Update style" — no option to create a style from the current text's look.
- No alternative creation path exists (canvas right-click menu, layer "..." menu, main menu Text submenu, Assets panel, Tools, Variables); the Styles panel stayed empty after every attempt.
- Additional: "the document did not persist across a page reload — my first 'Release notes' layer was wiped".

Expected Result:
The Styles "+" → "Text" action (or the TextStylesMenu) should open a naming dialog and create a shared text style ("Heading/Release") capturing the current look (Montserrat, 28), visible in the Styles panel. The document should also persist across reloads.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 completed runs failed (`verdict: not-approve`)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_2afe207b-ce21-4ff5-b665-b22ac3118895.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_5012a3b6-8aa9-400b-8aff-f4e8b9a4eb36.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_7daee61b-ecdb-4803-94f1-7c75d387addc.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_cda6c32d-c931-4050-aecb-23294352c943.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_dae64b64-8d35-4d5b-884e-5a901aa69b97.txt`

Agent report (verbatim tail of failing run):

```
I've completed all the investigation possible. Here's my final summary:

## Task Summary

**What succeeded:**
1. ✅ Created a text layer with the text "Release notes" using the Text tool
2. ✅ Set its font family to **Montserrat** in the Typography section
3. ✅ Set its font size to **28** in the Typography section (confirmed: Montserrat / Regular / 28, line-height 33.6)

**What failed — creating the shared text style ("Heading/Release"):**
- **Styles create panel** (right panel → "Styles" → "+" / "Add style" → "Text"): Clicking the "Text" option simply closes the menu and does nothing — no naming dialog opens and no style is created. I verified this repeatedly with coordinate clicks, accessibility-ref clicks, double-clicks, slow mouse-down/up sequences, and keyboard navigation, both before and after a fresh page reload. The "Color" option is equally unresponsive. Menu items don't even highlight on hover. Meanwhile the adjacent "Export +" button works normally (it added an export row when clicked directly), proving the clicks register fine elsewhere — this specific feature is broken.
- **TextStylesMenu** (⠿ icon next to Typography with the text selected): It only contains "No style" (checked), a "No text styles" placeholder, and a permanently disabled "Update style" entry. There is **no option to create a new style** from the current text's look.
- No alternative creation path exists: I checked the canvas right-click context menu, the layer "..." menu, the main menu (Text submenu only has Bold/Italic/Underline), the Assets panel (components only), Tools, and Variables.
- After every attempt, the Styles panel remained empty and the TextStylesMenu still reported "No text styles", confirming no style was ever created.

**Additional issue:** the document did not persist across a page reload — my first "Release notes" layer was wiped and I had to recreate it.

The text layer with the exact look (Montserrat, 28) exists on the canvas, but saving it as a shared text style named "Heading/Release" is impossible because the app's style-creation UI is non-functional in both documented entry points (the Styles create panel's "Add style → Text" is a silent no-op, and the TextStylesMenu has no create action).

verdict: not-approve
```
