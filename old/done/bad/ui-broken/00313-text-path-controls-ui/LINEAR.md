# DesignPen [text & typography]: 'text path controls' fails QA — 4/5 runs report broken workflow (00313-text-path-controls-ui)

Description:
The text-on-path features themselves (pen-tool curve, attaching text to the path, and the Flip side button in the Path/TextOnPath section) work correctly, but the surrounding session is broken. Mid-task the app crashed to a blank page (about:blank), and reloading restored an older "snapshot" document containing only the vector, losing the attached text. Explicit File → Save fails with the app error "Cannot read properties of undefined (reading 'digest')", and Ctrl+S also does not work, so the finished state cannot be persisted — a page reload reverts to the old snapshot. Minor issues: the properties panel is horizontally clipped (cutting off the "Flip side" button label), and dismissing the save-error toast with the Text tool still active accidentally creates an empty text box.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Select the Pen tool from the toolbar dropdown and draw a large curved line: place an anchor, click-drag to create a smooth bezier apex, place the end anchor, and finish the path.
3. With the Text tool, click directly on the path to create a path-bound text layer and type "around the bend"; confirm the properties panel gains a "Path" (TextOnPath) section with Offset/Alignment/Reverse/Flip side/Detach from path.
4. With the text selected, click the "Flip side" button in the Path (TextOnPath) section.
5. Attempt to persist the document via File → Save (and Ctrl+S).
6. Reload the page and compare the document to the pre-reload state.

Actual Result:
- Mid-task the app unexpectedly crashed to a blank page (about:blank); reloading restored an older "snapshot" document containing only the vector, losing the attached text (the text attach + flip had to be redone).
- File → Save fails with an app error: "Cannot read properties of undefined (reading 'digest')"; Ctrl+S does not work either, so the finished state cannot be persisted — a page reload reverts to the old snapshot.
- Minor: the properties panel is horizontally clipped, cutting off the "Flip side" button label; dismissing the save-error toast accidentally created an empty text box because the Text tool stays active.
- The drawing, text-on-path attachment, and Flip side features themselves worked correctly (glyphs moved to the opposite side of the curve, button shows as active).

Expected Result:
The app should not crash to about:blank mid-session, and File → Save (and Ctrl+S) should persist the document without errors so a reload restores the completed state.

Estimate: L (5 points) — state/undo consistency issue, needs investigation across the edit pipeline

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 4 of 5 completed runs failed (1 approved)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_24b96c64-87bb-464c-9208-aa001cc88a01.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_79a3dfaf-a05c-4c4e-949b-48267e2583d8.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_8266dcfd-8717-44d9-9b7c-690e56a93ff6.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_8f109d3d-2b4a-4b26-8495-0b09a2ef2dbc.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_d83cfd03-6ea6-48c2-a100-d1c1414b6646.txt`

Agent report (verbatim tail of failing run):

```
The task's end state is in place. Here's a summary of what was done and how it went:

**Completed steps:**
1. **Drew a large curved line with the Pen tool** — selected Pen from the toolbar dropdown, placed an anchor, click-dragged to create a smooth bezier apex, placed the end anchor, and finished the path ("Vector 1", a 560×220 arc).
2. **Attached "around the bend" to the curve** — with the Text tool, clicked directly on the path, which created a path-bound text; typed "around the bend" and it rendered flowing along the curve (the layer's properties panel gained a "Path" TextOnPath section with Offset/Alignment/Reverse/Flip side/Detach from path).
3. **Flipped the text to the other side** — with the text selected, clicked the **Flip side** button in the Path (TextOnPath) section; the glyphs moved to the opposite side of the curve (mirrored across the path), and the button shows as active.

**Problems encountered:**
- Mid-task the app unexpectedly crashed to a blank page (about:blank); reloading restored an older "snapshot" document containing only the vector, losing my attached text — I had to redo the text attach + flip.
- Explicit **File → Save fails with an app error**: "Cannot read properties of undefined (reading 'digest')", and Ctrl+S doesn't work either, so the finished state cannot be persisted — a page reload reverts to the old snapshot (verified once; I left the completed state live in the app afterwards without reloading).
- Minor UI issue: the properties panel is horizontally clipped, cutting off the "Flip side" button label; also, dismissing the save-error toast accidentally created an empty text box (the Text tool stays active), which I deleted.

The drawing, text-on-path attachment, and flip features themselves worked correctly, but the session was not smooth: the app crashed once with work loss, and saving is broken with a JS error, so the result only exists in the live (unsaved) session.

verdict: not-approve
```
