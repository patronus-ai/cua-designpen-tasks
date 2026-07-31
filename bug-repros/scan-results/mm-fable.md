# designpen v6 mm fable-5 10x — full scan 2026-07-31

job: 0d00efba-64f2-4010-b72a-8a4ffdf6b558
rows scanned: 89/90 (completed/all)

## Known-class hit table

Counts are regex-pattern counts over base64-stripped transcripts; excerpts scrubbed.

| class | transcripts w/ hits | total hits | strongest excerpt (scrubbed, ≤200ch) |
| --- | --- | --- | --- |
| 15 canvas-focus-loss (p_focus) | 56 | 117 | "Could not type '56': no editable element is focused (active element: other:DIV). Click the target input or text field first" (mm-wallet-insights#3) |
| 8 special-character-input (p_specialchar) | 77 | 1670 | "Successfully typed text: £100.00. Note: '£' have no US-keyboard key event and were inserted directly — no keydown/keyup fired" (mm-withdraw-cash#2); also literal `\t` inserted instead of field-tabbing (mm-wallet-insights#3, mm-account-settings#6) |
| 2 instance-override-revert (p_revert) | 19 | 43 | "The header icon overrides were lost (likely from the undo) — I'll re-swap them" (mm-wallet-insights#5); "also re-triggered sync that RESET avatar swaps in instances once — avoid touching masters now" (mm-notifications#5) |
| 5 fixed-frame-auto-expand (p_autoexpand) | 11 | 11 | "Root frame grew to 425x896. Fixing W back to 414." (mm-withdraw-cash#6); "Transaction List now selected and its height grew to 1200" (mm-wallet-insights#5) |
| 1 color-style-binding-no-repaint (p_norepaint) | 4 | 6 | "The paint didn't update. Let me use the Libraries tab in this picker to apply Red/60 properly." (mm-account-settings#7); "IMPORTANT BUG SEEN: applying a color STYLE to text whose fill had a variable binding did NOT change actual hex (showed style name but stayed 5C5C5C)" (mm-giftcard-checkout#5) |
| 4 stale-text-measurement (p_staletext) | 4 | 8 | "screen header Title 'Notifications' is CLIPPED (renders 'Notification' + sliver of s — stale text width from Title prop vs master 'Screen Title')" (mm-notifications#5) |
| 12/14 text-invisible (p_invis) | 5 | 13 | "text (content 'New', 98 wide fixed, Body/Default-Se 16/16, opacity 100) renders INVISIBLE on canvas … after cut/paste corruption AND after setting Title prop" (mm-notifications#8) |
| 7 negative-wrap-gap (p_neggap) | 4 | 7 | "shift+A wraps selection in auto-layout; auto-detects direction/gap — OFTEN WRONG (horizontal + negative gap)" (mm-account-settings#5) |
| 10 assets-panel-hang (p_assets) | 2 | 3 | no hang events — excerpts are how-to notes and one benign "Assets panel reset" (mm-account-settings#2) |
| 13 layer-reorder / drag-nesting (via p_bug) | ≥2 | — | "Drag-into-frame on canvas does NOT work; layer-panel drag nesting does NOT work" (mm-notifications#8) |
| 9 numeric first-keystroke (adjacent, via p_bug) | ≥1 | — | "resize it to ~250w (W field typing is broken — use resize handle drag or the W dropdown)" (mm-notifications#6) |
| 6 fill-container-stale-width (via p_bug) | ≥1 | — | "'Fill container' width via W field dropdown arrow, but buggy — typing exact 382 works" (mm-account-settings#1) |
| 3 text-property-dropped, 16 export-fig-timeout | 0 | 0 | no hits |

## NEW candidate classes

### N1. instance-copy-paste-corruption (strong, ≥3 transcripts; same class as mm-opus N1)

Copy/cut+paste of configured instances produces empty shells or resets overrides; matching text can go invisible (overlaps class 12 but the trigger is the clipboard op itself).

- "copy as empty shells. I must copy from the MASTER on the Components page instead. First, delete the broken empty row." / "The copy lost all overrides — broken." (mm-gifting-select-brand#10)
- "**AVOID ctrl+x/ctrl+v with instances** — earlier cut/paste caused the header's icon swap overrides AND inserted progress [to be lost]" (mm-notifications#7)
- "pasted instances revert to base (Amazon logo) or corrupt — e.g., Section Title text renders invisible after cut+paste of configured instance. RULE: place fresh unconfigured instances, THEN configure in place" (mm-notifications#8)

Why app: document serialization through the clipboard drops override state; reproducible enough that agents adopted standing workarounds mid-run.

### N2. undo-reverts-unrelated-changes (new in this job, 2 transcripts)

Ctrl+Z rolls back earlier, unrelated edits instead of (or in addition to) the last one.

- "ctrl+z undo can silently revert EARLIER unrelated changes (it reverted the header icon swap once) — avoid undo; prefer explicit [fixes]" (mm-gifting-select-brand#7)
- "The header icon overrides were lost (likely from the undo)" (mm-wallet-insights#5)

Why app: undo-stack scoping defect in the editor; nothing harness-side touches document history.

### N3. instance-swap-preserves-stale-overrides (strong, ≥2 transcripts; same family as mm-opus N2)

Swapping a nested instance carries the old instance's overrides into the new one, rendering broken (white-on-white, wrong look) until the nested instance is deleted and re-placed fresh.

- "The Selected state renders broken (white on white) — the swap carried overrides. Let me undo back to the original chip." (mm-giftcard-checkout#6)
- "the chevron row opens 'Swap instance' dialog instead; swapping preserves stale overrides (broken look) — better to delete nested chip and drop fresh Forms/Chip from Assets" (mm-giftcard-checkout#8)
- "original 'Chip £80' nested instance was DELETED (swap left broken overrides) and replaced with fresh Forms/Chip instance" (mm-giftcard-checkout#7)

Why app: override merge logic on swap-instance produces invalid render state; agent verified fresh placement of the same component renders fine.

### N4. transient-render-glitches-fixed-by-reload (weak, 1-2 transcripts; class-1 adjacent)

- "reload also fixed the Leon logo rendering glitch (avatar showed plain circle; after reload LEON roundel renders fine — it was a display glitch only)" (mm-giftcard-checkout#9)
- "Row 3 shows the gap glitch again. Let me check if it's a stale render by switching pages." (mm-giftcard-checkout#3)

Canvas raster diverges from document state until reload/page-switch — same stale-render mechanism family as class 1; logging separately because the trigger is image fills/gaps, not color-style binding.

### Feature-limitation notes (probably by design, both models report)

- Per-range text styling inside a node does NOT work — panel changes apply to the whole text node (mm-mpin-setup#2, mm-notifications#2).
- Ctrl+Alt+G (frame selection) and Ctrl+Alt+B (detach) shortcuts dead; right-click menu equivalents work (mm-mpin-setup#2, mm-notifications#1).

Seed-content notes (out of scope, known list): `Navigation/Screen Header` nested back icon defaults to broken "+" (mm-withdraw-cash#2/#3, mm-notifications#8 — known unwired seed prop); Simple header fixed-width title truncates "Bank Accou" (mm-withdraw-cash#5); GAP tile mislabeled "Zara" (mm-gifting-select-brand#3); "Created in this file" style `Blue/60(Pri)` broken, shows F8F8F8 (mm-giftcard-checkout#7); Phosphor icons render black square unless Format=Outline (multiple).

## Verdict

NEW classes found: yes — N1 instance-copy-paste-corruption and N3 instance-swap-preserves-stale-overrides (strong, corroborated across both mm jobs); N2 undo-reverts-unrelated-changes (new, 2 witnesses); N4 transient-render-glitch-reload (weak).
