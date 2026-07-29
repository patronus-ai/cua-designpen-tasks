# mcp-harness/ — chained MCP workflows + quality-matrix rows

**12 tasks** (`70001`–`70012`). Each one is a chain: the output of one tool call is the input of the
next, so a field that is mislabeled, missing, stale or silently truncated breaks the chain visibly
instead of passing as it would in a single-tool test.

Separate from `in-scope/mcp-testing-harness/`, which tests tools one at a time. Numbered `70xxx` so
both can run in the same problem set.

## Shape of a task

- **Chain** — an ordered workflow over one entity or one failure class, written so no step may retype
  a value it could have read from the previous response.
- **Focus** — what to interrogate in that chain (round-trips, list-vs-detail, references, settling).
- **Per-step contract** — `EXPECT:` before every call, `ACTUAL:` + `OK`/`MISMATCH` after. Mismatches
  are recorded and the chain continues, so one early defect does not hide the rest of the surface.
- **Divergence blocks** — `MISMATCH #<n>` with Step / Call / Expected / Actual / **Class** /
  Severity. Class is a fixed vocabulary: `round-trip`, `list-vs-detail`, `broken-reference`,
  `stale-read`, `shape-drift`, `pagination`, `error-quality`, `context-size`, `missing-tool`.
- **Matrix block** — `MATRIX` lines, one per row the chain exercised, `PASS | FAIL | N/A` plus
  one-line evidence naming the call that proves it. `N/A` requires a reason; blank is not accepted.
- **Sentinel** — `mcp-harness-report: complete`, the single `answer` reward. The reward only checks a
  report arrived; findings are harvested from transcripts.

## Coverage

CRUD chains, one per entity, each closing the loop back to a list read:

| # | Entity | Chain ends by proving |
| --- | --- | --- |
| 70001 | node | delete removes it from every view, clone survives |
| 70002 | page | page-scoped reads are really scoped; deleted page leaves nothing orphaned |
| 70003 | component / instance | the master link is readable, re-pointable, never dangling |
| 70004 | paint style | edits propagate to consumers; detach clears only one link |
| 70005 | tree / grouping | three tree tools agree on membership and order |
| 70006 | text | content, units and per-range styling round-trip |
| 70007 | vector path | `path_get` → `path_set` identity write does not drift |

Failure-class passes:

| # | Class | Matrix rows |
| --- | --- | --- |
| 70008 | async settling / stale reads after layout writes | 9.x, 19.x |
| 70009 | response-shape consistency across 8 tools returning the same node | 9.x, 19.x |
| 70010 | pagination, silent truncation, oversized responses (200-node document) | 9.3, 13.1, 13.2 |
| 70011 | error quality: structured, self-correctable, no leaked internals | 2.3, 9.4, 13.3 |
| 70012 | interleaved read/write, selection across mutation, auth observation | 9.2, 13.x, 19.x |

`70009` is the shape-drift catcher: it observes one rectangle through `get_node`, `find_nodes`,
`query_nodes`, `node_children`, `node_tree`, `get_page_tree`, `get_selection` and `describe`, and
asks for a per-tool table of field names, types, id representation and optional-field presence.

`70010` separates the two size failures that usually get conflated — a response that returns fewer
entries than exist while claiming completeness, versus a response that is simply too large — and
requires the true count and how it was established.

## Auth, honestly

This deployment has no login, accounts or session tokens. Rather than invent a login to test,
`70012` asks the agent to observe and state whether any tool ever reported an auth or permission
error and whether UI and tool surface stayed in agreement about the same document, then mark the auth
rows `N/A` **with that evidence**. Every prompt's grounding block says the same, so no task reports
"no auth" as a defect.

## Grounding

Shared baseline in every prompt, to keep reports signal:

- `setup_problem` / `grade_problem` are harness plumbing, excluded from tool-surface coverage claims
- no persistence: a reload discards the document, so there is no persistence layer to test
- numeric values may read back rounded; a rounded echo is a correct round-trip
- a fill-less shape exports transparent; sections are created without a background fill

One grounded gap is deliberately targeted rather than assumed: the registry exposes
create/list/apply/update/detach for paint styles but **no delete**, so `70004` asks the agent to
establish whether a style can be removed at all and to log it as `missing-tool` with the consequence.

## MCP grounding

All 56 distinct tool names referenced across the bucket were checked against the app's registry
(`packages/core/src/tools/`) — no invented names. Browser tools are included so the agent can
screenshot the canvas: a pair of reads that agree with each other but disagree with the rendered
document is a finding these chains are meant to catch.

## Running them

Not part of `tasks.jsonl` yet — `tasks/` is untouched and the published problem set is unchanged. To
ship, copy the task directories into `tasks/` and regenerate `tasks.jsonl`, as was done for `mixed/`.
