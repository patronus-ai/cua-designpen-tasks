# DesignPen v6 full-transcript scan playbook

Purpose: scan ALL attempts of assigned sampling jobs for designpen APP bugs
("something in the editor didn't work"), diff against the 16 known bug classes in
`bug-repros/README.md`, and report only NEW classes + strong evidence for known ones.
Results go to `task_data/cua-designpen-tasks/bug-repros/scan-results/<jobslug>.md`
(one file per job, create the dir if missing).

## Jobs (v6 cohort)

| job id | name | slug |
| --- | --- | --- |
| 27a14af4-21e5-4101-affe-c86f8a8486a2 | designpen v6 broking opus-5 10x | broking-opus |
| 088bacf2-bffe-491a-92bd-15185ef902c7 | designpen v6 broking fable-5 10x | broking-fable |
| 9628fa83-39ee-46f0-8622-3083505c78e2 | designpen v6 ptdev opus-5 10x | ptdev-opus |
| 604c7b2d-6483-47e5-8820-ea99ae50ed96 | designpen v6 ptdev fable-5 10x | ptdev-fable |
| 7cf836b0-933f-4953-a358-707e131a0f3e | designpen v6 ptweb opus-5 10x | ptweb-opus |
| d580a233-3755-4202-8809-1820938b9f28 | designpen v6 ptweb fable-5 10x | ptweb-fable |
| e9ee9a6e-021c-411e-9313-ef2b8032560d | designpen v6 mm opus-5 10x | mm-opus |
| 0d00efba-64f2-4010-b72a-8a4ffdf6b558 | designpen v6 mm fable-5 10x | mm-fable |

Already sampled earlier (2 attempts/problem, fable jobs only) — this pass covers the
REST: scan all `status == "completed"` rows; skip nothing else.

## Access recipe (Chrome MCP on taiga.ant.dev)

WebFetch is blocked by IAP — use claude-in-chrome `javascript_tool` on a
taiga.ant.dev tab (tabs_context_mcp → tabs_create_mcp → navigate to
`https://taiga.ant.dev/jobs/<your first job id>?environmentId=fcaf1b46-0e94-4c96-86c8-a23fba116644`).

- `/api/jobs/{jobId}/problems` → rows with `id` (row id), `problem_id`,
  `attempt_number`, `status`, `final_score`.
- `/api/transcript/{rowId}` → full transcript (raw ~5-40MB; strip base64 first).
- Build URLs with `new URL(path, location.origin)` — literal query strings in the JS
  code get blocked.
- The tool BLOCKS results containing `?`, `=`, `&`, "cookie", or 60+-char tokens.
  Scrub every output: `s.replace(/[=&?]/g,'~').replace(/co+ki/gi,'CK').replace(/[A-Za-z0-9+\/_-]{50,}/g,'[TOK]')`.
- Output truncates ~1.5k chars. For big payloads: stash in `window.__buf`, page out
  in 1400-char slices batched via `browser_batch` (10-16 javascript_tool actions per call).
- `javascript_tool` calls time out at 45s BUT the page keeps executing: launch the
  scan as a fire-and-forget async loop stored on `window`, then poll a counter.

## Scan harness (paste via javascript_tool, adjust JOB)

```js
window.__PAT = {
  p_focus: /no editable element is focused/i,
  p_internal: /Chrome DevTools error: Internal error/i,
  p_export: /(did not respond within \d+s|export_fig.{0,40}(fail|timed? ?out))/i,
  p_revert: /(revert(ed|s|ing)? (back )?to (the )?(component|master|default|original)|override(s)? (were|was|got|being)? ?(lost|dropped|reset|revert))/i,
  p_norepaint: /((does|did|do)( not|n't) (re)?paint|not repaint|still (shows?|renders?|displays?) (the )?(old|original|previous)|(color|fill|paint) (did not|didn't|never) (change|update))/i,
  p_staletext: /(stale (text )?(measurement|width|size)|clipped.{0,40}(until|after).{0,30}(toggle|retype|re-typ))/i,
  p_autoexpand: /(auto-?expand|grew (from \d+ )?to \d{3}|expanded (to|from) \d{3}|ballooned?)/i,
  p_neggap: /(negative (wrap )?gap|gap (of|to) -\d|itemSpacing[^\d-]{0,10}-\d)/i,
  p_invis: /(render(s|ed)? INVISIBLE|invisible (text|on canvas)|text.{0,25}invisible)/i,
  p_first: /(first (keystroke|character|digit).{0,30}(drop|miss|lost)|dropped the first)/i,
  p_specialchar: /(no US-keyboard key event|inserted directly — no key)/i,
  p_assets: /(assets panel.{0,80}(hang|hung|freeze|frozen|unresponsive)|(hang|froze|unresponsive).{0,60}assets panel)/i,
  p_bug: /(BUG|BROKEN|DEFECT|does ?n[o']t work|not working|glitch)/ig
};
window.__scan = []; window.__err = null;
window.__scanOne = async function(rowId, tag) {
  const t = await fetch(new URL('/api/transcript/' + rowId, location.origin)).then(r=>r.text());
  const clean = t.replace(/[A-Za-z0-9+\/]{120,}={0,2}/g,'');
  const res = {tag, hits: {}, ex: []};
  for (const [k, re] of Object.entries(window.__PAT)) {
    const g = new RegExp(re.source, 'gi'); let m, c = 0;
    while ((m = g.exec(clean)) && c < 500) { c++;
      if (res.ex.filter(e=>e.k===k).length < 3) {
        res.ex.push({k, t: clean.slice(Math.max(0,m.index-100), m.index+160).replace(/\s+/g,' ')});
      }
    }
    if (c) res.hits[k] = c;
  }
  window.__scan.push(res);
};
// load rows, filter completed, launch:
const JOB = '<job-id>';
const rows = await fetch(new URL('/api/jobs/' + JOB + '/problems', location.origin)).then(r=>r.json());
window.__todo = rows.filter(r => r.status === 'completed').map(r => ({id: r.id, tag: r.problem_id.replace(/-final$/,'') + '#' + r.attempt_number}));
(async () => { for (const s of window.__todo) { try { await window.__scanOne(s.id, s.tag); } catch(e){ window.__err = String(e).slice(0,80); } } })();
```

Poll with `'done~' + window.__scan.length + '/' + window.__todo.length + ' err~' + window.__err`
every few minutes (~6 transcripts/min). While polling you can already aggregate.

`p_bug` is the catch-all for NEW classes: after the run, pull its excerpts
(scrubbed, paged), read them, and classify anything that is an APP failure but does
not fit a known class. Ignore boilerplate matches (tool docs, task prompt text,
grader text) — judge by the excerpt.

## Known classes (do NOT report as new — evidence counts only)

1 color-style-binding-no-repaint · 2 instance-override-revert · 3 component
text-property dropped (dangling definitions) · 4 stale-text-measurement ·
5 fixed-frame-auto-expand · 6 fill-container-stale-width · 7 negative-wrap-gap
(Shift+A / itemSpacing −28) · 8 special-character-input (£/–/· no key event) ·
9 numeric first-keystroke drop (120→20) · 10 assets-panel hang · 11 assets drag
misparent · 12 text invisible after duplicate/move · 13 layer reorder tree≠visual ·
14 text style renders invisible · 15 canvas focus loss ("no editable element is
focused") · 16 export_fig timeout / export flip-flop.

NOT app bugs (skip): 413/32MB deaths, wall-clock kills, rubric/grader design,
overloaded_error, click-coordinate 0.8× scaling, open ports, seed CONTENT defects
(typos, missing assets, unwired seed props — note them only if new instance found).

## QA-job cross-check (mandatory per session)

Each opus job has an env_linter QA report. Fetch it via `/api/qa-jobs/{qaId}` (same
tab; response has `items[]` with `title`, `description`, `metadata`,
`problem_run_ids`, and `arguments.job_id` = the sampling job):

| qa job id | covers sampling job |
| --- | --- |
| 75101cdd-22fe-4b49-82a1-5d62db4658a0 | 27a14af4 broking-opus |
| 7c9b594b-15a6-49a5-9928-102bae4e66b4 | 9628fa83 ptdev-opus |
| 259c0fcc-9e60-43ab-9f3b-2f7a5e65a3ac | 7cf836b0 ptweb-opus |
| 81710459-d4a1-4fb2-ba63-09ebc7af79d5 | e9ee9a6e mm-opus |

Read ALL items (titles + full descriptions — remember the output scrubber and the
1.4k paging), then in your report add a section `## QA cross-check`:
- every app-bug claim from the QA items with the transcript evidence your scan found
  (confirms / not seen in scan / contradicts);
- any app-bug detail in QA descriptions your regexes missed → treat as NEW-candidate
  input (cite the QA item);
- run IDs the QA report names (`problem_run_ids`, ids inside descriptions) — if any
  of them is in your job, pull that transcript's hits explicitly.

## Seed rule for any NEW bug-repro tasks (merge session)

Every new task (017+) MUST set `bootstrap_data.seed` to the production seed of the
job family the bug was evidenced in: `broking-v4`, `ptdev-v4`, `ptweb-v4` or `mm-v4`
(mapping and wiring in `bug-repros/seeds/README.md`). Do not use
`patronus_design_system_and_logo`. Write prompts seed-agnostically (say "a library
component with a text label", not a component name from another seed), and where the
seed has KNOWN content defects (unwired component properties), tell the agent not to
report those as new bugs.

## Report format (`scan-results/<jobslug>.md`)

```
# <job name> — full scan <date>
rows scanned: N/M (completed/all)
## Known-class hit table
| class | transcripts w/ hits | total hits | strongest excerpt (scrubbed, ≤200ch) |
## NEW candidate classes
For each: name, what breaks, 2-3 excerpts w/ problem_id#attempt, why it's app not harness/agent.
## QA cross-check
(only in the opus-job report of the session; see playbook section above)
## Verdict
NEW classes found: yes/no; list.
```
