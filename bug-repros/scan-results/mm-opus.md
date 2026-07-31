# designpen v6 mm opus-5 10x — full scan 2026-07-31

job: e9ee9a6e-021c-411e-9313-ef2b8032560d
rows scanned: 83/90 (completed/all)

## Known-class hit table

Counts are regex-pattern counts over base64-stripped transcripts; excerpts scrubbed.

| class | transcripts w/ hits | total hits | strongest excerpt (scrubbed, ≤200ch) |
| --- | --- | --- | --- |
| 15 canvas-focus-loss (p_focus) | 63 | 121 | "Could not type '20': no editable element is focused (active element: other:BUTTON). Click the target input or text field first" (mm-giftcard-checkout#1) |
| 8 special-character-input (p_specialchar) | 81 | 1998 | "Successfully typed text: Gift Card Checkout — Leon. Note: '—' have no US-keyboard key event and were inserted directly — no keydown/keyup fired" (mm-giftcard-checkout#1) |
| 2 instance-override-revert (p_revert) | 8 | 12 | "The text overrides were lost in the cut/paste. Let me undo." (mm-mpin-setup#7); "the gap improved but the icon override reset. Let me re-apply the XCircle swap." (mm-mpin-setup#6) |
| 4 stale-text-measurement (p_staletext) | 9 | 20 | "Stale text measurement: changing text via an *instance's* property field (e.g. 'Label', 'Title') does NOT re-measure → text overflows/clips" (mm-gifting-select-brand#4); "chip label 'All brands' stays clipped at 31px text width" (mm-gifting-select-brand#9) |
| 7 negative-wrap-gap (p_neggap) | 6 | 10 | "Negative gaps aren't supported. Let me revert and evaluate at 100%." (mm-withdraw-cash#3) |
| 12/14 text-invisible (p_invis) | 12 | 35 | "The font for that style isn't available — text is invisible. Reverting to Body/Small." (mm-gifting-select-brand#8); "⚠️ BROKEN styles (render invisible — missing fonts): all `M3/*` and `Paragraph / P-200`" (mm-mpin-setup#2) — largely the known seed-font gap, same render mechanism as class 14 |
| 5 fixed-frame-auto-expand (p_autoexpand) | 1 | 2 | false positive — excerpt is "double-clicking … auto-expands the [layers] tree" (mm-account-settings#2). No real class-5 hit in this job |
| 10 assets-panel-hang (p_assets) | 2 | 4 | boilerplate how-to notes only, no hang events |
| 11 assets-drag-misparent (via p_bug) | ≥1 | — | "Drag-drop from Assets lands inside whatever frame is under the cursor (it landed inside `Checkout/Credit Info`, not as a sibling)" (mm-giftcard-checkout#3) |
| 13 layer-reorder tree≠visual (via p_bug) | ≥3 | — | "dropping a component from Assets into an auto-layout frame ALWAYS appends as the LAST child. Reordering does NOT work (layer-panel drag, canvas drag, Bring to front/Send to back all fail)" (mm-notifications#9); "Layer-tree drag to reparent does NOT work" (mm-giftcard-checkout#1) |
| 6 fill-container-stale-width (via p_bug) | ≥1 | — | "'Fill container' often shows a stale width — re-click 'Fill container' in the W chevron menu to force recompute" (mm-gifting-select-brand#8) |
| 1 color-style-binding-no-repaint (p_norepaint) | 0 | 0 | indirect only: "Canvas rendering is often stale. After changing an instance's `Label` property, the canvas keeps showing the old text — force a re[paint]" (mm-giftcard-checkout#3) |
| 3 text-property-dropped, 9 first-keystroke-drop, 16 export-fig-timeout | 0 | 0 | no hits |

Class-4 adjacent workaround seen repeatedly: "'Hug contents' shows checked but stays fixed → click 'Fixed width', then re-open and click 'Hug contents'" (mm-mpin-setup#4).

## NEW candidate classes

### N1. instance-copy-paste-corruption (strong, ≥3 transcripts)

Clipboard operations on instances corrupt or lose state — distinct from class 2 (reverts on page switch) and class 12 (invisible text): here the *paste itself* produces wrong content.

- "**Ctrl+C/Ctrl+V of instances is LOSSY** – pastes empty frames." (mm-gifting-select-brand#3)
- "**Copy/paste of nodes with IMAGE fills is BROKEN** — always pastes the first image (Amazon). Must MOVE original nodes instead." (mm-notifications#7)
- "**IMPORTANT BUG**: cut (ctrl+X) + paste (ctrl+V) inserts the layer as a sibling AFTER the currently selected layer, BUT the pasted element's Y position does not reflow" (mm-account-settings#8)

Why app: the editor's clipboard/serialization path drops overrides, image-fill refs, and auto-layout reflow; typing/tooling worked fine in the same transcripts (agent immediately observes and works around).

### N2. icon-swap-stale-render / black-square (strong, ≥3 transcripts)

Instance-swapping a nested icon leaves stale vector data rendered as a black square (or the swap simply doesn't render), until format/variant is re-set.

- "**Icon swapping inside `Actions/Icon Button` is broken** — swapped icons render as a black square with stale leftover vectors." (mm-home#3)
- "**⚠ Instance-swap bug:** Swapping a Menu Row's `Gear` icon instance for another icon produces a spurious black square." (mm-account-settings#1)
- "**CRITICAL BUG:** nested icon instances lose their overrides when a component is instantiated (render as a '+' Plus icon)." (mm-withdraw-cash#7)

Why app: render output disagrees with the document model after a supported operation (swap). The "+"-placeholder default overlaps the known seed unwired-prop issue, but "black square with stale leftover vectors" is a rendering defect, not seed content.

### N3. variables-panel-broken (weak, 1 transcript)

- "Variables panel (left rail 'Variables') is buggy: tabs all show same list, search doesn't filter." (mm-home#8)

Why app: pure UI behavior of the Variables panel; nothing agent- or harness-related. Needs confirmation (single witness).

### N4. keyboard-shortcuts-nonfunctional (low confidence — may be unimplemented, not broken)

Consistently reported across transcripts: Ctrl+Alt+G (frame selection) does NOT work (mm-account-settings#8, mm-gifting-select-brand#8/#10, mm-onboarding-carousel#6, mm-withdraw-cash#10 …); one transcript also "Ctrl+D does NOT work" (mm-withdraw-cash#10, contradicted by others where Ctrl+D duplicates fine). Right-click menu equivalents work. Flagging for triage, likely "not implemented" rather than regression.

### N5. boolean-shape-breaks-on-resize (weak, 1 transcript)

- "set the proportional-scale lock (↗ icon right of W/H fields) BEFORE resizing, or the boolean shape renders broken." (mm-onboarding-carousel#7)

Seed-content notes (out of scope, known list): Deliveroo logo "renders as 'To'" (mm-notifications#2), "Access part% of your paycheck" typo (mm-onboarding-carousel#5), GAP tile labeled "Zara", M3/* + Paragraph/P-200 styles bound to missing fonts, `Forms/Chip` Selected variant "renders with no fill" (mm-giftcard-checkout#4).

## Verdict

NEW classes found: yes — N1 instance-copy-paste-corruption, N2 icon-swap-stale-render (both strong, multi-transcript); N3 variables-panel-broken, N4 shortcuts-nonfunctional, N5 boolean-shape-resize (weak/single-witness, need confirmation).
