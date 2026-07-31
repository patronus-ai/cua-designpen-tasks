# QA items — env_linter 81710459 (mm-opus, sampling job e9ee9a6e) — 2026-07-31

8 itemów w raporcie. 1 designpen app-bug item (zbiorczy, z jednym wariantem wartym obserwacji), 7 pominiętych.

## Itemy designpen (app bugs)

### i4 — "OpenPencil editor corrupts or silently reverts valid work (stale layout/repaint, instance-override loss, copy/paste corruption), and the corrupted state is what gets gated"

- **Klasy:** #6 fill-container-stale-width ('Fill container' → stale widths), #1 color-style-binding-no-repaint (geometria/paint nie odświeża się po poprawnych edycjach; klaster `severe_stale_layout_render_engine`, rated critical), #2 instance-override-revert (overrides tekstu/filli/wariantów/icon-swapów cicho wracają do defaultów mastera po page switch / copy-paste / undo; run 9b30d84d oblany na `unoverriddenRowCount: 4` — wszystkie 4 wiersze Settings pokazywały default "Row title|Secondary text" przy gradingu; klaster `moderate_instance_override_state_loss`), #15 canvas-focus-loss ("Could not type … no editable element is focused" w obu czytanych transkryptach policy), #8-wariant special-character-input ("Unsupported key: plus" — klasa #8 dotyczy £/–/·; "+" to ten sam mechanizm, nowa instancja znanej klasy, nie nowa klasa).
- **Wariant do obserwacji:** copy/paste wrapperów **korumpuje zagnieżdżone instancje** — w jednym przypadku cicho zepsuł wcześniej ukończony deliverable (klaster `moderate_buggy_tool_environment`). Najbliżej klasy #2 (revert przy duplikacji), ale "korupcja" (nie revert) nested instances przy copy/paste może być odrębnym mechanizmem — kandydat na rozszerzenie repro-taska 002 albo nową klasę, wymaga weryfikacji w kodzie appki przed zgłoszeniem.
- **Skrót:** Klastry claudescope pokrywają wszystkie 9 problemów mm na bieżących wersjach; wcześniejsze env-lintery potwierdziły te same defekty interaktywnie (poprzednie itemy 04bd5ab8, ce85a848, 093224e2). Ciche reverty są przy gradingu nieodróżnialne od no-opów agenta. Meta: severity=error, discipline=technical, failure_modes=[application_bug, tool_wrong_data].
- **Run ID-y:** 9b30d84d-6df6-4408-aeb8-8801033e15c9 (mm-account-settings, unoverriddenRowCount:4), 1ce409b7-2c4c-4960-9080-2bcdfb56f70d (pass, friction w transkrypcie), 05903908 (fail, friction w transkrypcie).

## Pominięte (rubryki/grading/seed — jedna linia każdy)

- i0 (critical): reward-hack — owinięcie deliverable we własny komponent zeruje każdy reward-gating count (exploit/control pair upstream na mm-onboarding-carousel); jedyne dwa passy środowiska (1ce409b7, 21512a6d) to all-instance assemblies.
- i1 (error): cała waga rubryki na zero-tolerance 6-gate conjunction — 186/188 runów = 0.0 (missingPadding na root frame w 62/85 oblanych Spacing; offScaleRadius na pill radius 100; belowTouchTarget na dekoracyjnych ikonach 18×18; autoLayoutOff na pinned bottom nav); runy 05903908, 901218ba, 42d85b75, fd390d8f, 3dcf2fc7, 066edd29, b15a8e67.
- i2 (error): seed mm-v4.fig zawiera shared text styles 8–10px (Micro/Regular 8, Caption/Regular 10, Caption/Light 10), a Typography gate oblewa fontSize<12 nawet dla stylów seedowych — luka seed-vs-gate (znana z pamięci: mm 8–10px vs belowMinFontSize); runy dd459e15, 82995c57, 76c894ec.
- i3 (error): 23% gradingów (20/88) mierzy stale export, a rubryka każe scoring mechaniczny z niego — ścieżka gradingowa (harness), aplikacyjna strona = klasa #16; runy 5added46, 42d85b75, 547ee17b, b39e8a96.
- i5 (info): rubryka cytuje pola, których skrypt nie emituje (instancesPlaced, authoredContainers, componentPropertyValues).
- i6 (info): tekst agenta z canvasu w promptach graderów verbatim — injection surface, mitygacja framingiem.
- i7 (info): "Overall pass" na 7 single-screen problemach cytuje nieistniejący item "Flow clarity" — kosmetyka copy-paste.
