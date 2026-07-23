# DesignPen [text & typography]: 'text paragraph spacing' fails QA — 3/5 runs report broken workflow (00312-text-paragraph-spacing-ui)

Description:
Setting paragraph spacing itself works (Type settings popover → Basics tab → Paragraph spacing 24 visibly grows the layer height by 24px), but two real bugs hit during the flow. First, the Type settings sliders button in the Typography section is rendered outside the visible right-panel area at the 1280x720 viewport — the panel content overflows horizontally and the button is cut off; it is only reachable via the accessibility tree, which leaves the right panel horizontally scrolled (showing mostly blank space) with no way to restore it by normal scrolling. Second, mid-task the app unexpectedly navigated to about:blank, and reloading brought back an empty document with all work lost, forcing a full redo.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Create a single text layer with two paragraphs of placeholder copy (e.g. "Lorem ipsum dolor sit amet..." and "Ut enim ad minim veniam...") separated by a line break (Enter).
3. With the layer selected, look for the Type settings sliders button at the end of the Typography section in the right panel and try to reach it by normal scrolling.
4. Reach the sliders button via the accessibility tree (scroll it into view programmatically) and click it to open the Type settings popover.
5. In the Basics tab, set Paragraph spacing to 24.
6. Continue working in the session and watch for the app spontaneously navigating to about:blank.

Actual Result:
- The sliders (Type settings) button in the Typography section is rendered outside the visible right-panel area — the panel content overflows horizontally and the button is cut off. Reaching it via the accessibility tree left the right panel horizontally scrolled (showing mostly blank space), and normal scrolling could not restore it.
- Mid-task, after the workflow had been completed once, the app unexpectedly navigated to about:blank; reloading brought back an empty document with all work lost, forcing the entire task to be redone from scratch.
- The feature itself worked: paragraph spacing 24 applied visibly (layer height grew from 34 to 58, +24px gap between paragraphs) and the field reads 24.

Expected Result:
The Type settings button should be visible and clickable within the right panel at 1280x720 without accessibility-tree workarounds, and the app should never spontaneously navigate to about:blank or lose the document on reload.

Estimate: M (3 points) — scoped feature fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 3 of 5 completed runs failed (2 approved)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_10edb499-e801-4eba-94e8-e84d0838d037.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_13f00115-312d-4453-ab67-52caf90bdef2.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_2fab2750-8534-4f56-892b-667c6198dee7.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_56b51ba1-dfc7-43f7-9464-5976d0185ece.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_7f709fad-7e9d-4312-842c-c65e522963f9.txt`

Agent report (verbatim tail of failing run):

```
The task has been completed. Final state:

- **Text layer**: A single text layer containing two paragraphs of placeholder copy ("Lorem ipsum dolor sit amet..." and "Ut enim ad minim veniam...") separated by a line break (Enter), visible in the Layers panel as one layer.
- **Type settings**: Opened the Type settings popover via the sliders button in the Typography section (confirmed by its "Type settings" tooltip), and set **Paragraph spacing to 24** in the **Basics** tab. The change visibly applied on canvas — the layer height grew from 34 to 58 (+24px gap between the paragraphs), and the field reads 24.

However, I hit real problems along the way:
1. **UI clipping bug**: The sliders (Type settings) button in the Typography section is rendered outside the visible right-panel area at this viewport — the panel content overflows horizontally and the button is cut off. I could only reach it via the accessibility tree, which left the right panel horizontally scrolled (it now shows mostly blank space), and normal scrolling couldn't restore it.
2. **Unexpected page blank/reset**: Mid-task, after completing everything once, the app unexpectedly navigated to about:blank; reloading brought back an empty document with all work lost, so I had to redo the entire task from scratch.

The end result is correct, but the session was not problem-free.

verdict: not-approve
```
