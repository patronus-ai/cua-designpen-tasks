# QA items — env_linter 7c9b594b (ptdev-opus, sampling job 9628fa83) — 2026-07-31

9 itemów w raporcie. 2 itemy z treścią designpen app-bug (jeden czysty, jeden mieszany brief-vs-gate z aplikacyjnym szczegółem), 7 pominiętych.

## Itemy designpen (app bugs)

### i4 — "Canvas app bugs: nested-instance overrides silently revert, color-style binding records but doesn't repaint, auto-layout geometry goes stale"

- **Klasy:** #2 instance-override-revert (nested: icon swaps, recolors → white-on-white, warianty nie persystują; 'severe_nested_instance_override_nonpersistence', critical w claudescope), #1 color-style-binding-no-repaint (styl zapisany w panelu, paint bez zmian; workaround "raw hex w Custom, potem re-apply library style" zostawia hardcode, który zeruje Color gate), #4 stale-text-measurement (tekst w instancjach nie re-mierzy się po zmianie labela), #6 fill-container-stale-width ('Fill container'/'Hug' widths nie przeliczają się), #5 fixed-frame-auto-expand (kaskada 360→378/387px na screen frames; workaround Fixed→Hug "kick"). Brak nowej klasy.
- **Skrót:** Trzy defekty OpenPencil udokumentowane w klastrach claudescope na 13 z 17 problemów (help-center, menu-drawer, notifications, payment-options, start-talk-step, vip-invite, booking-calendar, live-qa, question-status, partner-form, ask-expert-hub, bookmarks, feedback). Koszt: 1400–3200 tur na run + oblanie Color gate, gdy workaround zostawia raw hex. Meta: severity=warning, discipline=technical, failure_modes=[application_bug]. Nie reprodukowane niezależnie w UI (data-verified przez claudescope + grader reasoning).
- **Run ID-y:** brak konkretnych run ID w opisie (klastry claudescope per-problem).

### i6 — "Brief-vs-gate conflicts: payment-options struck-through price can't coexist with shared-text-style gate" (mieszany; aplikacyjny szczegół)

- **Klasy:** NOWA-kandydat — **text-style-application-drops-decoration**: OpenPencil usuwa strikethrough przy nałożeniu shared text style, ponowne nałożenie strikethrough odpina styl, a 'Create style' nie przechwytuje dekoracji — wymagany wizual i binding gate wzajemnie się wykluczają w narzędziu. Nie pasuje do żadnej z 16 klas (najbliżej #14, ale tam tekst renderuje się niewidzialny, tu ginie dekoracja). Item jako całość to contradictory_requirements (rubryka), ale mechanizm dekoracji to zachowanie edytora — kandydat do weryfikacji w kodzie appki przed zgłoszeniem (por. lekcja batch-3: verify app code before filing).
- **Skrót:** (1) ptdev-payment-options wymaga przekreślonej ceny, ale Typography gate oblewa `unstyledTextCount > 0`, a aplikacja gubi przekreślenie przy stylu współdzielonym. (2) ptdev-partner-form: "Send Query disabled until complete" kłóci się z mandatem "visibly interactive/accent" — to czysto rubrykowe. Meta: severity=warning, discipline=non_technical, failure_modes=[contradictory_requirements].
- **Run ID-y:** brak (klastry claudescope, nazwy zredagowane jako [TOK]).

## Pominięte (rubryki/grading/harness/seed — jedna linia każdy)

- i0 (error): dwie heurystyki measure_artifact.mjs mechanicznie oblewają standardową strukturę mobile (missingPadding na root frame; position-blind "overlapping" na scrollowalnym Body); runy cc6a1ac7, 58164ad8, 99c44430, 4cab66a2.
- i1 (critical): wszystkie 265 runów × 17 problemów = 0.0 — jedyny ważony item to six-gate zero-threshold conjunction; runy d5e4aa15, cc6a1ac7.
- i2 (critical): reward-hack — każdy licznik defektów wyklucza node'y w instancjach; owinięcie deliverable we własną instancję zeruje 6 gate'ów (score 1.0).
- i3 (warning): rubryki cytują nieistniejące pola (instancesPlaced, authoredContainers, componentPropertyValues) + sprzeczne rozkazy "derive with bash" vs "do not recompute"; runy a0d30b5c, cac9d74c, d5e4aa15.
- i5 (warning): GraderIncompleteError — odpowiedź gradera ucina się przed ostatnim itemem rubryki (2/170 runów); runy ae4bb561, 6b17327d.
- i7 (warning): system prompt każe umieścić "real brand logo asset", a seed ptdev nie zawiera żadnego logo (tylko TEXT "Parentune") — luka seedowa.
- i8 (warning): tekst agenta z canvasu inline'owany verbatim do promptów graderów (injection surface; mitygacja framingiem, bez escapingu).
