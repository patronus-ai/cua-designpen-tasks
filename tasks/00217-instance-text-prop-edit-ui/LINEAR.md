# DesignPen [UI]: 00217-instance-text-prop false not-approve over UX friction — NOT an app bug (prompt fix)

No Linear issue — the deliverable completes (4/5 passed); the lone failure was a verdict-criteria issue, not a broken feature.

Description:
The agent completed the deliverable (instance text property changed to "Buy now") but voted not-approve over UX friction (confusing Add-vs-Create property, inability to delete a property). The prompt's verdict rubric ("if you hit any problems, bugs, or blockers") invited penalizing UX opinion.

Fix applied (definition.yaml):
- Verdict rubric now keys ONLY on reaching the end state ("Buy now" on the instance). UX friction/naming quirks/extra clicks are explicitly not blockers; not-approve reserved for a crash or genuinely broken/missing feature.

Evidence: classification.json category `agent-flaky`; 4/5 passed, 1 UX-friction false-negative.
