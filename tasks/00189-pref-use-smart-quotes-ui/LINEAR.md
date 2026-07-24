# DesignPen [preferences]: 'pref use smart quotes' fails QA — 5/5 runs report broken workflow (00189-pref-use-smart-quotes-ui)

Description:
The "Use smart quotes/symbols" preference (Main menu > Preferences, on by default) has no effect on text input: with the preference enabled, typing straight double quotes into a text layer leaves them as ASCII straight quotes (U+0022) instead of auto-converting them to typographic curly quotes. Typing `She said "hello" there.` stores and renders straight quotes on both sides of "hello" — confirmed via the accessibility tree escaping the layer name as `She said \"hello\" there.` and via a control layer with explicitly-inserted curly quotes rendering visibly slanted glyphs. The preference checkbox works; the substitution feature behind it is non-functional.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Open the Main menu (logo, top-left) > Preferences and confirm "Use smart quotes/symbols" is checked (on by default) — do not toggle it.
3. Select the Text tool and click the canvas to add a text layer.
4. Type exactly: She said "hello" there.
5. Inspect the stored/rendered quote characters (zoom the canvas rendering; check the layer name in the accessibility tree).

Actual Result:
- The typed straight quotes are not converted: the text remains `She said "hello" there.` with straight quotes (U+0022) instead of becoming `She said “hello” there.`
- Zoomed canvas rendering shows identical straight vertical quote glyphs on both sides of "hello".
- The accessibility tree escapes the layer name as `She said \"hello\" there.`, proving the stored characters are ASCII straight quotes.
- Control test: a temporary text layer with explicitly-inserted curly quotes (“x”) next to typed straight quotes ("y") shows the font renders curly quotes as clearly slanted glyphs — the typed quotes genuinely stayed straight and no smart-quote substitution occurred.

Expected Result:
With "Use smart quotes/symbols" enabled, typed straight quotes should be auto-converted to typographic curly quotes as the user types, producing `She said “hello” there.`

Estimate: S (2 points) — small handler/layout fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_28ea5d0b-830a-4fd4-bee5-b552443b5fa2.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_49585750-60bd-49ef-99fe-a2bcc9988665.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_916a7638-a89b-446e-aa95-e0393bc53f56.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_9458fb75-260d-4862-b0ab-db5d5871ff3a.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_d79d1a7c-6a30-42f5-ad59-16697fc81409.txt`

Agent report (verbatim tail of failing run):

```
All steps are complete. Here's a summary of what I did and found:

**Task execution:**
1. ✅ **Confirmed the preference**: Opened Main menu (logo, top-left) > Preferences and verified "Use smart quotes/symbols" has a checkmark — it is enabled (on by default). I verified this both before and after typing, without toggling it.
2. ✅ **Added a text layer**: Selected the Text tool, clicked the canvas, and typed exactly: `She said "hello" there.` The layer exists on the canvas and in the Layers panel.

**Bug found:**
Despite "Use smart quotes/symbols" being enabled, the app did **not** convert the typed straight quotes into typographic curly quotes. The text remained `She said "hello" there.` with straight quotes (U+0022) instead of becoming `She said “hello” there.` I verified this rigorously:
- Zoomed canvas rendering shows identical straight vertical quote glyphs on both sides of "hello"
- The accessibility tree escapes the layer name as `She said \"hello\" there.`, proving the stored characters are ASCII straight quotes
- Control test: I created a temporary text layer containing explicitly-inserted curly quotes (“x”) next to typed straight quotes ("y") — the canvas font renders curly quotes as clearly slanted glyphs, proving the typed quotes genuinely stayed straight and no smart-quote substitution occurred (the scratch layer was deleted afterward)

So while the preference is on, the smart quotes/symbols feature is non-functional — typed straight quotes are not auto-converted to smart quotes.

verdict: not-approve
```
