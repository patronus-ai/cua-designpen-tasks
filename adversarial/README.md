# adversarial/ — hostile-brief QA tasks

**20 tasks**: 10 UI (`60001`–`60010`) + 10 MCP (`60011`–`60020`). Each one wraps a realistic
workflow in an adversarial brief: the executing agent must complete the workflow *and* actively try
to break the app along the way, then report every defect it found inside the session.

Not to be confused with `in-scope/adversarial/` (`20xxx`/`30xxx`), which is the filtered copy of the
app repo's generated set. This bucket is authored separately and numbered `60xxx` so the two can be
run together without collisions.

## Shape of a task

Three parts, always in this order:

1. **Workflow** — an ordinary task the agent must finish, so there is a known end state to check
   against and the session has a purpose beyond fuzzing.
2. **Adversarial brief** — the attack angles for that workflow, with concrete payloads and the
   recovery instruction ("undo so the document ends in the state the workflow describes"), so a
   hostile probe does not silently become the deliverable.
3. **Reporting contract** — a fixed `DEFECT #<n>` block (Steps / Observed / Expected / Severity),
   the explicit `NO DEFECTS FOUND` line when nothing turned up, and the sentinel
   `adversarial-report: complete` as the single `answer` reward.

The reward only checks that a report was delivered. Findings are harvested from the transcripts
afterwards — the score is not a pass/fail judgement on the app.

## Attack angles, and where they live

| Angle | UI | MCP |
| --- | --- | --- |
| Empty / oversized / malformed form input | 60001, 60005 | 60011, 60017 |
| Boundary and extreme numeric values | 60001, 60002 | 60011, 60018, 60020 |
| Wrong types, nonexistent ids | — | 60011, 60015, 60019, 60020 |
| Injection-shaped payloads | 60005 | 60012, 60016, 60017 |
| Deleting records other records reference | 60002, 60003, 60004, 60006, 60009 | 60020 |
| Editing from a stale view | 60002, 60004, 60007, 60009 | 60013 |
| Navigating away mid-operation, back button | 60006, 60007 | — |
| Cancelling mid-flow | 60007, 60010 | — |
| Same action twice, quickly | 60001, 60003, 60006, 60008 | 60011 |
| Cycles / self-reference | 60003 | 60014, 60015 |
| Atomicity of a compound operation | 60008 | 60013 |
| Response-shape correctness | — | 60016, 60019 |

## Grounding — false positives the prompts pre-empt

Every prompt carries the same baseline block naming behaviours that look like bugs but are intended
here, so reports stay signal:

- no persistence: reloading or navigating away discards the unsaved local document
- layout guide bands hidden until View > "Layout guides" (Shift+G)
- a fill-less shape exports transparent; sections are created without a background fill
- numeric readouts round; a rounded echo of what you typed is correct
- native dropdown popups can drop a synthetic option click — a driver artifact, not a defect

Two prompts additionally bless behaviour that earlier QA rounds mis-filed: `60010` states that a pen
click on a two-segment vertex removes it by design (so only a toolbar/behaviour mismatch counts), and
`60009` asks about leaving Dev Mode by keyboard rather than asserting the `</>` segment is a toggle.

## MCP grounding

Every tool named in an MCP task's `available_tools` was checked against the app's tool registry
(`packages/core/src/tools/`) — 45 distinct tools, no invented names. `available_tools` also carries
the browser tools, so the agent can screenshot the canvas to confirm that what a tool *reported* and
what the document *shows* agree; that disagreement is one of the defect classes the contract asks
for.

## Running them

These are not part of `tasks.jsonl` yet — `tasks/` is untouched, so the published problem set is
unchanged. To ship them, copy the task directories into `tasks/` and regenerate `tasks.jsonl` the
same way the `mixed/` bucket was added.
