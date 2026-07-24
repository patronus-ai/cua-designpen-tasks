# DesignPen [text & typography]: 'text apply style' fails QA — 5/5 runs report broken workflow (00337-text-apply-style-ui)

Description:
Shared text style creation is broken on both documented paths. The Styles section "+" ("Add style") menu with nothing selected opens with Text / Color / Effect / Layout guide, but clicking "Text" just closes the menu — no style editor renders (confirmed via DOM inspection), no style is created, and the menu items don't even highlight on hover or keyboard focus; "Color" and "Effect" fail identically. The fallback path is also missing: the TextStylesMenu (four-dot icon in the Typography section) contains only "No style", "No text styles", and a permanently disabled "Update style" — there is no create/"+" option anywhere (layer context menu, panel "…" menu, main menu, Assets, Tools) to save a styled layer as a shared style, so no 32px Bold style can be created or applied.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Press Escape / click empty canvas so nothing is selected.
3. In the properties panel Styles section, click "+" to open the "Add style" menu.
4. Click "Text" to create a shared text style set to 32px Bold.
5. Observe: the menu closes with no style editor and no style created; reproduces with coordinate clicks, element-ref clicks, double-clicks, and keyboard navigation (Down/Enter); menu items don't highlight on hover.
6. (Fallback) Create a throwaway text layer, set it to 32px Bold, and open the TextStylesMenu (four-dot icon in the Typography section) looking for a save/create option.
7. Add a text layer with the text "Section title" and open the TextStylesMenu to apply the style.

Actual Result:
- Styles "+" → "Text" "does nothing — the menu just closes with no style editor and no style created"; DOM inspection confirms no dialog renders and the Styles list stays empty; "Color" and "Effect" fail identically; menu items don't highlight on hover or keyboard focus.
- No save-as-style path exists for a styled layer: the TextStylesMenu contains only "No style", "No text styles", and a disabled "Update style" — no "+"/create option; no "create style" command in the layer context menu, panel "…" menu, main menu, Assets panel, or Tools panel.
- Applying the style to "Section title" was impossible: the TextStylesMenu reported "No text styles". The layer was only manually set to 32px Bold.

Expected Result:
Clicking "Text" in the Styles "+" menu should open a text-style editor and create a shared style; the TextStylesMenu should then list that style so it can be applied to the "Section title" layer (and/or offer a way to save the current text's look as a style).

Estimate: S (2 points) — small handler/layout fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 completed runs failed (`verdict: not-approve`)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_13698b3e-9159-4d92-929a-d20e5e6c08d4.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_3f446092-3bcd-4c5e-a054-22ed1b351716.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_49174fc6-786f-4739-9fd8-8a040d1c88d6.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_4e9a8a83-149e-4b14-bcda-1d9de05612c6.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_dd6896eb-2f42-45f2-b47b-60dc56ec6b3a.txt`

Agent report (verbatim tail of failing run):

```
I've completed everything that was achievable. Here's a summary of the session:

**What I did:**
1. **Tried creating a shared text style via Styles "+" (nothing selected):** The "Add style" menu opens with Text / Color / Effect / Layout guide options, but clicking "Text" does nothing — the menu just closes with no style editor and no style created. I verified this with coordinate clicks, element-reference clicks, double-clicks, and keyboard navigation (Down/Enter), and confirmed via DOM inspection that no dialog renders and the Styles list stays empty. The menu items don't even highlight on hover or keyboard focus. "Color" and "Effect" fail identically, so the entire "Add style" flow is non-functional in this build.
2. **Tried the fallback — styling a throwaway layer and saving it:** I created a "Temp" text layer and successfully set it to 32px Bold. However, there is no way to save it as a style: the TextStylesMenu (four-dot icon in the Typography section) contains only "No style", "No text styles", and a disabled "Update style" — no "+"/create option. No "create style" command exists in the layer context menu, the panel "…" menu, the main menu, the Assets panel, or the Tools panel.
3. **Added the "Section title" text layer** and opened the TextStylesMenu in the Typography section to apply the style — it reported "No text styles", so there was nothing to apply. I manually set the layer to 32px Bold so it at least matches the intended appearance, and deleted the throwaway layer.

**What went wrong:** The app's style-creation feature is broken. Both documented paths failed: the Styles section "+" → "Text" menu item silently does nothing (no editor, no style created — all four Add-style options fail the same way), and there is no save/create option anywhere for turning a styled layer into a shared text style (TextStylesMenu has no "+" and "Update style" is permanently disabled). Consequently, no shared 32px Bold text style could be created, and it could not be applied to the "Section title" layer via the TextStylesMenu.

verdict: not-approve
```
