# DesignPen [text & typography]: 'type optical size auto' fails QA — 5/5 runs report broken workflow (00324-type-optical-size-auto-ui)

Description:
The "automatic optical size" toggle in the Type settings popover's Variable tab is unreachable because no font with an optical size (opsz) axis exists or can be added in this environment. Of the 8 bundled fonts, only Inter is variable, and its Variable tab exposes only Slant and Weight axes. Google Fonts search always returns "No fonts found" (no internet: fonts.googleapis.com fails with DNS_PROBE_FINISHED_NO_INTERNET), local/system fonts report "Unavailable" with an inert "Allow" button (Local Font Access API unavailable), and there is no font upload/import anywhere. The workflow's core requirement is impossible in this build.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Create a text layer with the text "Display size".
3. Open the font picker and inspect the available fonts (8 bundled: Host Grotesk, Inter, Montserrat, Noto Naskh Arabic, Noto Sans Symbols, Poppins, Proxima Nova, Roboto) — only Inter is a variable font.
4. With Inter applied, open the Type settings popover via the sliders button in the Typography section and switch to the Variable tab.
5. Look for an Optical size axis or an automatic optical size toggle — only Slant and Weight axes are shown.
6. Try to obtain an opsz font: search Google Fonts for e.g. "Roboto Flex", "Fraunces", "Literata" in the font picker; open Font settings and try enabling local/system fonts; look for a font upload option in Assets, Tools, File menu, and Preferences.

Actual Result:

- The Variable tab for Inter (the only variable font) shows only Slant and Weight axes — no Optical size axis and no automatic optical size toggle.
- The other 7 bundled fonts are static and show no Variable tab at all.
- Google Fonts searches always return "No fonts found"; fonts.googleapis.com fails with DNS_PROBE_FINISHED_NO_INTERNET. Toggling Google Fonts off/on in Font settings does not help.
- Local/system fonts show "Unavailable" in the Font settings popover and the "Allow" button for system font access is inert.
- No font upload/import capability exists anywhere (Assets panel, Tools panel, File menu, Preferences).

Expected Result:
At least one available font exposes an optical size (opsz) axis, so the Variable tab shows the axis with an automatic optical size toggle that can be turned off; alternatively, a working path exists to add such a font (Google Fonts, local fonts, or upload).

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 completed runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_3a59840b-d522-408f-a348-dffb0bfeb313.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_443ec2fe-6f86-4ca9-853e-70610b8e21e4.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_5b3ccf8d-4ad6-492f-b5ff-34e13097fd73.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_d4973345-4b59-4737-9fd1-8253952b3d32.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_fc07375a-6927-41b8-92cf-f001a11acf06.txt`

Agent report (verbatim tail of failing run):

```
I have exhausted every avenue. Final state: the "Display size" text layer is set to Inter (the only variable font available), with the Type settings popover open on the Variable tab — which shows only Slant and Weight axes, with no optical size axis or automatic optical size toggle.

**Summary of what was done and found:**

1. ✅ Created a text layer "Display size" on the canvas.
2. ✅ Opened the Type settings popover via the sliders button in the Typography section.
3. ✅ Switched to the Variable tab.
4. ❌ **Could not turn OFF the automatic optical size toggle**, because no font with an opsz axis is obtainable in this environment:
   - The font picker contains exactly **8 bundled fonts** (Host Grotesk, Inter, Montserrat, Noto Naskh Arabic, Noto Sans Symbols, Poppins, Proxima Nova, Roboto). I tested every one of them: only **Inter** is a variable font, and its Variable tab exposes only **Slant** and **Weight** axes — no Optical size axis and therefore no automatic optical size toggle. The other 7 fonts are static (no Variable tab at all).
   - **Google Fonts don't load**: the sandbox has no internet access (fonts.googleapis.com fails with DNS_PROBE_FINISHED_NO_INTERNET), so searching for opsz fonts like Roboto Flex, Fraunces, Literata, Source Serif, etc. always returns "No fonts found". Toggling Google Fonts off/on in Font settings didn't help.
   - **Local/system fonts are "Unavailable"** in the Font settings popover, and the "Allow" button for system font access is inert (the Local Font Access API isn't available in this browser context).
   - There is no font upload/import capability anywhere (checked the Assets panel, Tools panel, File menu, and Preferences).

The task's core requirement — using a variable font with an opsz axis and disabling its automatic optical size toggle — is impossible in this environment since no such font exists or can be added. The closest achievable state (text layer with the only available variable font, Type settings popover open on the Variable tab) has been set up, but the required toggle does not exist for any available font.

verdict: not-approve
```
