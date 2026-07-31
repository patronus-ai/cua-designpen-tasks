# designpen v6 ptdev fable-5 10x — full scan 2026-07-31

job: 604c7b2d-6483-47e5-8820-ea99ae50ed96
rows scanned: 164/170 (completed/all)

## Known-class hit table

| class | transcripts w/ hits | total hits | strongest excerpt (scrubbed, ≤200ch) |
| --- | --- | --- | --- |
| 1 color-style-binding-no-repaint | 6 | 11 | "BUG/WORKAROUND: replacing an EXISTING paint's style does not re-render (stays old color). Must REMOVE the fill/stroke (– button) t[hen re-add]" (ptdev-question-status#10); "Selection colors bulk swatch exists but icon recolor doesn't repaint" (ptdev-partner-form#2) |
| 2 instance-override-revert | 17 | 30 | "Layers-panel drag reparent RESETS nested instance icon swaps (labels/visibility overrides survive; swaps revert to master's globe/chevron-right). Canvas-drag reparent PRESERVES swaps (verified by test)" (ptdev-menu-drawer#4) |
| 3 component text-property dropped | 0 | 0 | no signature hits this job |
| 4 stale-text-measurement | 15 | 30 | "During this final QA pass I also fixed a real rendering bug: all tab labels (both screens) had stale text measurements causing the 'Live' tab to overlap 'Parent Talks'" (ptdev-bookmarks#5) |
| 5 fixed-frame-auto-expand | 40 | 55 | "Root frame grew to 1055. Set H back to 754" (ptdev-live-qa#6); heaviest class this job — grew-to incidents in 40 transcripts (369, 373, 397, 425, 444, 491, 586, 619, 622, 623, 692, 704, 794, 826, 966, 1055, 1058…) |
| 6 fill-container-stale-width | (in p_bug/p_staletext) | ~6 | "Form card frame FIXED width 328 — 'Fill container' is buggy here, computes stale 392, so left fixed" (ptdev-ovulation-calculator#6); "'Fill container' width is buggy/doesn't reflow — set explicit numeric widths instead" (ptdev-question-status#4) |
| 7 negative-wrap-gap | 18 | 42 | "shift+A wraps selection in auto-layout frame BUT often defaults to horizontal flow with bogus negative gap" (ptdev-booking-calendar#10); live incidents in 10+ transcripts ("Wrapped horizontally with negative gap", bookmarks#9) |
| 8 special-character-input | 149 | 3172 | "'—' have no US-keyboard key event and were inserted directly — no keydown/keyup fired" (driver note; fires on em-dash/₹/· in every transcript) |
| 9 numeric first-keystroke drop | 0 | 0 | no p_first hits; no independent evidence found this job |
| 10 assets-panel hang | 1 | 2 | regex mislabel (zoom-advice text mentioning Assets panel, ptdev-search#5); no hang/freeze evidence this job |
| 11 assets drag misparent | (in p_bug) | ~3 | "Warning: dropping over existing elements nests into them… Safer: drop on empty canvas, then reparent" (ptdev-search#10); "inserting Maskedpic into instance children does NOT work — inserts at frame root instead" (ptdev-search#7) |
| 12 text invisible after duplicate/move | (in p_invis) | ~5 | "Pasted/moved text nodes may render INVISIBLE until inline-edited (double-click into text, ctrl+A, retype, Escape)" (ptdev-vip-invite#7); "Some copied text nodes don't render (invisible glyphs) until content is edited" (ptdev-vip-invite#7) |
| 13 layer reorder tree≠visual | (in p_bug) | ~3 | "Layer drag-reorder in Layers panel does NOT work reliably; ']'/'[' don't work either. To fix a broken instance, delete it and re-drag fresh from Assets" (ptdev-notifications#7); "Reordering children INSIDE an instance does NOT work" (ptdev-live-event-detail#1) |
| 14 text style renders invisible | 12 | 27 | "'Heading 1_21px' style has BROKEN font (renders invisible)" (ptdev-live-event-detail#1); "Text is invisible with this style. Let me try another style to diagnose" (ptdev-payment-options#9); Proxima Nova styles "render INVISIBLE" (known seed-font gap) |
| 15 canvas focus loss | 126 | 288 | "Could not type … no editable element is focused (active element: other:DIV). Click the target input or text field first" (multiple) |
| 16 export_fig timeout | 0 | 0 | no hits (p_export, p_internal both zero this job) |

## NEW candidate classes

### NEW-1: icon vector renders broken after swap / scale (partial paths, broken arcs)
What breaks: swapping an icon instance or scaling an icon slot leaves the vector rendering as broken partial shapes (arcs, slivers, faint dashes); undoing/deleting and re-dragging is the only fix.
- "the original Icon/comment renders as broken faint dashes at 16px" (ptdev-live-qa#5); "The comment icon renders as a broken arc. I'll delete it and copy the working support icon" (ptdev-live-qa#8)
- "row 5's bookmark icon renders as a broken partial shape. Let me swap it to a different bookmark component" (ptdev-menu-drawer#9); same icon broken in ptdev-menu-drawer#3
- "added Drop shadow effect… but the inner vector did NOT scale — renders as broken partial arc" (ptdev-live-event-detail#8); "The lock renders broken. Let me undo the swap — the original icon was fine" (ptdev-live-event-detail#1); "trailing icon slot renders broken glyphs when swapped (gave up on icon)" (ptdev-ovulation-calculator#2)
Why app: canvas vector rasterization fails on swapped/rescaled icon geometry, observed visually via zoom by many independent agents on different icons/problems. Matches the weak lucide-partial-path signal in ptdev-opus (question-status#8) — cross-job class.

### NEW-2: hidden auto-layout children still occupy flow space
What breaks: layers hidden via visibility (or boolean props off) keep occupying auto-layout flow space until a forced reflow, producing ghost gaps.
- "Not a render glitch — hidden children still occupy flow space in this engine. The clean fix: delete the hidden icon/badge layers in all 5 tabs" (ptdev-vip-invite#9)
- "Stale layout bug: hidden auto-layout children sometimes still occupy space until a reflow is forced (resize the element, e.g. width 327→328)" (ptdev-start-talk-step#4)
- "Navigation/Tab Bar — NOT USED: nested-instance overrides buggy (hidden icons/badges leave ghost space)" (ptdev-vip-invite#3)
Why app: layout engine fails to exclude invisible children from flow computation; agents proved it by deleting vs hiding.

### NEW-3: stroke/border paints at stale width after resize (component-level, reproducible)
What breaks: resizing a component/instance leaves its stroke geometry at the original baked width (fill correct, border wrong).
- "the Input/Dropdown instance whose border painted at a stale width (a component bug that resisted every resize path — verified by reproducing on a fresh instance)" (ptdev-partner-form#8)
- "`Input/Dropdown` — NATIVE 300w; BUGGY when stretched (inner bordered box stays 300 while chevron moves) → was deleted" (ptdev-partner-form#6)
- "Stroke rendering bug: per-side bottom stroke (underline tab indicator) does NOT render on canvas even with weight set" (ptdev-search#3)
Why app: pure render defect, reproduced deliberately on a fresh instance by the agent. Same class as ptdev-opus NEW-B (strokes render at original baked width) — cross-job class; the per-side-stroke-not-rendering excerpt may be its own sub-defect.

### NEW-4: child stuck in absolute positioning, toggle back to in-flow fails
What breaks: a frame becomes absolutely-positioned inside an auto-layout parent and the position toggle won't return it to flow.
- "UNRESOLVED BUG RIGHT NOW: 'Time Section' frame is stuck absolutely-positioned inside/near 'Content'. The crosshair toggle right of Posi[tion…]" (ptdev-booking-calendar#3)
- "layer-drag reparent leaves the dragged item's flow broken (absolute at old coords; others reflow fine)" (ptdev-ask-expert-hub#3)
Why app: layout-mode state corruption via normal UI ops; agent could not undo it with the provided control.

### NEW-5: canvas text editing corruption (typing corrupts node / insert merges words)
What breaks: direct canvas text editing occasionally corrupts the text node or merges words at the insertion point.
- "Canvas typing into a chip label corrupts it (had to delete and re-dup[licate])" (ptdev-booking-calendar#8/#9 summary)
- "Insertion glitch — 'GynacologistPaediatrician' merged. Re-enter edit and double-click that word to select it" (ptdev-plus-conversion#9)
- "Don't press Escape right after panel text edits (reverts); commit by clicking empty canvas" (ptdev-start-talk-step#7)
Why app: text-editing buffer/commit defects in-editor; distinct from class 4 (measurement) and class 8 (key events). Weak-to-moderate: few transcripts, but each verified visually.

### Cross-job confirmations (new in opus scan, seen here too)
- Variables panel broken/empty: "Variables mostly empty/undefined; FontFamily/Body token ~ Roboto" (ptdev-vip-invite#7) — weaker phrasing here, strong in ptdev-opus (NEW-A there).
- Override-reset extra triggers (opus NEW-E): variant switch resets text override ("After switching a Navigation/Tab variant, text override resets to 'Tab'/default", ptdev-search#9; "Variant switched to Filled… but overrides were reset", ptdev-vip-invite#4); cut/paste loses nested overrides ("NEVER cut/paste instances with overrides", ptdev-ask-expert-hub#3); "ctrl+X of FRAMES is buggy/loses content" (ptdev-partner-form#5).
- Misc weak: Indicator/Badge "label text vanishes" (ptdev-notifications#10); calendar State~Disabled cells "render invisible" (ptdev-booking-calendar#9); "Auto" gap computes buggy/stale values (ptdev-ask-expert-hub#8); per-range text styling applies to whole node (ptdev-payment-options#1 — matches opus character-level-coloring note).

Not counted as app bugs: ctrl+alt+g / shift+1 / `t`/`f` shortcut failures (Linux-container keyboard trap); form_input failing on custom combobox buttons (driver limitation); Proxima Nova kerning/invisible (seed font gap, known); Tab key in numeric fields.

## Verdict

NEW classes found: **yes** — NEW-1 icon-vector-broken-render, NEW-2 hidden-children-occupy-space, NEW-3 stroke-stale-width (cross-job w/ opus NEW-B), NEW-4 absolute-position-stuck, NEW-5 canvas-text-edit-corruption; plus cross-job confirmation of opus NEW-A (variables panel) and NEW-E (override-reset extra triggers).
