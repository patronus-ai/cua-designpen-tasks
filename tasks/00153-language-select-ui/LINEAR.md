# DesignPen [view & UI toggles]: 'language select' fails QA — 5/5 runs report broken workflow (00153-language-select-ui)

Description:
The Main menu > View > Language selector stores the chosen language but never applies it: selecting a non-English language (tested with Deutsch and Español) moves the checkmark and the preference persists across page reloads, yet every menu and panel label ("File", "Edit", "View", "PAGES", "LAYERS", "Design", "Styles", "Export", "Share", etc.) stays in English. The selector UI works; the translation/application layer behind it is a no-op, so the UI language cannot actually be switched.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Open the Main menu (logo icon, top-left) > View > Language. The submenu lists: English ✓, Deutsch, Español, Français, Italiano, Polski, Русский, 中文（简体）.
3. Click Deutsch (the first non-English option) — the checkmark moves from English to Deutsch.
4. Inspect the UI text in menus and panels.
5. Reload the page and inspect again.
6. Optionally select Español to rule out missing German translations.

Actual Result:
- The checkmark moves to the selected language and the selection persists across a page reload.
- The UI text does not change — all menus and panels stay in English ("File", "Edit", "View", "PAGES", "LAYERS", "Design", "Styles", "Export", "Share", etc.).
- The same happens with a second language (Español): the checkmark moves, but no UI text is translated.

Expected Result:
Selecting a language from Main menu > View > Language should translate the app's UI text (menus, panels, labels) into the chosen language, both immediately and after reload.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_1c713c36-6676-4d1b-a5f5-545426d4f63d.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_b18aa45c-3a68-409a-a634-8b6d6a692274.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_d575f0d6-4bb1-4c1a-8de9-79ad7c6d7d62.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_d61335e7-9789-4f01-b5f0-51f632156645.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_da0f22b9-c48c-4d9a-b851-58d6fdc7ce79.txt`

Agent report (verbatim tail of failing run):

```
The menu is closed and the app is back to its normal state. Here's a summary of what happened:

**What I did:**
1. Opened the Main menu (logo icon, top-left) → **View** → **Language**, which listed: English ✓, Deutsch, Español, Français, Italiano, Polski, Русский, 中文（简体）.
2. Clicked **Deutsch** (the first non-English option). The checkmark moved from English to Deutsch, confirming the selection was registered.
3. However, the UI text did **not** change — all menus and panels stayed in English ("File", "Edit", "View", "PAGES", "LAYERS", "Design", "Styles", "Export", "Share", etc.).
4. Reloaded the page: the Deutsch selection persisted (checkmark still on Deutsch), but the UI remained entirely English.
5. Tried a second language (**Español**) to rule out missing German translations — same result: the checkmark moved, but no UI text was translated.
6. Set the selection back to **Deutsch** (first non-English option) and verified the checkmark; the UI is still English.

**Result:** The Language menu works as a selector (the preference is stored and persists across reloads), but the app never actually applies the chosen language — the interface stays in English no matter which language is selected. The core goal of switching the UI language was therefore not achieved due to an app bug: language selection has no effect on the displayed UI text (tested with both Deutsch and Español, including a full page reload).

verdict: not-approve
```
