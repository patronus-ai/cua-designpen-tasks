# DesignPen [color picker]: 'alpha slider to exact 50%' fails QA — 3/5 runs report broken workflow (00239-color-alpha-slider-ui)

Description:
The color picker's alpha slider and opacity readout are inconsistent and cannot be trusted or corrected. In all three failing runs, dragging the alpha slider toward 50% landed on the internal value 49.5%, but the color picker's own opacity field rounds its display to whole numbers and showed "50%" — while the Fill panel (which shows one decimal) simultaneously displayed the true 49.5% for the same fill. The two readouts for one value disagree. Worse, typing "50" into the color picker's opacity field does nothing in this state: because the field already displays the rounded "50", the input registers no change and the value stays at 49.5%. The only way to reach a true 50% is the separate Fill-panel opacity input. A user relying on the slider and picker alone would believe they are at exactly 50% while actually at 49.5%.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Draw a rectangle with the Rectangle tool (R).
3. Click the rectangle's fill swatch in the right panel to open the color picker.
4. Type FF0000 into the Hex field to set pure red.
5. Drag the alpha slider down toward the middle until the picker's opacity readout shows "50%".
6. Compare with the Fill panel's opacity value, then try typing 50 into the picker's opacity field.

Actual Result:

- The slider lands on 49.5%; the color picker's opacity field displays a rounded "50%" while the Fill panel shows "49.5%" — two disagreeing readouts for the same fill.
- Typing "50" into the picker's opacity field has no effect (the field already shows "50", so no change is applied); the value remains 49.5%.
- Exactly 50% is only reachable via the Fill panel's numeric opacity input as a workaround.

Expected Result:
The color picker's opacity readout should show the actual value (or the slider should snap to whole percentages), the picker and Fill panel must always agree, and typing a value into the picker's opacity field should always apply it — even when the displayed rounded text matches the typed text.

Estimate: S (2 points) — display rounding plus a no-op guard in the opacity input's change detection; localized to the color picker component

Evidence:

- QA job `db76a8af-97c9-41fb-bbba-42d2d887d5b8`, model `claude-opus-4-8` — 3 of 5 runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_edb71ddd-f8fd-4ec9-ade3-6611ddea1915.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_71d42d2a-aa26-493f-bfc4-ba4243e49902.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_e8f4b1b9-5f64-4915-81f7-00cd2ee47aa0.txt`

Agent report (verbatim tail of failing run):

```
The task is complete. The final state shows Rectangle 1 with Fill = FF0000 at exactly 50% alpha, rendered as a semi-transparent red over the canvas so content behind it shows through.

Here's a summary of what I did and what I encountered:

**Steps completed:**
1. ✅ Selected the rectangle tool and drew a rectangle (270 × 220) on the canvas.
2. ✅ Clicked the fill swatch in the right panel — the color picker opened.
3. ✅ Set the color to pure red by typing `FF0000` in the Hex field (confirmed FF0000).
4. ⚠️ Dragged the alpha slider down to reduce opacity — and this is where I hit friction.

**Problem I hit:** Dragging the alpha slider landed on **49.5%**, not exactly 50%. The color picker's opacity readout **rounded this to a misleading "50%"**, even though the Fill panel (which shows one decimal) revealed the true value was 49.5%. When I then tried to correct it by typing `50` directly into the color picker's own opacity field, it **did nothing** (the field already displayed the rounded "50", so it registered no change). I was only able to reach exactly 50% by editing the separate **Fill-panel opacity field** (49.5 → 50), after which reopening the picker confirmed the alpha handle centered at exactly 50% with Hex FF0000.

So while I did achieve the end goal (pure red at exactly 50% alpha, with content showing through), the alpha-slider/opacity flow has a real inconsistency: the picker rounds 49.5% to a displayed "50%" and won't accept a corrective value in that state — which could easily leave a user at 49.5% thinking they're at exactly 50%.

verdict: not-approve
```
