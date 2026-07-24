# DesignPen [text & typography]: 'type feature generic' fails QA — 5/5 runs report broken workflow (00317-type-feature-generic-ui)

Description:
The standard ligatures toggle is missing from the app: the Type settings popover's Details tab exposes OpenType features per font, but its "Letterforms" section only ever contains "Rare ligatures" (discretionary ligatures/dlig), "Contextual alternates", and "Ordinals" — there is no "Standard ligatures" / "Ligatures" / "Common ligatures" row for any of six fonts tested (Inter, Roboto, Host Grotesk, Montserrat, Poppins, Proxima Nova). No ligature control exists in the Basics tab, Variable tab, font gear settings, text style menu, or main-menu Text submenu either. The app appears to enumerate optional OpenType features but omits the standard "liga" feature entirely, so there is no way to disable standard ligatures (with Host Grotesk the canvas clearly renders a true ffi ligature, yet no toggle is offered). Secondary issue: the right panel renders oddly narrow, so the Type settings sliders button requires horizontal scrolling of the panel to reach.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Create a text layer with the word "office" using the Text (T) tool (default font Inter Regular 14).
3. Open the Type settings popover via the sliders button at the end of the Alignment row in the Typography section (the button may require horizontal scrolling of the right panel to reach).
4. Switch to the Details tab (tabs: Basics / Details / Variable).
5. Inspect the "Letterforms" section (and the rest of the Details tab) for a standard ligatures toggle; repeat with other fonts such as Roboto, Host Grotesk, Montserrat, Poppins, Proxima Nova.
6. Also check the Basics tab, Variable tab, font gear settings, text style menu, and the main menu's Text submenu for any ligature control.

Actual Result:
- The Details tab's "Letterforms" section only ever contains "Rare ligatures" (discretionary ligatures/dlig), "Contextual alternates", and "Ordinals" — no "Standard ligatures" / "Ligatures" / "Common ligatures" row exists anywhere, for any of the six fonts tested.
- No ligature control exists in the Basics tab, Variable tab, font gear settings, text style menu, or main menu Text submenu.
- With Host Grotesk the canvas clearly renders a true ffi ligature, yet no toggle is offered to turn it off — disabling standard ligatures to force f-f-i to render as separate letters is impossible.
- Secondary: the right panel renders oddly narrow, so the Type settings sliders button requires horizontal scrolling of the panel to reach.

Expected Result:
The Type settings Details tab should include a standard ligatures ("liga") toggle so users can turn standard ligatures off and have sequences like f-f-i render as separate letters on the canvas.

Estimate: M (3 points) — scoped feature fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 completed runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_35b760e4-3a64-44d4-b560-38bebd132e90.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_3d87a87b-c26e-4e25-a376-493f3fa7af75.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_717307cc-d1d7-4180-a7ee-c04c9d7da216.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_7bf58f6d-ecd3-4c6a-842c-d7b7c82c33a9.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_da6d4d61-ef5b-4316-ab53-6060830268e0.txt`

Agent report (verbatim tail of failing run):

```
I have completed all the work possible on this task. Here's the final summary:

**What was accomplished:**
1. ✅ **Created a text layer with the word "office"** — using the Text (T) tool on the canvas; the layer "office" exists at X=304, Y=300 with the default font Inter Regular 14.
2. ✅ **Opened the Type settings popover** — via the sliders button at the end of the Alignment row in the Typography section (the right panel renders oddly narrow, so the button required horizontal scrolling of the panel to reach, but it worked).
3. ✅ **Switched to the Details tab** — the popover shows Basics / Details / Variable tabs, and Details is active.
4. ❌ **Turn OFF the standard ligatures toggle — impossible: the toggle does not exist in this app.**

**The blocker:** I exhaustively inspected the Details tab (full DOM text dumps plus visual scrolling of the entire list) for six different fonts (Inter, Roboto, Host Grotesk, Montserrat, Poppins, Proxima Nova). The "Letterforms" section only ever contains **"Rare ligatures"** (discretionary ligatures/dlig), "Contextual alternates", and "Ordinals" — there is no "Standard ligatures" / "Ligatures" / "Common ligatures" row anywhere. The Basics tab, Variable tab, font gear settings, text style menu, and main menu Text submenu contain no ligature control either. The app appears to enumerate optional OpenType features from each font but omits the standard "liga" feature entirely, so there is no way to disable standard ligatures and force f‑f‑i to render as separate letters. (Notably, with Host Grotesk the canvas clearly rendered a true ffi ligature, yet no toggle was offered to turn it off.)

I left the document in the closest possible state to the task: the "office" text layer in Inter is selected, and the Type settings popover is open on the Details tab.

The required toggle is missing from the application — this is an app bug/omission that blocks the final step of the task.

verdict: not-approve
```
