# QA items — env_linter 75101cdd (broking-opus, sampling job 27a14af4) — 2026-07-31

12 itemów w raporcie. 1 designpen app-bug item, 11 pominiętych (rubryki/grading/harness/security).

## Itemy designpen (app bugs)

### i7 — "Editor bugs corrupt compliant work into gate violations: bindings apply without repainting, instance overrides are lost, auto-layout returns wrong geometry"

- **Klasy:** #1 color-style-binding-no-repaint, #2 instance-override-revert, #4/#5/#6 auto-layout stale geometry (Fill container → 0/stale widths = #6; root frames ballooning 375→398/407 = #5; hug heights collapsing to 0 ≈ #4/#6). Brak nowej klasy.
- **Skrót:** Trzy powtarzalne zachowania OpenPencil zamieniają poprawną pracę w naruszenia liczników: (1) nałożenie stylu koloru/obrysu z design systemu aktualizuje etykietę bindingu, ale nie przemalowuje node'a — agenci uciekają w hardcode hex, co potem wpada w `unboundFillsCount` (gating). (2) Nadpisania tekstu w instancjach giną między edycją a gradingiem: w run 72dbb8bd MID-RUN export zawiera nadpisane etykiety wierszy, a żywy canvas przy gradingu pokazuje defaulty mastera "Title Text"/"Secondary Text" — stan cofnął się bez akcji agenta, run oblał Content. (3) Silnik auto-layout zwraca stale/błędną geometrię ('Fill container' → 0 lub stale widths, root frame 375→398/407, hug heights → 0; claudescope 'moderate_autolayout_and_sizing_engine_bugs'), zasilając `clipped`/`autoLayoutOff`. Workaroundy istnieją (hex-then-rebind, Hug→Fill toggle), więc poniżej progu unrecoverable, ale systematycznie zaniża all-or-nothing gates. Meta: severity=warning, discipline=technical, failure_modes=[application_bug, tool_wrong_data].
- **Run ID-y:** 72dbb8bd-c67e-4e82-80e8-e610062ae24c (ledger).

## Pominięte (rubryki/grading/harness/security — jedna linia każdy)

- i0 (critical): reward 0 na 141/141 runach — Spacing∼Layout gate obciąża root screen frame (missingPadding/autoLayoutOff w measure_artifact.mjs); runy 23f0eeda, 080aecca, 0b890633.
- i1 (error): belowTouchTargetCount klasyfikuje interaktywność substring-matchem nazwy ("Disclosed" zawiera "close") — TEXT/LINE liczone jako tap targets; runy 17a8d5c8, 22e6e1bb, 552313d7, 1882e7c5.
- i2 (error): placeholderTextCount liczy ukryty master-default text w instancjach seedowych (niewidzialny "Field Label" w Keyboard) — kara za instruowane zachowanie; runy 1a41e290, 4e08ca01, 01a49801, 78dd0b7d.
- i3 (error): 49% gradingów (69/141) na stale exporcie — liczniki gate'ów z pliku mid-run; ścieżka gradingowa (harness), powiązana z klasą #16 od strony aplikacyjnej; runy 0959e561, 72dbb8bd, 0b890633.
- i4 (error): reward-hack — owinięcie niechlujnego ekranu we własny komponent zeruje wszystkie gating countery (zweryfikowane end-to-end przez MCP bridge).
- i5 (warning): rubryka DSA cytuje pola measured-reportu (instancesPlaced, authoredContainers), których skrypt nie emituje.
- i6 (warning): unboundFillsCount obciąża fille IMAGE/GRADIENT, dla których design system nie ma tokenów; runy 09a9ec81, 1564e53a.
- i8 (info): nieuwierzytelniony 128-toolowy MCP bridge + CDP na localhost — defense-in-depth (security, nie app-bug w edytorze).
- i9 (info): tekst z canvasu agenta trafia verbatim do promptów graderów (injection surface, mitygacja framingiem).
- i10 (info): "Overall pass" cytuje item "Flow clarity" istniejący tylko w 4/15 rubryk — kosmetyka.
- i11 (info): 3/150 runów padło przy gradingu (GraderIncompleteError, 2 wyjątki harnessa) — runy wykluczone, nie źle ocenione; runy c9aa703c, 02c48a71, 74b98e16.
