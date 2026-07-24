# pid 00217 — verdict penalized UX friction on a completed deliverable

## Root cause
Deliverable achievable and achieved; the open-ended "any problems/bugs/blockers → not-approve" rubric let the agent downvote on subjective UX friction. App works.

## Fix (prompt)
Completion-focused rubric: approve iff the instance text property reads "Buy now"; friction is explicitly not a blocker; not-approve only for crash/broken-feature.

## Disposition
PROMPT FIX applied. Retest on Taiga.
