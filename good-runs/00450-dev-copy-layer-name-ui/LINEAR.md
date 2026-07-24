# DesignPen [clipboard / copy-paste]: 'dev copy layer name' fails QA — 4/5 runs report broken workflow (00450-dev-copy-layer-name-ui)

Description:
In the DesignPen/OpenPencil design app's Dev Mode, the "Copy layer name" control in the code panel header silently fails to write anything to the clipboard, with no error or toast shown. The whole workflow up to that point works (draw rectangle, rename layer to "HeroBanner", toggle Dev Mode via the `</>` button, select the rectangle — the code panel header shows the layer name). The agent proved the environment's clipboard pipeline itself works via native ctrl+c/ctrl+v, seeded the clipboard with "MARKER123", clicked the control, and pasting still yielded "MARKER123" instead of "HeroBanner". The app's other copy control (the Layout CSS copy button, which even flashes green "copied" feedback) also fails, so the app's copy-to-clipboard is broken app-wide — plausibly because the site is served over insecure HTTP where `navigator.clipboard` is unavailable and no fallback is implemented.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Select the rectangle tool and draw a rectangle on the canvas.
3. In the layers panel, double-click the layer name and rename it from "Rectangle 1" to "HeroBanner".
4. Switch to Dev Mode using the `</>` toggle in the bottom toolbar.
5. Select the rectangle on the canvas; the code panel header shows the layer name.
6. Click the copy-layer-name control in the code panel header (the layer-name element whose hover tooltip reads "Copy layer name").
7. Paste into any text field to inspect the clipboard contents.

Actual Result:
- Clicking the "Copy layer name" control does not copy anything: after seeding the clipboard with "MARKER123" and clicking the control multiple times, pasting still produced "MARKER123" instead of "HeroBanner".
- No error or toast is shown to the user — the failure is completely silent.
- The Layout CSS copy button (which even flashes green "copied" feedback) likewise fails to write to the clipboard, indicating an app-wide clipboard-write failure.
- The environment's native clipboard works (ctrl+c/ctrl+v of text in an edit field round-trips correctly), ruling out an environment issue.

Expected Result:
Clicking the copy-layer-name control in the Dev Mode code panel header should place the layer name ("HeroBanner") on the system clipboard, or surface an error to the user if the copy fails. Clipboard writes should work (or have a fallback) on the insecure HTTP origin.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 4 of 5 runs failed (agent verdict: not-approve; 1 approved)
- Attempt transcripts:
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_3bbdfee5-a2e6-4ebc-9eda-76acafcc01ff.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_6fe61c9f-8690-4df6-8f39-5e57251f499e.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_88d0982a-1b85-4a93-a718-0e876bd88563.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_8f26ed54-60a7-45bc-9469-9df3c37537d2.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_b45a9918-7760-468c-94cd-121fc8d42157.txt`

Agent report (verbatim tail of failing run):

```
All steps of the task were performed, and the final state is consistent: the rectangle exists on the canvas, its layer is named "HeroBanner", Dev Mode is active, and the rectangle is selected with the code panel header showing the layer name.

**Summary of what I did:**
1. ✅ Selected the rectangle tool and drew a 300×180 rectangle on the canvas
2. ✅ Renamed its layer from "Rectangle 1" to "HeroBanner" via double-click in the layers panel
3. ✅ Switched to Dev Mode using the `</>` toggle in the bottom toolbar (UI switched to dev-mode dark toolbar + Code/Inspect panel)
4. ✅ Selected the rectangle on the canvas (code panel header shows "HeroBa…", canvas shows the HeroBanner badge)
5. ⚠️ Clicked the copy-layer-name control in the code panel header (the layer-name element whose hover tooltip reads "Copy layer name") — **but it did not actually copy anything to the clipboard**

**The problem found:** I verified the clipboard rigorously. First I proved the environment's clipboard pipeline works (native ctrl+c of text in an edit field, then ctrl+v, round-trips correctly). Then I seeded the clipboard with a marker value "MARKER123", clicked the "Copy layer name" control (multiple attempts), and pasted — the clipboard still contained "MARKER123" instead of "HeroBanner". I also tested the app's other copy control (the Layout CSS copy button, which even flashes green "copied" feedback) and it likewise failed to write to the clipboard. So the app's copy-to-clipboard feature is broken app-wide in this environment (plausibly because the site is served over insecure HTTP, where `navigator.clipboard` is unavailable, and no fallback is implemented), and no error/toast is shown to the user. The copy-layer-name control silently fails, so the final requirement — the name actually being on the clipboard via that control — could not be fulfilled.

verdict: not-approve
```
