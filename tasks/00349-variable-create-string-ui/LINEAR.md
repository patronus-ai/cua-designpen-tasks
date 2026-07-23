# DesignPen [variables]: 'variable create string' fails QA — 2/2 runs report broken workflow (00349-variable-create-string-ui)

Description:
There is no functional UI to bind a text layer's CONTENT to a STRING variable. The Design panel exposes working "Apply variable" pickers for width, height, opacity, font family, font size and fill, but the only content-binding candidate in the DOM — an "Apply variable" button in the Appearance header — renders invisible/zero-width, opens no picker when activated, and focusing it corrupts the right panel layout (content shifts and gets clipped). On top of that, the app hard-crashed to about:blank twice during the run (once after clicking the Code tab, once right after clicking the hidden "Apply variable" button), losing the unsaved text layer each time. Creating the STRING variable itself ("cta-label" = "Get started") works fine.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Open the Local variables dialog from the left panel Variables tab.
3. Create a collection ("New collection") via the folder-plus icon.
4. Use the "+ Add" menu > Text to create a STRING variable, rename it to "cta-label", set its value to "Get started"; close the dialog.
5. Add a text layer via the Text tool (e.g. "Placeholder") and select it.
6. In the right Design panel, look for a control to bind the layer's text content to a variable; try the "Apply variable" button in the Appearance header.
7. Also try clicking the Code tab with the layer selected.

Actual Result:

- No functional control exists to bind a text layer's content to a variable; the "Apply variable" button in the Appearance header is rendered invisible/zero-width, opens no picker when activated, and focusing it corrupts the right panel layout (content shifts and gets clipped).
- The app hard-crashed to about:blank twice (once after clicking the Code tab, once right after clicking the hidden "Apply variable" button); each crash lost the unsaved text layer (the variable collection survived).
- Alternative paths all failed: canvas/layer context menus, the app main menu (File/Edit/Object/Text), text-edit mode with selection, drag-and-drop of the variable onto the canvas and Layers panel, clicking the variable row/type icon while the layer was selected, and the Type settings popup (its "Variable" tab is only for variable-font axes).

Expected Result:
With a text layer selected, a visible working control should open a variable picker for the layer's text content, and choosing the "cta-label" STRING variable should bind the content to it. The app should not crash to about:blank during the flow.

Estimate: L (5 points) — state/undo consistency issue, needs investigation across the edit pipeline

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 2 of 2 completed runs failed (`verdict: not-approve`)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_05fb9c0d-4a4b-4934-bcf7-3a6137f547d4.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_5f80092a-3a21-42c0-8fa9-f81b75101859.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_6015122d-edd5-45a1-88f5-0c3acbfa1a9a.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_907ddaae-2006-4a72-a056-666457974daf.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_de8482cf-1d49-40e5-a5d3-f97e639bf6ce.txt`

Agent report (verbatim tail of failing run):

```
I've completed all steps that were achievable and exhausted every plausible UI path for the final binding step. Final state of the work:

**What succeeded:**
1. ✅ Opened the Local variables dialog from the left panel Variables tab
2. ✅ Created a collection ("New collection") via the folder-plus icon
3. ✅ Used the "+ Add" menu → Text to create a STRING variable, renamed it to "cta-label" with value "Get started" (verified intact in the dialog)
4. ✅ Added a text layer ("Placeholder") via the Text tool

**What failed — binding text content to the "cta-label" token:**
- The Design panel exposes working "Apply variable" pickers for width, height, opacity, font family, font size and fill (the font-family picker even lists "cta-label"), but there is **no functional control to bind a text layer's CONTENT to a variable**. The only candidate in the DOM — an "Apply variable" button in the Appearance header — is rendered invisible/zero-width, opens no picker when activated, and focusing it corrupts the right panel layout (content shifts and gets clipped).
- Worse, the app **hard-crashed to about:blank twice** during the session (once after clicking the Code tab, once right after clicking that hidden "Apply variable" button). Each crash lost the unsaved text layer (the variable collection survived), forcing me to re-create the layer.
- I also tried: canvas/layer context menus, the app main menu (File/Edit/Object/Text), text-edit mode with selection, drag-and-drop of the variable onto the canvas and Layers panel, clicking the variable row/type icon while the layer was selected, and the Type settings popup (its "Variable" tab is only for variable-font axes). None offers content binding.

The collection, the "cta-label" = "Get started" string variable, and the text layer all exist in the document, but the text-content binding could not be completed due to the missing/broken binding UI and the repeated crashes to about:blank with loss of unsaved work.

verdict: not-approve
```
