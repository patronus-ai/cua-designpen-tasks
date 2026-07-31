# QA items — env_linter 259c0fcc (ptweb-opus, sampling job 7cf836b0) — 2026-07-31

6 itemów w raporcie. 1 designpen app-bug item (zbiorczy, pokrywa 6 znanych klas), 5 pominiętych.

## Itemy designpen (app bugs)

### i3 — "OpenPencil editor state bugs (non-persisting bindings/instances, stale renders, dropped keystrokes) create exactly the defects the zero-tolerance gates punish"

- **Klasy:** #1/#2 binding- i instance-override non-persistence (text-fill/style binding overrides nie persystują → agenci hardcode'ują hex → `unboundFillsCount`), #4/#6 instancje znikają lub trzymają stale child geometry po resize, **#9 numeric-first-keystroke-drop** ("120" → "20" — off-scale spacing; to jest źródłowy item dla taska 009), **#11 assets-drag-misparent** (drag z Assets ląduje w page root / złym parencie; źródłowy item dla taska 011), **#13 layer-reorder/tree** (layer-tree re-parenting failures), **#16 export-fig-timeout/flip-flop** (repro w kontenerze: kolejne exporty tego samego dokumentu flip-flopują między dwoma stanami — komponent obecny vs nieobecny; run 4cafc83e graded na stale exporcie). Dodatkowo CDP command timeouts (run 0b6868b4 utknięty w `running`) — harness-adjacent, nie nowa klasa appki. Brak nowej klasy.
- **Skrót:** Potwierdzone przez claudescope (job 8b957e3d) na add-address, payment-failed, personalising, referral, podcast, profile, registration. Autor QA sam zreprodukował state-sync raciness w kontenerze (export flip-flop). Znaczenie: grading to zero-tolerance conjunction, więc jeden nie-spersystowany binding / jeden stale 6px spacing / jeden mis-parented node = 0. Meta: severity=warning, discipline=technical, failure_modes=[application_bug, tool_wrong_data, intermittent_failure].
- **Run ID-y:** 0b6868b4-bc2a-420b-b1cf-9882cde4ac68 (podcast, stuck running), 4cafc83e-d91f-4ebd-99e4-4c493a95683a (podcast, stale export przy gradingu).

## Pominięte (rubryki/grading/seed — jedna linia każdy)

- i0 (critical): reward-hack — owinięcie niechlujnej pracy we własny komponent zeruje każdy gated count (1.0 vs 0.0 u wszystkich uczciwych; repro upstream QA na payment-failed, ~15 akcji GUI).
- i1 (critical): każdy run 13 problemów = 0.0 — Spacing∼Layout 0/87 przez missingPadding na root frame, offScaleRadius na kołach (radius 200 vs 100 piksel-identyczny), autoLayoutOff na ilustracjach; runy a2e1650e, 6c244c23, f53f33f4, c33668df.
- i2 (error): seed daje logo tylko jako surowy FRAME z 14 hardcoded vector fills w masterze Navigation Bar — skopiowanie (nakazane promptem) oblewa Color gate; luka seedowa; runy b38633c8, 46c43c74, 043a76da, be63c5b0, 923d7bde, c33668df, 4bc90676, ccef4036.
- i4 (info): 13 rubryk cytuje nieistniejące pola (instancesPlaced/authoredContainers); 8 single-screen rubryk wymienia nieistniejący item "Flow clarity"; run 043a76da.
- i5 (info): tekst agenta z canvasu przekazywany verbatim do promptów graderów (deliverableTextByFrame) — injection surface, mitygacja tylko framingiem.
