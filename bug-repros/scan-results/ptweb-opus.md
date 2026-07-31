# designpen v6 ptweb opus-5 10x — full scan 2026-07-31

job: 7cf836b0-933f-4953-a358-707e131a0f3e
rows scanned: 81/130 (completed/all). Skipped 49 rows, all `status == "failed"` (job itself finished; no running rows). Scanner errors: none.

## Known-class hit table

| class | transcripts w/ hits | total hits | strongest excerpt (scrubbed, ≤200ch) |
| --- | --- | --- | --- |
| 15 canvas-focus-loss (p_focus) | 68 | 153 | ptweb-add-address#5: "Could not type '800': no editable element is focused (active element: other:BUTTON)" |
| 8 special-character-input (p_specialchar) | 81 | 1766 | ptweb-payment-failed#2: "Successfully typed text: Payment Failed — Mobile … '—' have no US-keyboard key event and were inserted directly — no keydown/keyup fired" |
| 14 text-style-renders-invisible (p_invis) | 9 | 26 | ptweb-referral#1: "**`Body_Bold_16px` DOES NOT RENDER (invisible text) — never use it**"; ptweb-add-address#3: "BROKEN styles (font missing, text renders invisible — DO NOT USE): Body_16px, Body_Bold_16px, SubHeading_18px, Primary CTA" |
| 1 color-style-binding-no-repaint (p_norepaint) | 8 | 16 | ptweb-consult-booking-form#9: "CRITICAL BUG+FIX — colour styles on nested-instance text don't repaint: applying a colour style to text inside an instance sets the style *name* but not th[e paint]"; ptweb-profile#8: "Applying a color style to a paint ALREADY bound to a style/variable sets the name but NOT the color (renders stale/black)" |
| 2 instance-override-revert (p_revert) | 7 | 14 | ptweb-profile#1: "The badge fill overrides reverted. Let me re-apply them."; ptweb-personalising#8: "nested badge overrides reverted during reparenting"; ptweb-profile#9: "**Overrides that DO NOT persist (revert to master on reload)**" — reload as a new trigger |
| 4/6 stale-text-measurement / fill-container-stale-width (p_staletext) | 10 | 30 | ptweb-payment-failed#1: "KNOWN BUG: children with W ~ 'Fill container' keep stale widths when an ancestor's width changes"; ptweb-podcast#10: "CRITICAL TEXT RE-MEASURE BUG: when you change an instance's text … the text node keeps its OLD width" |
| 5 fixed-frame-auto-expand (p_autoexpand) | 4 | 8 | ptweb-web-landing#5: "the root frame's width spontaneously grew to 1238 once (matching Hero Banner's intrinsic width)"; ptweb-personalising#8: "root frame … accidentally grew to 407 once" |
| 7 negative-wrap-gap (p_neggap) | 1 | 4 | (weak; wrap-direction complaints present but few explicit negative-gap strings) |
| 9 numeric-first-keystroke (p_first) | 0 | 0 | — |
| 10 assets-panel-hang (p_assets) | 0 | 0 | — |
| 16 export_fig timeout (p_export) | 0 | 0 | — |
| CDP internal error (p_internal) | 0 | 0 | — |

p_bug catch-all: 81 transcripts / 676 raw hits; dominant match is CDP tool-doc boilerplate ("remote debugging enabled") — ignored. 64 unique excerpt signatures reviewed manually; classification below.

## NEW candidate classes

1. **ctrl+alt+G "Frame selection" shortcut dead (menu item works).** The right-click menu action works; the documented keyboard shortcut never fires. Not the Linux $mod trap — it is already Ctrl-based, and Ctrl+Alt+K (Create component) works in the same transcripts.
   - ptweb-profile#8: "Right-click menu has: Frame selection (Ctrl+Alt+G – keyboard shortcut doesn't work, use menu) … Create component (Ctrl+Alt+K works)"
   - ptweb-referral#2: "Right-click layer → **Frame selection** wraps a layer in a frame (ctrl+alt+G keyboard shortcut does NOT work)"
   - also ptweb-add-address#7, ptweb-add-address#10, ptweb-registration#6, ptweb-registration#10, ptweb-name-poll#3 — 7+ independent attempts converge on the same finding.
   - Why app: same key chord delivered by the same harness works for Ctrl+Alt+K; only this binding is dead.

2. **Cut/paste (ctrl+X → ctrl+V) of FRAMES yields empty clipboard (text layers work).**
   - ptweb-add-address#5: "`ctrl+X` then `ctrl+V` works for text layers but **failed for frames** (clipboard empty). `ctrl+C`/`ctrl+V` works."
   - Cross-job corroboration: ptweb-fable ptweb-referral#9 "ctrl+X/ctrl+V doesn't re-parent either" (see fable report, NEW class "re-parenting broken").
   - Why app: clipboard round-trip inside the editor; copy works, cut of the same node type doesn't.

3. **Renderer: strokes on rounded rects with radius ≥ half-height draw only left/right arcs.**
   - ptweb-web-landing#7: "**Renderer bug:** strokes on rounded rects with radius ≥ half-height render as only left/right arcs (Ghost butt[on])"
   - Cross-job: ptweb-fable consult-booking-form#6/#9 "lucide/circle renders broken (open arc) — replaced with primitive Ellipse" (same arc-stroking path).
   - Why app: pure canvas rasterization defect, no agent/harness involvement.

4. **`&` in text re-escapes to `&amp;` after the layer row is double-clicked.**
   - ptweb-referral#10: "**Bug:** typing `&` sometimes re-escapes to `&amp;` when the layer row is double-clicked afterwards. Verify/fix ampersands at the end."
   - Single transcript — weak; HTML-entity double-encoding leak between layers-panel label and text content. Watch other jobs before promoting.

5. **"Selection colors" bulk replace does not assign variables.**
   - ptweb-add-address#5: "'Selection colors' bulk replace does NOT work for assigning variables."
   - Single transcript — weak; distinct from class 1 (this is the bulk-replace UI, not style binding repaint).

6. **Swap-instance on nested instances does nothing.**
   - ptweb-profile#4: "3 Shortcut tiles must show different icons … but **nested instance swap doesn't work**"
   - Cross-job: strong corroboration in ptweb-fable (podcast#5 "Swap instance dropdown does NOT work (clicks on result rows do nothing)", profile#4 "The swap feature is broken in this build"). Top-level swaps sometimes work (web-landing#7 used Swap Instance successfully) — failure appears specific to nested instances / certain dialogs.

Class-adjacent (reported as evidence, not new): ptweb-personalising#2 "instances do NOT reflow their internal auto-layout when their own text/size changes. Fix ~ nudge the MAIN COMPONENT's width" → class 4 family. ptweb-add-address#1 "'Fill container' widths often don't recompute correctly (computed 264 instead of 232 with 3 children)" and ptweb-personalising#8 "'Fill container' on a child computes the FULL parent content width (ignores siblings)" → class 6 family (compute-ignores-siblings nuance).

Seed-content notes (out of scope, new instances): ptweb-referral#1/#3 Empty State component icon is a broken/unrenderable tofu glyph; ptweb-web-landing#5 seed "Search Icon" renders as a broken L shape (agents swap in lucide/search); ptweb-referral#9 CTA Banner "Button Text property does NOT work" (known dead-prop family, task 003).

## Verdict

NEW classes found: yes — (1) ctrl+alt+G frame-selection shortcut dead [strong, 7 transcripts], (2) frame cut/paste empty clipboard [moderate, cross-job], (3) rounded-rect/circle stroke arc renderer bug [moderate, cross-job], (6) nested swap-instance dead [moderate, cross-job]; plus weak singletons (4) `&`→`&amp;` re-escape and (5) selection-colors bulk replace inert.
