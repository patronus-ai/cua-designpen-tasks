# bug-repros/ — app-bug regression tasks from the v6 sampling QA (2026-07-31)

**34 tasks**: `001`–`016` mined from the initial v6 sampling QA pass, plus `017`–`034`
added after the full-transcript scan of all 8 v6 jobs (`scan-results/*.md`, 948
completed transcripts) and the env_linter QA cross-check (`scan-results/qa-items-*.md`). Each task walks the exact flow that broke in
production transcripts and reports the standard verdict sentinel: **`verdict: approve`
means the bug did NOT reproduce** (regression passed), `verdict: not-approve` means it
did. Same reward shape as the main QA set, so they run on the existing pipeline.

Naming: `NNN-<job-name-slug>-<issue>` — the job slug is the sampling job in which the
bug was evidenced (per the user convention, e.g. `designpen v6 mm fable-5 10x` →
`designpen-v6-mm-fable-5-10x`).

## Source sessions

v6 cohort (image 20260730-014043):

| job | name |
| --- | --- |
| 27a14af4 | designpen v6 broking opus-5 10x |
| 088bacf2 | designpen v6 broking fable-5 10x |
| 9628fa83 | designpen v6 ptdev opus-5 10x |
| 604c7b2d | designpen v6 ptdev fable-5 10x |
| 7cf836b0 | designpen v6 ptweb opus-5 10x |
| d580a233 | designpen v6 ptweb fable-5 10x |
| e9ee9a6e | designpen v6 mm opus-5 10x |
| 0d00efba | designpen v6 mm fable-5 10x |

Earlier-cohort jobs cited by the QA reports: 641bfe3c `chirag-real-4seeds-v2`
(opus-4-7), f36e7d6e `chirag-real-4seeds-opus5`, 4d2b2812
`chirag-real-4seeds-postfix-opus5-5000t-btf`, 695f1cc4/a12ec6a4/aea562db
`designpen v5 {ptdev,ptweb,mm} fable-5 10x r3-full`.

Evidence: 77 env_linter QA items across 10 QA jobs (only application-bug items used;
rubric/grader/harness/security items excluded), plus a regex scan of 132 sampled
transcripts (2 attempts × every problem × all four fable-5 v6 jobs) for bug
signatures ("no editable element is focused", "render INVISIBLE", "doesn't repaint",
"negative gap", "grew to NNN", "revert to default", ...).

2026-07-31 full scan: ALL completed transcripts of the 8 v6 jobs (948 rows) were
scanned per `scan-playbook.md`, one report per job in `scan-results/`, and the 4
opus-job env_linter QA reports were re-read in full (`scan-results/qa-items-*.md`).
Every app-bug QA claim was cross-checked against the scan (see per-row counters
below and the new-task rows 017–034). Two QA claims found no transcript-side scan
evidence but are not contradicted: class 9 (first-keystroke drop) has 0 regex hits
in its source job ptweb-opus (claim came from claudescope clusters; ptdev-opus and
ptweb-fable each show 1 hit), and class 16 (export flip-flop) has 0 transcript hits
in any v6 job — the QA author reproduced it container-side, outside transcripts.

## Task → evidence map

| task | bug | evidence |
| --- | --- | --- |
| 001 color-style-binding-no-repaint | applying shared color style records binding but canvas keeps old paint / goes white; unbinds to raw hex | ptdev-opus QA (nested `severe`/`moderate_color_style_binding_not_rendering`); broking-opus QA item "bindings apply without repainting"; mm/ptweb v5 QA; broking-fable v6 scan: "Content-field editing sometimes doesn't repaint canvas after variant swaps" (broking-settings#1), p_norepaint=9; v6 full scan: p_norepaint in 57 transcripts across all 8 jobs |
| 002 instance-override-revert | instance overrides (text/fill/icon swaps/variants) silently revert on page switch, Ctrl+D, visiting components page | mm-fable v6 scan: "all per-card Media avatar swaps + header icon/button swaps reverted to defaults after visiting Component…" (mm-notifications#1); ptdev-opus QA `severe_nested_instance_override_nonpersistence` (critical); broking-opus run 72dbb8bd; ptweb-fable v6 "Overrides revert when double-clicking" (ptweb-profile#1); v6 full scan: p_revert in 124 transcripts / 8 jobs (broking-fable 23, ptdev-opus 21); extra triggers documented (rename, new instance, multi-select style, variant switch — ptdev-opus NEW-E) |
| 003 component-text-property-dropped | instance carries componentPropertyValues but master's componentPropertyDefinitions ends up `[]`; labels render placeholder; property un-deletable | job 4d2b2812 runs e3bef233 (ptweb, 7 fields all "Field label", scored 0.0) and afc1e3e6 (ptdev, label stuck on "Button"); v6 full scan: 0 signature hits; pass-2 traces only in broking jobs (exposed property doesn't update render) |
| 004 stale-text-measurement | text keeps stale measured width after content edit; clipped until Fixed↔Hug toggle or retype | ptdev-fable-v5 QA run e4589641 (5 workarounds in one transcript); v6 fable scan p_staletext: ptdev 17, ptweb 16, mm 11, broking 15 ("The first row's value is clipped", mm-wallet-insights#2); v6 full scan: p_staletext in 63 transcripts (+18 combined-4/6 in ptweb jobs) |
| 005 fixed-frame-auto-expand | Fixed-dimension ancestors silently auto-expand when children overflow (360 → 524) | ptdev-fable-v5 QA "root frame grew to 524 once; had to reset W~360"; ptdev-fable v6 scan "Feed Content grew to 361×868" (ptdev-menu-drawer#2); ptweb-fable v6 "Hero Block once grew to 1238" (ptweb-web-landing#2); v6 full scan: p_autoexpand in 117 transcripts (ptdev-fable 40; grew-to incidents 361→2010) |
| 006 fill-container-stale-width | "Fill container" keeps stale fixed width after reparent/sibling change/parent resize | ptweb-fable-v5 QA (Fill-container resolves bogus widths); job 4d2b2812 QA item (Fill container keeps stale fixed widths, run e3bef233); v6 full scan: no dedicated regex — pass-2/p_bug evidence in every job |
| 007 negative-wrap-gap | Shift+A wrap computes large negative gaps (−314); stale itemSpacing −28 written on SPACE_BETWEEN rows | ptweb-fable-v5 run ffd872a2 export artifact; v6 fable scan p_neggap: ptweb 12, ptdev 5 ("often horizontal with weird negative gap", ptdev-ask-expert-hub#1); v6 full scan: p_neggap in 76 transcripts (ptweb-fable 28) |
| 008 special-character-input | typing £ − · — fires no key event / starts a new paragraph, splitting "-£4.00" | mm-fable-v5 QA `moderate_text_input_and_render_defects` (20–30 remediation calls per field); v6 fable scan p_specialchar: ptweb 820, broking 506, ptdev 398, mm 286 ("'–' have no US-keyboard key event", broking-place-order#2); v6 full scan: p_specialchar in 900 of 948 scanned transcripts (every job; · – — £ ₹ + literal \t) |
| 009 numeric-first-keystroke-drop | numeric panel fields drop the first keystroke ("120" → "20") | ptweb-opus v6 QA item ("numeric inputs dropping the first keystroke — off-scale spacing"); v6 full scan: near-absent — 0 hits in source job ptweb-opus; ptdev-opus 1 (+2 corroborating), ptweb-fable 1, mm-fable W-field-adjacent |
| 010 assets-panel-hang | Assets panel (1,500+ grid) render/search hangs the tab; container dies after 5 CDP failures | job f36e7d6e run 241b9dac (52 tool errors, zero deliverable); claudescope QA 8ca1b7d6; v6 full scan: NO hang events in any v6 job (all p_assets hits benign) |
| 011 assets-drag-misparent | drag from Assets drops instance at page root / wrong parent | ptweb-opus v6 QA item ("Assets-panel drag landing components at the page root or wrong parent"); ptdev-fable v6 scan ("Insert instance … items landed clipped inside Home frame; deleted 2 strays", ptdev-menu-drawer#1); v6 full scan: pass-2 evidence in every job (mis-nest / lands at root / appends at end) |
| 012 text-invisible-after-duplicate | text renders invisible after duplicate/move | image-1 cohort (641bfe3c) claudescope cluster "text invisible after duplicate/move"; v6 full scan: p_invis shared w/ class 14 (~103 transcripts); fresh trigger evidence ptdev-fable (pasted/moved text invisible until inline-edited) |
| 013 layer-reorder-visual-mismatch | layer reorder changes tree order but not visual stacking | image-1 cohort (641bfe3c) claudescope cluster; related z-order history RLCU-2668; v6 full scan: 0 direct hits; 'reorder does nothing at all' evidence reclassified to new task 024 |
| 014 text-style-renders-invisible | certain shared text styles render text invisible | ptweb-fable v6 scan: "coarse-named text styles (Body_16px…) DO NOT RENDER (invisible text)" (ptweb-support#1); broking-fable v6: "shared styles Typography/Subheading/Sub4 and Sub4 SemiBold render INVISIBLE" (broking-order-confirmation#1); v6 full scan: p_invis in ~103 transcripts / 8 jobs (shared w/ 12; broking-fable 34) — mostly font-gated seed styles |
| 015 canvas-focus-loss-typing | canvas drops focus between click and type — "no editable element is focused" | v6 fable scan p_focus: broking 62, ptweb 50, ptdev 28, mm 23; job f36e7d6e run 241b9dac (15+ occurrences); v6 full scan: p_focus in 703 transcripts / 8 jobs |
| 016 export-fig-timeout | .fig export never completes on larger docs (60s/240s timeouts even idle); consecutive exports of unchanged doc flip-flop between states | f36e7d6e QA (export_fig dead on 20–33MB seeds, reproduced idle); 4d2b2812 QA (all mm/ptdev/broking gradings on stale autosave); 27a14af4 QA (49% of gradings stale); ptweb-opus v6 reproduced flip-flop; v6 full scan: 0 transcript hits in all 8 v6 jobs; ptweb-opus QA reproduced export flip-flop container-side (runs 0b6868b4, 4cafc83e) |
| 017 variant-switch-no-commit | right-panel variant dropdown selections silently don't commit (mouse+keyboard); hidden native select works | broking-fable v6 scan N1 (~10 transcripts: "Variant switching is 100% BROKEN", login-flow#7; mechanism broking-orderbook#8); broking-opus N1 (~8 transcripts) |
| 018 instance-copy-paste-corruption | copy/cut+paste of configured instances pastes empty shells, drops overrides, pastes wrong image fill, doesn't reflow | mm-opus v6 scan N1 (≥3 transcripts) + mm-opus QA i4 variant; mm-fable N1; broking-fable N2 (degrades to EMPTY frame, broking-search#5); ptdev-fable (NEVER cut/paste instances w/ overrides) |
| 019 variables-panel-broken | Variables panel: all collection tabs show same list, search dead, rows undefined; picker Libraries-tab assignment doesn't render | ptweb-fable v6 scan (5+ transcripts, payment-failed#10); ptdev-opus NEW-A (6 transcripts); broking-opus N7; broking-fable N6; mm-opus N3 — all 4 seed families |
| 020 stroke-stale-after-resize | strokes render at original baked geometry after resize; inside strokes can drop an edge | ptdev-opus v6 scan NEW-B (partner-form#1/#6, start-talk-step#10); ptdev-fable NEW-3 (fresh-instance repro, partner-form#8); broking-opus N2 (right border missing, place-order#8); ptweb-opus (rounded-rect arc-only strokes, web-landing#7) |
| 021 instance-resize-no-relayout | resizing an instance doesn't re-layout nested children (stale widths, clipped text) | ptdev-opus v6 scan NEW-C ("CRITICAL TOOL BUG", ovulation-calculator#6, help-center#2); broking-opus N8; broking-fable N5 (Table/List corrupts, ledger#8); ptweb-opus (personalising#2) |
| 022 icon-vector-broken-after-swap | swapped/scaled icon vectors render broken: partial paths, arcs, slivers, black squares | ptdev-fable v6 scan NEW-1 (6-7 transcripts: live-qa#5/#8, menu-drawer#3/#9, live-event-detail#1/#8); mm-opus N2 (black square, home#3, account-settings#1); broking-fable N3 (nested vector swaps don't render, detach fixes); ptdev-opus lucide partial paths |
| 023 hidden-children-occupy-space | hidden auto-layout children still occupy flow space (ghost gaps) until forced reflow | ptdev-fable v6 scan NEW-2 (3 transcripts; proven by delete-vs-hide, vip-invite#9; 1px-nudge reflow workaround, start-talk-step#4) |
| 024 layers-drag-reparent-inert | layers-panel drag to reorder/reparent does nothing (no feedback, tree unchanged) | broking-opus v6 scan N5 (~8 transcripts, cut/paste workaround); broking-fable N9; ptweb-fable NEW-1 (ALL routes incl. cut/paste of frames fail, referral#9); ptweb-opus NEW-2 (frame ctrl+X empty clipboard); mm-opus (reorder all-fail, notifications#9) |
| 025 swap-instance-dead | Swap-instance dialog row clicks no-op (esp. nested); applied swaps can carry stale overrides and render corrupt | ptweb-fable v6 scan (podcast#5, profile#4); ptweb-opus (profile#4 nested swap dead); mm-fable N3 (swap preserves stale overrides → white-on-white, giftcard-checkout#6/#7/#8) |
| 026 undo-corrupts-layout | Ctrl+Z mangles instance child geometry or reverts earlier unrelated edits | broking-fable v6 scan N7 (3 transcripts: watchlist#2, orderbook#2/#5); mm-fable N2 (reverts unrelated changes, gifting-select-brand#7); mm-opus (overrides lost from undo, wallet-insights#5) |
| 027 middle-dot-glyph-corruption | '·' corrupts glyph advances → overlapping/garbled text (render, not input) | broking-opus v6 scan N3 (ledger#4, multiple hits, retype-content fix); broking-fable (₹1,245.60 renders as ₹1.245.60/₹25.60 glitch, charges-sheet#10) |
| 028 caps-retype-corruption | retype + width edit renders text ALL-CAPS with no property change | broking-fable v6 scan N4 (ledger#5, reproduced 3+ times in-run; "CAPS BUG triggered by width edit") — single-transcript class, task doubles as confirmation probe |
| 029 strikethrough-breaks-style-binding | strikethrough and shared-text-style binding mutually exclusive; Create-style drops decoration | ptdev-opus v6 scan NEW-D (payment-options#10/#8, both attempts); ptdev-opus QA i6 (independent claudescope confirmation, brief-vs-gate conflict) |
| 030 frame-selection-shortcut-dead | Ctrl+Alt+G never fires; same action works from menu; Ctrl+Alt+K works (not the modifier trap) | ptweb-opus v6 scan NEW-1 (7+ transcripts w/ Ctrl+Alt+K control, profile#8, referral#2); broking-opus N6 (~10 transcripts); broking-fable N8; mm-opus N4 |
| 031 apostrophe-breaks-text-measurement | apostrophe/comma in text wedges auto-measurement — content correct, width stale/clipped | ptweb-fable v6 scan NEW-3 (baby-names-hub#7 "CRITICAL BUG FOUND", #3 same fix; profile#8 comma) — deterministic character trigger distinguishes it from class 4 |
| 032 gap-auto-space-between-broken | gap "Auto" (space-between) fails to distribute children / renders stale | ptweb-fable v6 scan (baby-names-hub#6, support#10, consult-booking-form#3); ptdev-fable ("Auto" gap computes buggy/stale, ask-expert-hub#8); broking-opus (gap Auto→fixed forces relayout, place-order#3) |
| 033 panel-header-rename-dead | design-panel header rename never commits; layers-tree rename works | ptweb-fable v6 scan (4 transcripts: consult-booking-form#4, payment-failed#4, registration#3, baby-names-hub#9); broking jobs (place-order#9, orderbook#2) |
| 034 absolute-position-stuck-child | auto-layout child stuck absolutely positioned; toggle won't return it to flow | ptdev-fable v6 scan NEW-4 (booking-calendar#3 "UNRESOLVED BUG RIGHT NOW", ask-expert-hub#3); broking-opus N9 (Shift+A wrap makes 2nd child absolute, account-recovery#8) |

## Out of scope (not app behavior — cannot repro in this gym image)

Documented for completeness; these need env-author fixes in the sampling problem set,
not tasks here:

- **Seed dead component properties** — ptdev 48/200 unwired text props (CTA Label on
  Card/Session 0:946 etc.), broking 20/84, ptweb 15/51, mm 4/148; mm Menu Row
  "Destructive" hardcodes "Delete Account" (0:3604). The app-side mechanism IS covered
  by task 003 using this gym's seed.
- **Seed fonts** — ptdev heading styles bind Proxima Nova, not shipped in the image.
- **mm seed content** — typos "occassion"/"Cancle"/"part%", GAP-logo tile labeled
  "Zara", calendar "September 2019" grid mismatch, missing theme/bank/moon-sun icons.
- **Authoring debris** — broking TEXT 0:13349 "# Frames in scope for corrections"
  (nonexistent node IDs), ptdev SECTION 0:6616 "DUPLICATE CANDIDATES — MANUAL REVIEW".
- **ptdev missing brand-logo asset** vs system-prompt mandate.
- **mm 8–10px seed text styles** vs the belowMinFontSize gate (9/10 mpin runs failed).
- Harness/grading items: 413/32MB request deaths, 12h wall-clock deaths, rubric
  all-or-nothing conjunction, grader prompt injection, stale-export *grading* path,
  click-coordinate 0.8× scaling, open CDP/MCP ports.

## Seeds

Every task loads the SAME production seed its source job ran on
(`bootstrap_data.seed`: `broking-v4` / `ptdev-v4` / `ptweb-v4` / `mm-v4`) so repros
are faithful to the sampling sessions. Tasks 017–034 follow the same rule (seed =
family of the strongest-evidence job); their prompts are seed-agnostic and call out
the known seed content defects so agents don't report those as new bugs. The four .fig files are NOT in the current app
release — see `seeds/README.md` for the wiring required before these tasks can run.

## Running

Definitions follow the standard schema (validated against `gym_browser_use.task.Task`).
To include them in a build, copy the folders into `tasks/` and re-run
`uv run dev/combine_tasks.py task_data/cua-designpen-tasks`, or merge them into
`tasks.jsonl` directly. All tasks set `bootstrap_data.seed` to their family's
production v4 seed (see `seeds/README.md`).
