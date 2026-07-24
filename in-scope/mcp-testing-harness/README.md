# MCP testing-harness task set — cua_designpen (in scope only)

**24 tasks** (`40001`–`40024`), harness format `<number>-<slug>-mcp/definition.yaml`.
Numbering disjoint from the other sets: workflow UI `00001`–`00464`, workflow MCP
`10001`–`10125`, adversarial UI `20001`–`20040`, adversarial MCP `30001`–`30025`.

## What these are

End-to-end workflows that **chain MCP tools** — the output of one call feeds the input of the
next — with expected-vs-actual checked at every step. This is where data-modeling problems
surface: fields that don't round-trip, list vs detail disagreements, broken references, stale
reads after writes, silent truncation. Regenerate with `python3 generate.py` (edits go in the
`TASKS` table there).

## Scope

Only in-scope features per `Patronus_QA_Report_EXTERNAL_updated - Figma.csv`. Excluded tools
(dedicated Variables engine is an intentional stub; tokens go through Styles): `bind_variable`,
`unbind_variable`, `create_variable`, `delete_variable`, `set_variable`, `get_variable`,
`find_variables`, `list_variables`, `create_collection`, `delete_collection`, `get_collection`,
`list_collections`, `node_bindings`, `design_to_tokens`.

**Coverage: 111/111 remaining catalog tools**, each in at least one chain.

## Task map

| Task | Chain |
|------|-------|
| 40001 | shape CRUD round-trip (create → find → get → update → rename → delete) |
| 40002 | group / tree / ancestors / clone / reparent / ungroup |
| 40003 | page lifecycle (create, switch, reorder, scoping, delete) |
| 40004 | component → instance → override → orphaned instance |
| 40005 | paint styles (create, apply, update-propagation, detach) |
| 40006 | text + fonts (list consistency, set_font, ranges, resize) |
| 40007 | vector paths (get/set round-trip, move/scale/flip math, width profile) |
| 40008 | all four booleans + flatten, bounds sanity |
| 40009 | geometry readers agree (bounds vs get_node, rotation, min/max clamps) |
| 40010 | appearance round-trip after every write (fill/stroke/opacity/blend/radius/effects) |
| 40011 | auto-layout math + arrange/distribute/tidy |
| 40012 | stock photo → image fill → adjustments → export→import round-trip |
| 40013 | icons (search → fetch → insert consistency) |
| 40014 | export_svg → import_svg round-trip; export_fig / export_pdf probe |
| 40015 | selection + viewport round-trips |
| 40016 | analyze_* vs a ground-truth scene |
| 40017 | response-shape consistency across all read tools |
| 40018 | codegen/diff (get_jsx, render, replace_with, diff_*, component map) |
| 40019 | batch atomicity + mixed read/write freshness + calc |
| 40020 | error-surface audit (not-found consistency, types, no-results vs error, leaks) |
| 40021 | large responses + truncation honesty (60 nodes; eval env-gated) |
| 40022 | server file round-trip (new/save/open; path traversal; OPENPENCIL_MCP_ROOT-gated) |
| 40023 | text-on-path attach/options/detach |
| 40024 | visibility, lock enforcement, slice, section status |

## Reporting contract (baked into every prompt)

Per finding:

```
MISMATCH #<n>
Step: <exact tool call with args>
Expected: <what and why>
Actual: <what came back>
Severity: <critical | major | minor | cosmetic>
```

No findings → agent states exactly `NO MISMATCHES FOUND`. Every final message ends with exactly
`mcp-harness-report: complete` (the harvest sentinel).

## Rewards

ONE `answer` reward per task: `STRING_CONTAINS` → `mcp-harness-report: complete`. Mismatches are
the desired output, not failures — no `verdict: approve` reward on purpose.

## Env gates

`eval` → `OPENPENCIL_MCP_EVAL=1` (40021 has a batch_update fallback). `new_document` /
`open_file` / `save_file` → `OPENPENCIL_MCP_ROOT` (40022 treats a structured "disabled" error
as a pass-through result, not a blocker).
