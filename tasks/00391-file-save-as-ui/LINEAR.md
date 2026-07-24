# DesignPen [file handling]: 'file save as' fails QA — 5/5 runs report broken workflow (00391-file-save-as-ui)

Description:
Save As in DesignPen (Main menu > File > Save as…, shortcut Ctrl+Shift+S / Cmd+Shift+S) is implemented as a native browser `prompt()` dialog ("Save as:") instead of an in-app dialog. Automation environments auto-dismiss native JS dialogs, so the filename can never be typed and the dialog closes instantly — the save cannot be completed. The app also gives no feedback after the prompt is dismissed (no toast, no saved-file indication), and there is no in-app way to verify a save: "Back to files" does nothing, File > Open… shows no dialog, "Auto-save to local file" produces no visible response, and the Actions/command palette search is not focusable. Fixing this requires replacing the native prompt with an in-app Save As dialog (or at minimum providing save confirmation UI).

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Select the Ellipse tool from the shape tool dropdown and draw a circle on the canvas (e.g. 150x150; it appears as "Ellipse 1" in the Layers panel).
3. Open Main menu > File > Save as… (or press Ctrl+Shift+S / Cmd+Shift+S).
4. Try to enter the filename "copy-of-design.fig" in the dialog that appears.

Actual Result:
- The app opens a native browser `prompt()` dialog ("Save as:") instead of an in-app dialog; in the automation environment it is auto-dismissed instantly, so the filename "copy-of-design.fig" can never be typed.
- After re-triggering Save As (including after renaming the document to "copy-of-design" so the prompt default might be used), the app gives no confirmation of any save — no toast, no saved-file indication.
- No alternate verification path works: "Back to files" does nothing, File > Open… shows no dialog, "Auto-save to local file" produces no visible response, and the Actions/command palette search is not focusable.

Expected Result:
Save As should open an in-app dialog (or otherwise automatable UI) where the user can type a new filename such as "copy-of-design.fig", and completing it should save a copy and surface visible confirmation (e.g. a toast or updated file list).

Estimate: XS (1 point) — likely environment/tooling limitation, verify manually and re-scope

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 completed runs failed (`verdict: not-approve`)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_1e7383c0-e0c5-4515-8af3-e3817875696c.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_93a77cfe-5924-4147-9049-7977db12e337.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_9490fcdb-6166-47fc-8a35-daba5cd16c02.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_b389850b-3688-4943-a3c9-1e0edf848f87.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_edfa6269-04fd-4271-af47-fb62cacea3de.txt`

Agent report (verbatim tail of failing run):

```
I've completed all feasible steps. Let me summarize the final state of the task:

**What worked:**
- ✅ **Circle drawn**: I selected the Ellipse tool from the shape tool dropdown and drew a 150×150 circle on the canvas (it appears as "Ellipse 1" in the Layers panel).

**What didn't work:**
- ❌ **Save As with filename "copy-of-design.fig"**: I invoked Main menu > File > Save as… (and the Ctrl+Shift+S / Cmd+Shift+S shortcut) multiple times. Each time, the app opened a **native browser `prompt()` dialog** ("Save as:") instead of an in-app dialog. This environment automatically dismisses native JS dialogs, so there was no way to type the filename "copy-of-design.fig" into it, and the dialog closed instantly every time.
- As a workaround, I renamed the document to "copy-of-design" (hoping the prompt's default value would be used if the auto-dismissal accepted it), then re-triggered Save As — but the app gave no confirmation of any save (no toast, no saved-file indication).
- I also could not verify any save through other means: "Back to files" does nothing, File > Open… shows no dialog, "Auto-save to local file" produces no visible response, and the Actions/command palette search is not focusable.

**Summary of the problem:** The circle was drawn successfully, but saving a copy as "copy-of-design.fig" could not be completed or verified. The app's Save As feature relies on a native browser prompt dialog, which is auto-dismissed in this automation environment, making it impossible to enter the requested filename, and the app provides no feedback or file list to confirm whether anything was saved.

verdict: not-approve
```
