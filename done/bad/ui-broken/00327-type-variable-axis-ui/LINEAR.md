# DesignPen [text & typography]: 'type variable axis' fails QA — 5/5 runs report broken workflow (00327-type-variable-axis-ui)

Description:
Taking manual control of an optical size (opsz) axis in the Type settings popover's Variable tab is impossible: no font with an opsz axis exists or can be added. Only Inter is variable among the 8 bundled fonts, exposing just Slant and Weight; Google Fonts searches return "No fonts found" (no internet — fonts.googleapis.com → DNS_PROBE_FINISHED_NO_INTERNET), local fonts are "Unavailable", and no font upload exists. On top of that, the run hit hard app bugs: the app crashed to about:blank twice when clicking the font-family dropdown (losing the document each time), the right Design panel horizontally clips the Type settings button off-screen, Ctrl+S raised an error toast "Cannot read properties of undefined (reading 'digest')", and clicking the middle of the font combobox opens a variable-binding popover instead of the font picker.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Create a text layer with the text "Fine tune".
3. Click the font-family dropdown in the Typography section — the app can crash to about:blank, losing the document (observed twice); reload and recreate the layer if so. Note that clicking the middle of the combobox opens a variable-binding popover; the chevron must be clicked to get the font picker.
4. Inspect all 8 bundled fonts (Host Grotesk, Inter, Montserrat, Noto Naskh Arabic, Noto Sans Symbols 2, Poppins, Proxima Nova, Roboto) — only Inter is variable.
5. With Inter applied, open the Type settings popover via the sliders button (clipped off-screen; reachable only via the accessibility tree) and switch to the Variable tab — only Slant and Weight axes are listed, no Optical size.
6. Try obtaining an opsz font: search Google Fonts (e.g. "Lato", "Roboto Flex", "Fraunces", "opsz") via the Font settings gear icon; check Local fonts; look for font upload in menus, Assets, Tools, Preferences.
7. Press Ctrl+S to save.

Actual Result:

- No font with an optical size (opsz) axis exists in the environment; Inter's Variable tab exposes only Slant and Weight, so "take manual control of the optical size axis and set the slider to 14" is impossible.
- Google Fonts searches always return "No fonts found" (fonts.googleapis.com → DNS_PROBE_FINISHED_NO_INTERNET); Local fonts report "Unavailable"; no font-upload exists in menus, Assets, Tools, or Preferences.
- The app crashed to about:blank twice when clicking the font-family dropdown, losing the document each time.
- The right Design panel is horizontally clipped, hiding the Type settings sliders button off-screen; it could only be clicked via the accessibility tree, and interacting with the panel causes odd scrolling.
- Pressing Ctrl+S raised an app error toast: "Cannot read properties of undefined (reading 'digest')".
- Clicking the middle of the font combobox unexpectedly opens a variable-binding popover instead of the font picker (must click the chevron).

Expected Result:
A variable font with an opsz axis is available (or can be added), the Variable tab exposes that axis so it can be manually set to 14, and the font dropdown, panel layout, and Ctrl+S save all work without crashes or errors.

Estimate: L (5 points) — state/undo consistency issue, needs investigation across the edit pipeline

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 completed runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_00579556-e20d-42b0-8244-f819e4500426.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_0eda3fc2-353a-4c12-8ded-85a486fde4c6.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_27ae938d-c307-4439-841f-21e9728ae1b4.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_5aaa371a-01ce-47a3-87d7-fef0a5750ce4.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_d7e3c211-86d1-4b51-a64d-0743027562ad.txt`

Agent report (verbatim tail of failing run):

```
The "Fine tune" layer remains intact on canvas. I've exhausted every avenue, so here is my final report.

## Summary

**What was accomplished:**
- Created the text layer **"Fine tune"** on the canvas
- Applied **Inter** — the only variable font available in the app
- Opened the **Type settings popover** via the sliders button in the Typography section
- Switched to the **Variable tab**, which displays the font's variable axes (Slant and Weight for Inter)

**What could NOT be accomplished — the core requirement:**
- **No font with an optical size (opsz) axis exists in this environment.** I verified all 8 bundled fonts (Host Grotesk, Inter, Montserrat, Noto Naskh Arabic, Noto Sans Symbols 2, Poppins, Proxima Nova, Roboto): only Inter is variable, exposing just **Slant** and **Weight** — no opsz. The Font settings dialog (gear icon) offers Google Fonts integration ("Enabled") and system/local font access, but the sandbox has no internet (fonts.googleapis.com → DNS_PROBE_FINISHED_NO_INTERNET), so every Google-font search ("Lato", "Roboto Flex", "Fraunces", "opsz") returns "No fonts found"; Local fonts report "Unavailable". Toggling Google Fonts off/on didn't help, and no font-upload exists in menus, Assets, Tools, or Preferences. Therefore "take manual control of the optical size axis and set the slider to 14" was impossible.

**Bugs encountered along the way:**
1. The app **crashed to about:blank twice** when clicking the font-family dropdown, losing the document each time (the text layer had to be recreated from scratch).
2. The right Design panel is horizontally clipped, hiding the Type settings sliders button off-screen — it could only be clicked via the accessibility tree, and interacting with the panel causes it to scroll oddly.
3. Pressing Ctrl+S to save raised an app error toast: "Cannot read properties of undefined (reading 'digest')".
4. Clicking the middle of the font combobox unexpectedly opens a variable-binding popover instead of the font picker (must click the chevron).

Because the central requirement (an opsz axis in the Variable tab) is unachievable with the fonts available, and due to the crashes/data loss and save error above, this task cannot be considered completed successfully.

verdict: not-approve
```
