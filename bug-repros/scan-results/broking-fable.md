# designpen v6 broking fable-5 10x — full scan 2026-07-31

job: 088bacf2-bffe-491a-92bd-15185ef902c7
rows scanned: 145/150 (completed/all; 5 non-completed skipped per playbook)

## Known-class hit table

| class | transcripts w/ hits | total hits | strongest excerpt (scrubbed, ≤200ch) |
| --- | --- | --- | --- |
| 1 color-style-binding-no-repaint | 10 (p_norepaint) + very many pass-2 | 18+ | "applying a color STYLE to an existing paint updates the link but NOT the rendered color" (broking-orderbook#9); "Style-apply bug: applying a shared style over a VARIABLE-bound fill updates the label but NOT the paint" (broking-orderbook#7); "fill is bound to Colors/Greyscale/Black but renders gray. Fix by removing and re-adding" (broking-ledger#4) |
| 2 instance-override-revert | 23 | 41 | "Override-reset bug: ANY reflow-affecting structural op (drag into auto-layout list, wrap, etc.) resets nested chip variant overrides… re-fixed all BUY chip variants after the override-reset bug re-struck (frames 01, 02, and 03)" (broking-orderbook#6) |
| 3 component-text-property-dropped | pass-2 | few | "text properties exposed in right panel Properties as labeled fields" work in places, but "Content field shows 'Long Term' but canvas doesn't update" (broking-watchlist#3) — see also N-classes |
| 4 stale-text-measurement | 6 | 9 | "Backspace snapped it back to cached 69. Workaround: switch the text to fixed-width mode, then set W manually" (broking-orderbook#5); "Same stale-layout bug (X~273, W~89). Let me test the 'one edit behind' theory: change content to something else, then back" (broking-charges-sheet#5) |
| 5 fixed-frame-auto-expand | 13 | 18 | "Root frame grew to 666. Setting W back to 375" (broking-order-confirmation#3); "The card grew to 423 wide (a 391-wide divider is forcing hug)" (broking-profile#2); "watch the frame width growing bug — if 'My Queries' W ≠ 375, re-type 375" (broking-my-queries#5) |
| 6 fill-container-stale-width | pass-2 | several | "Render bug persists with Fill. Set fixed width 343 instead" (broking-place-order#7); "STALE-WIDTH BUG: instance children keep old widths after variant/size changes" (broking-place-order#7) |
| 7 negative-wrap-gap | 6 | 14 | "The wrap went horizontal with negative gap. Fixing: setting flow to vertical" (broking-ledger#7); "shift+A wraps selection in auto-layout frame (may come out horizontal w/ negative gap)" (broking-ledger#7) |
| 8 special-character-input | 133 | 2656 | "Successfully typed text: Sell Order Placed – Confirmation. Note: '–' have no US-keyboard key event and were inserted directly — no keydown/keyup fired" (broking-order-confirmation#1); same for '₹' and '·' |
| 9 numeric-first-keystroke-drop | 0 | 0 | — |
| 10 assets-panel-hang | 6 | 11 | regex hits are benign panel mentions; no hang/freeze evidence in this job |
| 11 assets-drag-misparent | pass-2 | several | "inserting from Assets may mis-nest (landed inside a row instance once — corrupted ICICI row H to 94)… SAFER: drop on empty canvas, then…" (broking-watchlist#6); "Safe method: drop on empty page background → reparent via layers-panel" (broking-orderbook#5) |
| 12 text-invisible-after-duplicate | 34 (p_invis, shared w/ 14) | 81 | see class 14 — most p_invis hits in this job are style-driven invisibility |
| 13 layer-reorder-visual-mismatch | 0 direct | 0 | — |
| 14 text-style-renders-invisible | 34 (p_invis) | 81 | "CRITICAL RENDERING BUG: shared styles 'Typography/Subheading/Sub4' and 'Sub4 SemiBold' render INVISIBLE on Canvas page. Working verified styles: H3 ✓, Body2 ✓" (broking-order-confirmation#1); "3rd 'Paragr' item ~ a 14/18 style whose font does NOT render (text disappears — avoid it!)" (broking-my-queries#9); "the '14 stocks' text invisibility bug after applying text style was fixed via the resize-to-fit (⤢) button" (broking-watchlist#7) |
| 15 canvas-focus-loss-typing | 106 | 266 | "Could not type 'spacing': no editable element is focused (active element: other:BUTTON). Click the target input or text field first" (broking-settings#5) |
| 16 export-fig-timeout | 0 | 0 | p_export zero hits |

p_internal (DevTools internal error): 0.

## NEW candidate classes

Letters (A)–(I) reference the ptdev v6 scan taxonomy (scan-results/ptdev-*.md); those are cross-job confirmations.

### N1. Variant switching on instances broken (clicks/keyboard silently rejected)
The strongest new signal in this job — ~10 transcripts, several calling it app-wide:
- "Variant switching is 100% BROKEN (dropdown clicks AND keyboard selection silently fail for ALL variant properties). Workaround: use default variant + overrides, or copy from DS page" (broking-login-flow#7)
- "KNOWN BUG: The variant dropdowns (and swap-instance panel) in the right panel DO NOT switch Label/Tag variants (clicks don't commit)" (broking-my-queries#1)
- "DS component variant switching on instances is broken (dropdown clicks silently rejected). To get a specific variant: right-click the variant component on Design Sys[tem page]" (broking-charges-sheet#10)
- "Variant switching is broken app-wide. New approach: find an existing INSTANCE of the needed variant on the Design System page" (broking-profile#9)
- Mechanism leads: "Variant dropdowns in right panel are broken for mouse clicks/keyboard-Return; works ONLY via form_input on the hidden native select" (broking-orderbook#8); "variant dropdowns REJECT changes when intermediate combo doesn't exist (e.g., Input Only→OTP)" (broking-login-flow#1); "snaps back when target combo doesn't exist or UI bug" (broking-profile#1); "Variant change didn't commit (known bug)" (broking-order-confirmation#4); also ledger#3/#8, settings#5, login-flow#7, orderbook#10.
Why app: visible dropdown UI ignores committed selections while the hidden native select works — a UI wiring bug; partially aggravated by sparse seed variant sets (missing intermediate combos), but the silent no-commit occurs on valid targets too.

### N2. Instance degrades to EMPTY frame / places hollow on copy-paste-drag
- "copy-paste of an instance degrades it into an EMPTY FRAME (bug!) — avoid; use ctrl+D duplicate, or Insert from Assets… drag degraded the rows to empty frames — same bug as copy-paste" (broking-search#5)
- "Many component instances render EMPTY (bug): Input box/Basic, Button Type/Tabs, Button Type/Tags, Button Type/Toggle all place hollow (children exist but don't paint; detach doesn't fix). Working instances: Header/Collapsed-Fund ✓, Data/LTP Price ✓" (broking-place-order#2)
- "The tabs component doesn't render its nested instances" (broking-place-order#2)
Why app: the node tree contains the children (layers panel shows them) but the canvas paints nothing — renderer/instancing bug, not agent error. Distinct from known 12/14 (text-specific) and from seed geometry defects.

### N3. Vector overrides/swaps inside instances don't render — (F) cross-job
- "Known bug: vector icons revealed/swapped INSIDE instances don't render; fresh top-level icon instances DO render" (broking-search#2)
- "vector fill/stroke overrides DO NOT RENDER (panel shows override but canvas doesn't update). Workaround used: Detach Instance, then edit the raw vector" (broking-stock-detail#8)
- "…vectors inside instances does NOT render (known bug) — avoided" (broking-watchlist#1); "swapping a nested icon to it renders broken sliver" (broking-search#5); "Default radios (Market/IOC) rendered as broken 'C' arcs: fixed by double-clicking into each outline shape (enters vector edit) then Escape — re-renders full circle" (broking-place-order#8)
Why app: same document renders correctly after detach or vector-edit round-trip — pure renderer state bug.

### N4. ALL-CAPS text-transform corruption on retype
"CAPS BUG: retyping content in row-name nodes (Typography/Button style) sometimes renders ALL-CAPS. Fix: select node → [Case ~ none + re-apply style]… Row 1 name now renders 'RECEIPT BANK' (CAPS BUG triggered by width edit)" (broking-ledger#5, 3+ hits). Why app: a width edit flips the rendered letter-case with no user-visible property change. First sighting in the cohort; possibly related to ptdev (D) strikethrough-decoration style-binding break (text-style attribute corruption family).

### N5. Instance internals don't stretch / corrupt on resize — (B)/(C) cross-job
- "KNOWN BUG: stretching frames INSIDE component instances renders stale (e.g. inner Inp[ut]…)" (broking-account-recovery#4)
- "inner box does NOT stretch when instance is resized (render bug) — keep at native 311 width" (broking-account-recovery#10, login-flow#10)
- "CRITICAL BUG: Table/List instances get corrupted inside auto-layout containers (inner text offsets break, texts clip at left edge, height shrinks 186→162)" (broking-ledger#8)
- "DS 'Table Row/Style' components (17/19/21/22-variant sets) break on ANY child override (label edit/visibility toggle)" (broking-watchlist#2)
- "The icon's inner elements are broken from resizing… Even fresh, this icon renders broken" (broking-account-recovery#8); "The logo is broken from the earlier resize" (broking-account-recovery#1)

### N6. Variables panel broken — (A) cross-job
"The Variables panel seems partially broken (shows undefined). Let me close it and inspect the design tokens directly on canvas" (broking-order-confirmation#6). Single transcript here; matches ptdev (A).

### N7. Undo corrupts layout / restores wrong state
- "Undo corrupted row 1's layout. Let me delete row 1 and recreate it from row 2" (broking-watchlist#2)
- "only card 1 was corrupted by undo… delete this corrupted card (its chip/text order can't be fixed inside an instance)" (broking-orderbook#2)
- "undo left card broken → had to delete + re-copy from frame 01" (broking-orderbook#5)
Why app: Ctrl+Z produces a state that never existed (mangled child geometry) instead of the previous state. Candidate — 3 transcripts, all around instances in auto-layout.

### N8. Keyboard chords / Tab handling dead (same as broking-opus N6)
- "ctrl+alt+g (frame-wrap) does NOT work" (broking-ledger#4, order-confirmation#9, account-recovery#1, my-queries#9 + more)
- "Tab char in `type` doesn't work as key; use separate field clicks" (broking-place-order#1); "The tab char corrupted the field. Let me fix X and Y separately" (broking-place-order#8); "one field at a time; Tab doesn't work" (broking-orderbook#9)

### N9. Layers-panel drag limits (same family as broking-opus N5)
"Dragging layers INTO instance internals does NOT work; into plain frames works" (broking-ledger#4); "drag-reorder inside instances IMPOSSIBLE (fresh insert from Assets has correct order)" (broking-orderbook#2); "Drag-into a component main doesn't work. Let me try cut + paste-into" (broking-settings#7); "SHIFT+A / structural ops DO NOT WORK on multi-selection (silently fails)" (broking-place-order#7); "shift+A doesn't work across different parents" (broking-place-order#3).

### N10. Misc single-transcript candidates (weak, for the record)
- Text renders first character only: "'Booked P~L' text still renders broken (only 'B' shows)" (broking-funds#4) — extreme stale-measurement (class 4) variant?
- Numeric content renders wrong: "overview card currently renders '₹1,245.60' possibly as '₹1.245.60'/'₹25.60' glitch in some screenshots" (broking-charges-sheet#10) — glyph corruption family (cf. broking-opus middle-dot N3).
- Canvas "dead strip" where clicks don't land; scroll canvas to move the row into a clickable zone (broking-holdings#9).
- Stale render at drop spot; visibility toggle forces re-layout (broking-settings#1); "children sometimes keep stale absolute positions inside AL frames (don't relayout). Fix: change gap Auto→fixed" (broking-place-order#3); "still no relayout — looks like a stale-layout bug. Reload the app to force recompute" (broking-charges-sheet#10) — stale-layout family beyond text (classes 4/6), matches ptdev (H).
- "renaming via right panel header doesn't work" — layer rename only works in the layers tree (broking-place-order#9, orderbook#2).

## Seed CONTENT defects (not app classes — new instances noted per playbook)
- `Icons/Basic/Arrows/ArrowLeft` renders right-pointing (many transcripts, same as opus job).
- `Icons/Basic/Info` broken (i outside circle) — charges-sheet#1/#5/#8, account-recovery#2/#6/#9; `Icons/Lock` also misaligned, `Icons/Clock` clean (account-recovery#6).
- Broken 17-variant legacy `Table Row` duplicate set; also 19/21/22-variant sets fragile (settings#4/#5/#6, watchlist#2).
- `Button Type/Toggle` 5-variant broken brick 76×50; 4-variant OK (settings#6/#7).
- 4-variant Radio renders broken ovals; 3-variant set clean (settings#4/#7/#8, place-order#10); Radio "Default variant's vector is broken in the DS — no arc controls" (settings#8).
- `Label/Exchanges` NSE 19px "NS/E" wrap — "also broken in DS" (search#3/#8/#9, charges-sheet#5).
- "Mobile - Responsive (New)/Paragraph" and "Body(old)/HKG Light 12px" styles have BROKEN FONTS — text disappears (my-queries#9, charges-sheet#4/#9, order-confirmation#3/#10, profile#1/#9) — seed font binding driving known class 14.
- `Colors/Greyscale/White` resolves dark (charges-sheet#3).
- Brand logo renders as broken-image placeholder at low zoom (login-flow#4 says fine at high zoom; watchlist#2/login-flow#9 report real breakage after ops).
- `Card/Watchlist` master has right Column at X~303 overflow — "the bug is in the main component itself" (login-flow#3, watchlist#9).
- `Icons/TrendDown` ships a stray 16px red "err…" square vector that must be hidden per instance (watchlist#3); TrendUp xs breaks after swap (watchlist#8).
- Market-Depth card background vectors have phantom height (stock-detail#10).
- Seed copy error: "TCS strip says 'RMS: Margin shortfall of ₹12,450' but should be 'RMS: Quantity exceeds freeze limit'" (broking-orderbook#5).
- Status-bar time text doesn't render (charges-sheet#5 "Time's text style" suspected missing font).

## Verdict
NEW classes found: YES.
First-sighted in this cohort: N1 variant-switching-no-commit (strongest, ~10 transcripts, with hidden-native-select mechanism lead), N2 instance-degrades-to-empty-frame on copy/paste/drag, N4 ALL-CAPS retype corruption, N7 undo-corrupts-layout.
Cross-job confirmations of ptdev taxonomy: N3=(F) nested vector no-render, N5=(B)/(C) instance-internals stale on resize, N6=(A) variables panel, stale-absolute-positions=(H).
Shared with broking-opus: keyboard chords dead, layers-panel drag inert, zoom quirks.
