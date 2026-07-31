# designpen v6 broking opus-5 10x — full scan 2026-07-31

job: 27a14af4-21e5-4101-affe-c86f8a8486a2
rows scanned: 117/150 (completed/all; 33 non-completed skipped per playbook)

## Known-class hit table

| class | transcripts w/ hits | total hits | strongest excerpt (scrubbed, ≤200ch) |
| --- | --- | --- | --- |
| 1 color-style-binding-no-repaint | 6 (p_norepaint) + many pass-2 | 16+ | "Applying a color style to a fill inside an INSTANCE records the style name but does NOT repaint (tag fill shows Colors/Warning/100 but still renders green #D6F3E9)" (broking-my-queries#5) |
| 2 instance-override-revert | 14 | 22 | "Nested instance overrides do NOT persist across page switches (fills revert to the component's values). TEXT content/style overrides DO persist" (broking-settings#6); "child overrides on instances (deleting/adding children) do NOT persist — instances re-sync to their main component" (broking-my-queries#4) |
| 3 component-text-property-dropped | pass-2 only | ~2 | "`Inner-text` > `Search` (exposed \"Search\" property does NOT update render — must edit nested text layer's Content field)" (broking-holdings#10) |
| 4 stale-text-measurement | 13 | 33 | "fill-width children render at the stale width (e.g. 391 instead of 311). Fix: set Fixed width explicitly" (broking-charges-sheet#1); "CRITICAL BUG: text layer hug-width sometimes does NOT recompute after a Content edit → next sibling overlap" (broking-holdings#3) |
| 5 fixed-frame-auto-expand | 7 | 13 | "Had to reset Account Profile frame W back to 375 once after this bug stretched it to 2010" (broking-profile#4); "screen frame width jumped to 427 once and had to be reset to 375" (broking-order-confirmation#10) |
| 6 fill-container-stale-width | pass-2 | several | "Known bug: 'Fill container' widths don't recompute when sibling content changes — parent frames grow ins…" (broking-profile#10); "widths cascaded wrong: Search Row shows 418 and Search~Filters grew to 450" (broking-search#3) |
| 7 negative-wrap-gap | 5 | 9 | "'Add auto layout' wraps selection in an auto-layout frame (defaults to horizontal with a negative gap — must fix direction + gap)" (broking-my-queries#4) |
| 8 special-character-input | 117 | 2666 | "'·' have no US-keyboard key event and were inserted directly — no keydown/keyup fired for them" (broking-profile#8) — every transcript hits this; chars: · – ₹ |
| 9 numeric-first-keystroke-drop | 0 | 0 | — |
| 10 assets-panel-hang | 2 | 5 | regex hits are benign panel mentions (asset grid items list, broking-place-order#7); NO real hang evidence in this job |
| 11 assets-drag-misparent | pass-2 | several | "drag from Assets onto populated auto-layout frame fails silently. Workaround: drag onto empty canvas (root level), then re-parent" (broking-account-recovery#8); "Drag-and-drop from Assets does NOT work. Insert places the new instance at the END of the currently-selected layer's parent" (broking-place-order#5) |
| 12 text-invisible-after-duplicate | 6 (p_invis, shared w/ 14) | 12 | "some component instances render invisible inside certain frames. The original 'Sheet Footer' frame was corrupted this way and was deleted" (broking-charges-sheet#6) |
| 13 layer-reorder-visual-mismatch | 0 direct | 0 | (`]` z-order note in broking-my-queries#4 describes correct behavior, not the bug) |
| 14 text-style-renders-invisible | pass-2 | several | "some design-system components' text fills are bound to a variable that resolves to a light grey (#BDBDBD) even after applying…" (broking-place-order#1); Composition/Margin-Row "label text nearly invisible" (broking-funds#8) |
| 15 canvas-focus-loss-typing | 88 | 186 | "Could not type '812': no editable element is focused (active element: other:BUTTON). Click the target input or text field first" (broking-profile#8) |
| 16 export-fig-timeout | 0 | 0 | p_export zero hits (matches ptdev scan: bug absent or unexercised in v6) |

p_internal (DevTools internal error): 0.

## NEW candidate classes

Letters (A)–(I) reference the ptdev v6 scan taxonomy (scan-results/ptdev-*.md) where the class was already named — those are cross-job confirmations, not first sightings.

### N1. Variant switching on instances broken (dropdown selection doesn't apply)
What breaks: picking a variant value in the right-panel dropdown silently does nothing, for many component sets; workaround is Create-instance from the DS page or copy an existing instance.
- "Variant dropdowns on instances are BROKEN (selecting a value doesn't apply). Workaround: go to Design System page, double-click into the component set…" (broking-profile#6)
- "`Table Row/Style 1 (List Layout)` variant switching does NOT work (variants have inconsistent/sparse property sets, so only exact matches apply)" (broking-settings#10)
- "Variant switching on DS components is BROKEN/incomplete — `Table Row/Style 1 ~ 2` variants won't change. Don't rely on them" (broking-charges-sheet#10); also broking-ledger#5/#8 (Input box/Basic), broking-settings#2, broking-watchlist#8, broking-charges-sheet#2.
Why app: the dropdown UI accepts the click but the document never changes — editor-side variant resolution, not agent misuse (partly aggravated by sparse seed variant sets, but "selecting a value doesn't apply" reproduces on well-formed sets too). Massively confirmed in broking-fable (see that report).

### N2. Stroke geometry bugs — (B) cross-job
Two manifestations:
(a) Inside-position stroke drops the RIGHT border: "IMPORTANT RENDERER BUG: frames with stroke Position~'Inside' don't render their RIGHT border. Fix ~ set stroke Position to 'Center'" (broking-place-order#8); "The input boxes' RIGHT border does not render (top/bottom/left strokes show, right edge missing). Confirmed it is a renderer quirk" (broking-place-order#3).
(b) Stroke renders at stale width after resize: "Stroke render bug: after resizing a frame with an inside stroke, the stroke renders at the old width. Fix: change Stroke Position…" (broking-account-recovery#3, #8); "`Input box/Basic` stale stroke bug: instances render their border at the original 311px width" (broking-place-order#7, account-recovery#5).
Why app: pure renderer output wrong for a given document state.

### N3. Middle-dot glyph-advance corruption (render, distinct from known class 8 input)
"TEXT RENDER BUG: the '·' (middle-dot) character corrupts glyph advances → overlapping/garbled text. AVOID '·' in new text. Fix corrupted text by retyping content in the Content field. '₹' is fine" (broking-ledger#4, multiple hits). Why app: text with the char renders garbled regardless of how it was inserted; class 8 only covers the missing key event.

### N4. Text-tool text vanishes after applying a fill color style
"CREATING TEXT WITH THE TEXT TOOL IS BROKEN: new text layers vanish shortly after applying a Fill color style. RELIABLE WORKAROUND: Ctrl+C an existing styled text layer, 'Paste here', then edit" (broking-orderbook#5, 3 hits). Why app: layer disappears from canvas after a legal styling op; adjacent to known 12/14 but the trigger (fresh text-tool node + fill style) is distinct.

### N5. Layers-panel drag-and-drop inert (reorder/reparent does nothing)
- "Layer-tree drag-and-drop to reparent does NOT work; use cut/paste instead" (broking-profile#2, profile#9)
- "Layers-panel drag-reordering does NOT work. Plan child/sibling order up-front" (broking-place-order#7)
- "Reparenting layers: drag-and-drop in the layer tree does NOT work. Working method: Ctrl+X → select target → Ctrl+V" (broking-holdings#5); also settings#8, account-recovery#2, settings#5, search#8 ("Dropping 'between' rows does not work").
Why app: consistent across ~8 transcripts and models; the panel gives no drop feedback and never mutates the tree (related to ptdev (E) which covers the override-reset when it *does* work via canvas). Note funds#8 says drop-ON-row works to move INTO a frame but not to root — partial implementation.

### N6. Keyboard chords / Tab handling dead
- Ctrl+Alt+G (Frame selection) never works via keyboard, menu item works — ~10 transcripts (broking-settings#2/#5/#6, search#8, account-recovery#1/#3/#7/#10, funds#6, orderbook#8, watchlist#10, my-queries#8, place-order#1/#5, order-confirmation#9)
- "'Detach Instance' button works (Ctrl+Alt+B does not)" (broking-settings#2); "`ctrl+]` does NOT work" (broking-my-queries#7)
- "Tab between X/Y fields does NOT work — set each field separately" (broking-place-order#6, settings#3)
Why app: in-app shortcut registry misses these; not the Linux Cmd/Ctrl trap (agents use Ctrl correctly and the menu equivalents work).

### N7. Variables panel — (A) cross-job
"Variables panel (left rail) has a bug: switching collection tabs doesn't refresh the list. Avoid" (broking-place-order#10). Single transcript here; matches ptdev (A).

### N8. Instance resize doesn't re-layout / corrupts children — (C) cross-job
- "BUG: `Brand/Logo` does not scale inner content when resized → must stay 40×40" (broking-account-recovery#5)
- "The radio shape got corrupted by resizing. Let me delete it and insert a fresh radio instance" (broking-settings#7)
- "Instance layout staleness bug (important!): instance children cache their layout per-instance-width. After editing a main component, instances…" (broking-place-order#4)
- "Table Row/Style 1 (List Layout) and Table/List have baked/stale child positions — changing te…" (broking-funds#7); "Table/List component's internal layout doesn't recompute with overridden text (values clip)" (broking-funds#4)

### N9. Shift+A wrap makes 2nd child absolutely positioned — (H) cross-job
"wrapping 2 items makes the 2nd child absolutely positioned (broken). Separate items vertically first, or duplicate an already-flowed child" (broking-account-recovery#8).

### N10. Zoom-to-fit broken
"`shift+2` ~ zoom to selection. Zoom-to-fit is broken (stays 2%)" (broking-ledger#8, repeated in its notes). Minor but pure app.

### N11. Misc single-transcript candidates (weak, listed for the record)
- Text tool creates node at page ROOT, not the clicked frame (broking-stock-detail#4).
- "Detaching loses frame FILL style bindings" (broking-settings#2).
- Ctrl+Z unreliable: "an earlier ctrl+z reverted a swap+text edit" (broking-orderbook#1); "Ctrl+Z unreliable — prefer…" (broking-place-order#7).
- Ctrl+D copy inherits a broken/absolute transform from the source (broking-settings#1).

## Seed CONTENT defects (not app classes — new instances noted per playbook)
- `Icons/Basic/Arrows/ArrowLeft` renders a RIGHT-pointing arrow (inner layer literally named "ArrowRight") — ~12 transcripts (profile#1/#5, my-queries#5, search#4/#8/#9, place-order#4/#5/#9, watchlist#10, ledger#5, stock-detail#9, funds#1).
- `Icons/Basic/Info` renders broken (circle + detached/displaced "i") — local version; LIBRARY version fine (charges-sheet#6/#7/#10, order-confirmation#9/#10, account-recovery#1/#5).
- `Button Type/Toggle` 5-variant set renders broken 76×50 (knob mis-positioned); 4-variant fine (place-order#2/#3/#4/#6/#10, settings#7).
- 4-variant Radio Button renders wrong 45×45; 3-variant fine (settings#2, place-order#10).
- `Navigation/Header-Alt2` "Grey Header" variant content overflows left edge (order-confirmation#9).
- `Label/Exchanges` NSE variant inner text fixed 19×10 → "NSE" wraps to "NS/E" (search#6, search#4).
- `Colors/Greyscale/White` style resolves to dark #1B1C1E (funds#1).
- `Navigation/Status bars` "9:41" time text does not render (ledger#5).
- `Composition/Margin-Card`/`Margin-Row` broken hidden children / absolutely-positioned internals (funds#4/#7/#8); `Composition/Search-Input` Inner-text hidden 0-height (search#1).
- `Icons/Basic/RemoveCircle` broken (circle+minus stacked, 36×72); ChevronLeft renders broken diamond in funds#9 (contradicts other transcripts where ChevronLeft is the recommended fallback — per-file corruption?).
- 17-variant legacy `Table Row` duplicate set renders broken (settings#5/#6).

## Verdict
NEW classes found: YES.
First-sighted in this cohort: N1 variant-switching-no-apply, N3 middle-dot glyph corruption, N4 text-tool text vanishes after fill style, N5 layers-panel drag inert, N6 keyboard chords dead, N10 zoom-to-fit stuck.
Cross-job confirmations of ptdev taxonomy: N2=(B) stroke stale/right-border, N7=(A) variables panel, N8=(C) instance resize no-relayout, N9=(H) absolute-positioned wrap child.
