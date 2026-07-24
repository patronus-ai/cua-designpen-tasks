# DesignPen [view & UI toggles]: 'theme select' fails QA — 3/5 runs report broken workflow (00158-theme-select-ui)

Description:
Switching the editor to Dark via Main menu > View > Theme > Dark works and persists, but the Dark appearance is applied incompletely: the floating bottom toolbar (move/frame/shape/pen/text/comment tools plus the right-hand tool group) does not adopt the dark theme. It stays white with dark icons — pixel-identical to its Light-mode styling — even after a full page reload, while the left sidebar (Pages/Layers), icon rail, top bar, and right Design panel all re-theme correctly. This is a partial theming bug, not a broken selector.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Open the Main menu (logo button, top-left) > View > Theme.
3. Select Dark (initially set to "Auto"); verify the checkmark moves to "Dark".
4. Inspect the floating bottom toolbar and compare it with the rest of the editor chrome.
5. Reload the page and inspect the bottom toolbar again.

Actual Result:
- The theme setting changes to "Dark" and persists across reloads; the left sidebar (Pages/Layers), icon rail, top bar, and right Design panel all render with dark backgrounds.
- The floating bottom toolbar (move/frame/shape/pen/text/comment tools plus the right-hand tool group) does not adopt the dark appearance — it stays white with dark icons in Dark mode, pixel-identical to its Light-mode styling, even after a full page reload.

Expected Result:
Selecting the Dark theme should re-theme all editor chrome, including the floating bottom toolbar, so the entire UI renders with the dark appearance.

Estimate: M (3 points) — scoped feature fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 3 of 5 runs failed (2 approved)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_085d7032-de14-4786-8dc0-62de618618bb.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_288aef23-33db-4868-a06e-4ca2532a16dc.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_42f66b73-0592-4c96-bc05-7d8cfe7e472f.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_7ebdcc34-03e2-4c45-a550-4ef5c576f7aa.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_969f1bc6-8238-4e62-8919-4e2579855116.txt`

Agent report (verbatim tail of failing run):

```
I completed the requested steps and verified the results. Here's a summary:

**What I did:**
1. Opened the Main menu (logo button, top-left) → **View** → **Theme**
2. Selected **Dark** (previously set to "Auto")
3. Verified the checkmark moved to "Dark" in the Theme submenu
4. Reloaded the page to confirm the setting persists (it does)
5. Cross-checked by toggling Light and back to Dark to isolate an inconsistency I noticed

**Result:** The theme setting is now "Dark" and most of the editor chrome switched correctly — the left sidebar (Pages/Layers), icon rail, top bar, and right Design panel all render with dark backgrounds, and the setting persists across reloads.

**Issue found:** The floating bottom toolbar (move/frame/shape/pen/text/comment tools plus the right-hand tool group) does **not** adopt the dark appearance. It stays white with dark icons in Dark mode — pixel-identical to its Light-mode styling — even after a full page reload. Every other UI surface re-themes correctly, so the editor's Dark appearance is only partially applied, which looks like a theming bug in the app rather than a design choice.

The menu navigation and theme selection themselves worked without blockers, but because the Dark appearance is incompletely applied (bottom toolbar remains light-themed), I can't call this fully successful.

verdict: not-approve
```
