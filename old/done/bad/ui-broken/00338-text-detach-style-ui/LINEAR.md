# DesignPen [text & typography]: 'text detach style' fails QA — 5/5 runs report broken workflow (00338-text-detach-style-ui)

Description:
Shared text style creation via the right panel's Styles section "+" ("Add style") → "Text" is a silent no-op: no style appears in the Styles section, no dialog or naming prompt opens, and no error toast is shown (the notifications region stays empty); the same applies to the menu's Color/Effect/Layout guide items. Control tests show the app is not globally broken (text layer creation, Effects "+", undo, File menu, and context menus all work) — this specific style-creation menu is dead. Because no style can be created, the TextStylesMenu only shows "No style" / "No text styles" / disabled "Update style", no style chip ever appears in the Typography section, and the unlink/detach action can never be reached.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. In the right panel Styles section, click "+" ("Add style") and click "Text" to create a shared text style.
3. Observe the silent no-op; reproduces clicking the menu item by coordinates (label, icon, mid-row), clicking the `menuitem` element by reference, slow mouse-down/mouse-up, double-click, keyboard navigation (ArrowDown + Enter), after a fresh reload, with and without a text layer selected, and even while editing text with characters selected.
4. Create a new text layer and open the TextStylesMenu (grid icon next to "Typography") to apply the style.
5. Look for a style chip with an unlink action in the Typography section to break the link.
6. Set the layer's font size to 40.

Actual Result:
- "Every attempt was a silent no-op — no style appeared in the Styles section, no dialog or naming prompt opened, and no error toast was shown (notifications region stayed empty)." Same for the menu's Color/Effect/Layout guide items.
- The TextStylesMenu opens but only ever shows "No style" (checked), "No text styles", and a disabled "Update style" — no create option and nothing to apply.
- No style chip (with an unlink action) ever appears in the Typography section, so the detach step is unreachable.
- Only the font-size change to 40 succeeded, confirming the Typography inputs themselves work.

Expected Result:
"Add style" → "Text" should create a shared text style (opening an editor/naming prompt), the TextStylesMenu should let it be applied to a text layer, and the resulting style chip in the Typography section should expose an unlink action that detaches the layer so its font size can be changed independently.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 completed runs failed (`verdict: not-approve`)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_0b9e00b9-b070-408e-a2d5-e85b1803767a.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_9fdf5284-5b0d-437f-a6ed-38b5388b071a.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_e9bcd78e-6a9d-4b0a-b306-8c7fe739faec.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_eadbbd12-fe32-4b4a-a298-0f2f8b211444.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_ebef57e5-ad03-4094-9ef6-a5a10afc4984.txt`

Agent report (verbatim tail of failing run):

```
I've completed my investigation. Here's a summary of what happened:

**What I did:**
1. **Attempted to create a shared text style** — The only creation entry point in the app is the right panel's **Styles section "+" ("Add style") → "Text"**. I tried this many times and ways: clicking the "Text" menu item by coordinates (on the label, the icon, and mid-row), clicking the actual `menuitem` element by reference, slow mouse-down/mouse-up, double-click, keyboard navigation (ArrowDown + Enter), and after a fresh page reload, both with and without a text layer selected and even while editing text with characters selected. **Every attempt was a silent no-op** — no style appeared in the Styles section, no dialog or naming prompt opened, and no error toast was shown (notifications region stayed empty). The same applies to the menu's Color/Effect/Layout guide items.
2. **Verified the app isn't globally broken** (control tests): creating text layers works, the Effects "+" button correctly added a drop shadow, undo worked, and menus elsewhere (File menu, context menus) function normally. The style-creation menu is specifically dead.
3. **TextStylesMenu** (grid icon next to "Typography"): it opens, but only ever shows "No style" ✓, "No text styles", and a disabled "Update style". It has no create option, and with no styles in existence there was nothing to apply to a new text layer.
4. **Unlink on the style chip**: impossible to test — since no style could be created or applied, no style chip (with an unlink action) ever appears in the Typography section.
5. **Font size 40**: I did set the text layer's font size to 40 successfully (the one actionable step), confirming the Typography inputs themselves work.

**Conclusion:** The core flow of this task is blocked by an app bug: "Add style → Text" (the shared text style creation action) silently does nothing, so no shared text style can be created, none can be applied via the TextStylesMenu, and the unlink-on-chip step can never be reached. Only the final font-size change was achievable.

The task could not be completed because shared text style creation is broken (silent no-op with no style created, no error surfaced), which blocks applying a style via the TextStylesMenu and unlinking it from the style chip.

verdict: not-approve
```
