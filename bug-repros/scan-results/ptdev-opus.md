# designpen v6 ptdev opus-5 10x — full scan 2026-07-31

job: 9628fa83-39ee-46f0-8622-3083505c78e2
rows scanned: 146/170 (completed/all)

## Known-class hit table

| class | transcripts w/ hits | total hits | strongest excerpt (scrubbed, ≤200ch) |
| --- | --- | --- | --- |
| 1 color-style-binding-no-repaint | 13 | 33 | "Color style binding doesn't repaint unless you first set the raw hex in the Custom tab to the style's exact value, THEN apply the style" (ptdev-notifications#9) |
| 2 instance-override-revert | 21 | 40 | "Instance-swap overrides on instances NESTED INSIDE another instance are NOT serialized. They revert to the component default on any page switch/re-render (tested with 6s wait, and with swap+Detach Instance — both revert)" (ptdev-menu-drawer#1) |
| 3 component text-property dropped | 0 | 0 | no signature hits this job |
| 4 stale-text-measurement | 16 | 43 | "CRITICAL BUG — stale text widths: after changing a text's content (esp. in copied/pasted instances), hug widths don't recompute and text clips" (ptdev-ask-expert-hub#4) |
| 5 fixed-frame-auto-expand | 18 | 31 | "WARNING: the 360-wide screen frame auto-grew to 482 when an over-wide child was added" (ptdev-start-talk-step#3); also grew to 524→n/a, 546 (ask-expert-hub#6), 1151 tall (help-center#2) |
| 6 fill-container-stale-width | (in p_bug/p_staletext) | ~6 | "Critical bug: 'Fill container' width inside component INSTANCES computes wrongly (ignores siblings). Fix: use fixed widths" (ptdev-help-center#1); "when another sibling is added, the fill width does NOT recompute" (ptdev-help-center#8) |
| 7 negative-wrap-gap | 8 | 20 | "shift+A wraps selection in a new AL frame appended at END of parent (defaults to horizontal + negative gap — fix flow/gap/alignment after)" (ptdev-bookmarks#10) |
| 8 special-character-input | 146 | 3776 | "Note: '—' have no US-keyboard key event and were inserted directly — no keydown/keyup fired for them" (ptdev-ask-expert-hub#8; also '₹') — driver note fires on every em-dash/rupee type; present in every transcript |
| 9 numeric first-keystroke drop | 1 (+2 corroborating) | 2 | "Without ctrl+a the first character gets eaten (e.g. '286' becom…)" (ptdev-partner-form#6); "triple-click → Ctrl+A → type value → Enter (the first keystroke can be dropped without Ctrl+A)" (ptdev-menu-drawer#1) |
| 10 assets-panel hang | 1 | 2 | regex hit is a mislabel (matched the Assets-panel GLOBAL RESET excerpt, see NEW-A below); no actual hang/freeze evidence this job |
| 11 assets drag misparent | (in p_bug) | ~2 | "Dragging a component from Assets onto an existing instance can drop INSIDE it" (ptdev-ask-expert-hub#4) |
| 12 text invisible after duplicate/move | (in p_invis) | ~4 | "Do NOT move frames via cut/paste or layers-panel drag — this produced a rendering bug where the frame and its children became invisible on canvas (had to delete and redraw)" (ptdev-help-center#4); render desync after cut/paste of AL frame w/ hidden children (ptdev-vip-invite#7) |
| 13 layer reorder tree≠visual | (in p_bug) | ~3 | "Layer reordering does NOT work (drag in layers panel, 'Send to back'/'Bring to front' all fail) → must add children to auto-layout frames in order" (ptdev-notifications#4) |
| 14 text style renders invisible | 9 | 22 | "Text style `Body/sm` (14/20) renders INVISIBLE (missing font) — do not use" (ptdev-live-qa#10, partner-form#2, live-event-detail#8, start-talk-step#9); "AVOID 'Heading 1_21px' — renders invisible (broken font)" (ptdev-help-center#3) |
| 15 canvas focus loss | 105 | 224 | "Could not type '44': no editable element is focused (active element: other:BUTTON). Click the target input or text field first" (ptdev-help-center#6) |
| 16 export_fig timeout | 0 | 0 | no hits (p_export, p_internal both zero this job) |

## NEW candidate classes

### NEW-A: Variables panel broken / collections render empty
What breaks: the Variables panel/dialog does not list collection contents — agents across many problems independently declare it non-functional and fall back to shared styles. List rendering itself is buggy, not just empty seed data.
- "image styles exist: `Avatar/Bonnie Green`… The Variables panel itself is broken/non-functional, but color styles work" (ptdev-booking-calendar#2)
- "Variables collections exist but are broken/empty (only junk entries) — use shared color/text styles instead" (ptdev-bookmarks#3); same verdict ptdev-payment-options#2, ptdev-menu-drawer#6, ptdev-ovulation-calculator#6
- "Variables dialog list rendering is buggy (row…)" (ptdev-ovulation-calculator#10)
Why app: panel UI fails to render collection rows in-editor; independent of agent/harness (observed via plain UI reads). Caveat: seed collections may genuinely contain junk — but "dialog list rendering is buggy" points at the panel itself.

### NEW-B: stroke geometry stale after resize (strokes render at original baked width)
What breaks: resizing a frame/instance re-renders fills but strokes keep the component's original geometry; border appears at old width.
- "Strokes do NOT re-render on resize. If you resize a DS input component (or its inner field)…" (ptdev-partner-form#1)
- "Resizing nested instance children is buggy: a frame's stroke geometry renders at its ORIGINAL baked width even when the layout width changes (fill renders correctly)" (ptdev-partner-form#6)
- "a frame's **stroke** inside an instance will not repaint beyond the component's original width unless you change Stroke Position from Inside → Center" (ptdev-start-talk-step#10)
Why app: pure canvas-render defect reproduced via UI resize; workaround (stroke position toggle) forces repaint — classic stale-render-cache. Distinct from class 1 (style binding) and class 4 (text measurement): here vector stroke geometry is stale.

### NEW-C: resizing an instance does not re-layout its nested children
What breaks: setting a new W/H on a component instance leaves internal auto-layout children at baked sizes (clipped/overflowing) until each child is manually toggled.
- "CRITICAL TOOL BUG: resizing a component *instance* does NOT reflow its internal children (stale widths, clipped text). Avoid resizing instances" (ptdev-ovulation-calculator#6)
- "Known tool bug (stale layout in instances): resizing an instance root does NOT re-layout its nested children. Fix by explicitly setting a n…" (ptdev-help-center#2)
- "KNOWN RENDER/DATA BUG: frames *inside* an instance (e.g. the Dropdown's `Form`) do not visually resize when stretched — their fill renders at the…" (ptdev-start-talk-step#3)
Why app: layout engine skips relayout pass for instance subtrees on root resize; broader than known classes 4/6 (covers frames, fills, strokes, not just text/fill-container width).

### NEW-D: strikethrough text decoration breaks text-style binding
What breaks: applying Decoration→Strikethrough via the text-options popover detaches/breaks the bound text style.
- "IMPORTANT BUG: Applying text decoration (strikethrough) via the text-options popover (icon at 991,407 → 'Decoration' row → S) **breaks the text style binding** (style…" (ptdev-payment-options#10)
- "all colors/type bound to styles (except the documented strikethrough exception)" (ptdev-payment-options#8)
Why app: deterministic UI action → data regression (binding lost); agent had full workaround discipline, observed twice across attempts of the same problem.

### NEW-E: override reset triggered by RENAMING an instance / by unrelated edits
What breaks: class-2 family but with previously undocumented triggers — renaming an instance, creating a new text layer, creating another instance from Assets, or multi-select color-style application, each resets nested overrides.
- "RENAMING AN INSTANCE RESETS ITS NESTED OVERRIDES (icon swaps reverted to default) → Always rename instances BEFORE doing swaps/overrides" (ptdev-feedback#5); "The overrides reset from renaming. I'll redo swaps last" (ptdev-payment-options#4)
- "(icon swaps + nested vector colors) get GLOBALLY RESET when a new component instance is created from the Assets panel or when copying layers out of an instance. Also, changing a component *property* (e.g. Button `Label`) resets that…" (ptdev-feedback#10)
- "CRITICAL BUG FOUND: applying a color style to MULTIPLE icon instances at once (via multi-select Selection colors) RESET their instance sw[aps]" (ptdev-help-center#6)
- "swapping a nested icon instance inside a component instance reverts to the component default whenever a new text layer is created (or the doc re-renders)" (ptdev-feedback#1)
Why app: same nonpersistence defect as class 2 but the trigger set is much wider than page-switch/Ctrl+D — worth folding into the 002 repro task as extra steps.

### NEW-F (weak, 1 transcript each): misc render/selection defects
- Timer component instances "do not appear in the Layers panel tree and are not click-selectable on canvas (but they do render and their properties…)" (ptdev-live-event-detail#2)
- "Many lucide icons render broken (only partial paths): `lucide/zap` renders as a diagonal sliver, `lucide/clock` as an arc+line" (ptdev-question-status#8); "swapping lucide/star into the 12×12 badge icon slot rendered broken/clipped" (ptdev-payment-options#10)
- "Character-level text coloring does NOT work (applying a style to a selected character range applies to whole layer / doesn't repaint)" (ptdev-menu-drawer, single hit)
- "Primary-axis alignment in horizontal auto-layout does not work via the 9-dot alignment grid (only cross-axis)" (ptdev-vip-invite#2)
- "Boolean component properties bound to visibility are NOT persisted" (ptdev-feedback#1)
Why app: all observed in-editor via plain UI; single-transcript each, need verification against app code before filing.

Not counted as app bugs: Ctrl+Alt+G / `t` / `f` keyboard shortcuts "don't work" (many transcripts) — consistent with the known Linux-container keyboard/modifier trap, not necessarily the app; Tab-between-fields not working; Delete-vs-Backspace. Noted only.

## Verdict

NEW classes found: **yes** — NEW-A variables-panel-broken, NEW-B stroke-geometry-stale-on-resize, NEW-C instance-resize-no-relayout, NEW-D strikethrough-breaks-style-binding, NEW-E override-reset-extra-triggers (extends class 2), plus weak single-transcript candidates in NEW-F.
