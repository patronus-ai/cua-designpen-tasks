# designpen v6 ptweb fable-5 10x — full scan 2026-07-31

job: d580a233-3755-4202-8809-1820938b9f28
rows scanned: 123/130 (completed/all). Job was still RUNNING at scan start: skipped 7 rows — 1 `running`, 6 `failed`. Scanner errors: none.

## Known-class hit table

| class | transcripts w/ hits | total hits | strongest excerpt (scrubbed, ≤200ch) |
| --- | --- | --- | --- |
| 15 canvas-focus-loss (p_focus) | 91 | 240 | ptweb-registration#7: "Could not type 'Why do we need this info~': no editable element is focused (active element: other:CANVAS)" |
| 8 special-character-input (p_specialchar) | 116 | 3152 | ptweb-support#5: "Successfully typed text: 1 · Compose Question — '·' have no US-keyboard key event and were inserted directly — no keydown/keyup fired" |
| 7 negative-wrap-gap (p_neggap) | 28 | 65 | ptweb-support#8: "'Add auto layout' via right-click menu (Shift+A) wraps selection but often creates wrong direction/negative gap and COMPRESSES children widths"; ptweb-registration#7: "The wrap chose horizontal with negative gap" |
| 5 fixed-frame-auto-expand (p_autoexpand) | 24 | 46 | ptweb-web-landing#9: "The section grew to 608. Set it back to 360 fixed"; ptweb-consult-booking-form#10: "Details Form grew to 479 fixed"; ptweb-podcast#6: "Fill mis-expanded to 377" |
| 14 text-style-renders-invisible (p_invis) | 16 | 46 | ptweb-consult-booking-form#2: "Body_Bold_16px 16/16 (**BROKEN — renders invisible, do not use**)"; ptweb-web-landing#6: "The style made the text invisible (font issue~)" |
| 2 instance-override-revert (p_revert) | 15 | 22 | ptweb-profile#1: "Overrides revert when double-clicking onto other texts"; ptweb-web-landing#8: "editing anything INSIDE a component master … RESETS all icon-swap overrides on its instances"; ptweb-referral#3: "Escape during property edit REVERTS text overrides" |
| 1 color-style-binding-no-repaint (p_norepaint) | 10 | 16 | ptweb-registration#2: "applying a color STYLE to a vector stroke bound to a variable shows the style name but keeps stale resolved color"; ptweb-podcast#2: "**Shared color styles DO NOT RENDER on instance children** (fills or strokes)" |
| 4/6 stale-text-measurement / fill-container-stale-width (p_staletext) | 8 | 17 | ptweb-podcast#4: "after changing text content in an instance … the text node does NOT re-measure (stays clipped at old width)"; ptweb-web-landing#9: "**Fill-container render bug**: value sometimes stays stale" |
| 9 numeric-first-keystroke (p_first) | 1 | 1 | (single hit; no strong excerpt captured) |
| 10 assets-panel-hang (p_assets) | 1 | 2 | ptweb-podcast#5 — excerpt is an Assets-drag note, likely regex false positive, no actual hang observed |
| 16 export_fig timeout (p_export) | 0 | 0 | — |
| CDP internal error (p_internal) | 0 | 0 | — |

p_bug catch-all: 123 transcripts / 900 raw hits; dominant match is CDP tool-doc boilerplate — ignored. 109 unique excerpt signatures reviewed manually; classification below.

## NEW candidate classes

1. **Re-parenting an existing layer is broken via every route.** Layer-panel drag, canvas drag, and cut/paste all fail to move a node into a target frame; instances that DO get reparented come out visually broken.
   - ptweb-referral#9: "**Layer-panel drag re-parenting does NOT work**; canvas drag re-parenting does NOT work; ctrl+X/ctrl+V doesn't re-parent either. **Workaround: select an existing child inside target frame and [paste as sibling]**"
   - ptweb-podcast#5: "(move → parent row) often FAILS silently; delete and redo via root instead"
   - ptweb-consult-booking-form (…#7 area): "The reparented instance is truly broken in this app. New rule: only drop instances directly."
   - ptweb-baby-names-hub#10: "The auto-layout nesting is buggy. Let me switch strategy: build sections as root-level frames"
   - Why app: pure in-editor tree operations; multiple mechanisms (drag AND clipboard) fail identically across attempts. Related to but broader than known class 11 (assets drag misparent, which is about NEW instances from the Assets panel). Cross-job: ptweb-opus add-address#5 frame cut/paste clipboard-empty.

2. **Swap-instance dropdown dead — clicks on result rows do nothing.**
   - ptweb-podcast#5: "**Swap instance dropdown does NOT work** (clicks on result rows do nothing). Workaround: edit the MAIN component … propagates to all instances."
   - ptweb-profile#4: "The swap feature is broken in this build. I'll detach tiles 2 ~ 3 and replace their icons manually."
   - Cross-job: ptweb-opus profile#4 "nested instance swap doesn't work". Intermittent — other attempts used Swap Instance successfully — but three independent hard failures.
   - Why app: dialog renders, search works, row click is a no-op; nothing harness-specific about clicking a list row.

3. **Plain punctuation (apostrophe, comma) breaks text auto-measurement.** Distinct from known class 8 (special chars with no key event — £/–/·): apostrophe and comma ARE plain US-keyboard keys; typing them wedges width recompute.
   - ptweb-baby-names-hub#7: "**CRITICAL BUG FOUND: typing an apostrophe (') in text/property values breaks text auto-measurement** — chip label 'Don't know yet' stayed 34px wide and clipped. FIX: av[oid]"; same run ships "Dont know yet" without apostrophe: "(Default; NO apostrophe — tool bug)"
   - ptweb-baby-names-hub#3: "let me try without the apostrophe, which may also fix the measurement bug"
   - ptweb-profile#8: "The comma triggers a wrap bug. Let me use '1.2k' instead."
   - Why app: the character lands in the text node (content correct), only layout/measurement wedges — same engine defect family as class 4 but with a reproducible character trigger.

4. **Variables panel broken.** Multiple independent failures: panel shows the same list for every collection; assigning a variable via the color-swatch Libraries tab doesn't render; agents in 5+ attempts give up on variables and fall back to color styles.
   - ptweb-payment-failed#10: "Variables panel is buggy (shows same list for all collections) — use color styles instead."
   - ptweb-personalising#4: "(Clicking color swatch → Libraries tab assignment does NOT work visually!)"
   - ptweb-web-landing#3: "Variables dialog (left rail 'Variables') is buggy; use color styles instead." — also ptweb-referral#8, ptweb-name-poll#8, ptweb-personalising#10 (opus).
   - Why app: panel state/render defects observed by inspection, not by input failures.

5. **Auto-layout gap "Auto" (space-between) unreliable/dead.**
   - ptweb-baby-names-hub#6: "**'Auto' gap (space-between) is BUGGY** — don't use; compute fixed gaps instead"
   - ptweb-support#10: "Gap ~ 'auto' (space-between) does NOT work; instead set the first child's width to 'Fill container' to push siblings right"
   - ptweb-consult-booking-form#3: "Gap 'auto' (space-between) typing does NOT work"
   - Note: typing "auto" into the numeric field may be by-design (dropdown chevron path exists — opus transcripts use it) — but #6/#10 claim the space-between MODE itself misbehaves. Moderate confidence.

6. **Panel-header rename dead (layers-panel rename works).**
   - ptweb-consult-booking-form#4: "Renaming via right panel header does NOT work."
   - ptweb-payment-failed#4: "Renaming via right-panel header doesn't work."
   - ptweb-registration#3: "(Panel header rename doesn't work.)"; ptweb-baby-names-hub#9: "Renaming via double-click panel header name does NOT work reliably"
   - Why app: same rename gesture succeeds in the layers panel in the same runs; the Design-panel header field just never commits.

7. **Multi-line canvas-typed text renders only the first line** (auto-width default).
   - ptweb-registration#4: "**Text render bug fix**: texts created via canvas typing default to auto-width resizing; multi-line content then renders ONLY first line. Fix: select text → Layout Resizing →"
   - Single transcript — weak; adjacent to class 4/12 but a distinct render-clip symptom.

Renderer arc bug (cross-ref, reported as NEW in ptweb-opus report): ptweb-consult-booking-form#6: "**lucide/circle renders broken (open arc)** — replaced with primitive Ellipse 20×20"; ptweb-consult-booking-form#9: "The lucide/circle component itself renders broken."

Class-adjacent evidence (not new): ptweb-name-poll#10 "child 'Fill container' width computes to FULL parent content width ignoring siblings" → class 6; ptweb-support#5 "Chip label override bug: chip doesn't re-hug" and ptweb-shop#10 Badge/text hug clip → class 4; ptweb-registration#9 "recoloring lucide icon instance strokes does NOT render (data changes but canvas shows dark)" → class 1; ptweb-baby-names-hub#4 parent frames "REVERT TO HUG" spontaneously → class 5/6 family.

Seed-content notes (out of scope, new instances): ptweb-registration#8 style "Text/primary" resolves white 0% opacity ("BROKEN white 0%, never use it"); ptweb-support#4 "Text/inverse … buggy resolved value 333333"; ptweb-web-landing#10 "Brand/accent-light (WARNING: resolves teal — buggy)"; underscore legacy styles (Body_16px family) broken-font — known font-gated class 14 seed pattern.

## Verdict

NEW classes found: yes — (1) re-parenting broken via all routes [strong, 4+ transcripts + cross-job], (2) swap-instance dropdown dead [moderate, cross-job], (3) apostrophe/comma breaks text measurement [strong, reproducible character trigger], (4) variables panel broken [moderate, 5+ transcripts], (5) gap-Auto space-between unreliable [moderate], (6) panel-header rename dead [moderate, 4 transcripts], (7) first-line-only render on canvas-typed multiline [weak singleton].
