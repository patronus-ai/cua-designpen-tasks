# DesignPen [MCP tools]: 30001-create-shape context flood — NOT an app bug (prompt fix)

No Linear issue — MCP works (4/5 passed); the lone failure drowned its own context.

Description:
Reward is marker-only (`adversarial-report: complete`). The prompt required a browser screenshot and a 5000-character name; the failing run's tail was pure screenshot/base64 with no verdict — the run flooded its context and never emitted the marker.

Fix applied (definition.yaml + available_tools):
- Remove the browser-screenshot step; verify via MCP read tools only.
- Remove `browser_screenshot` from available_tools (hard-prevents the flood vector).
- Cap the oversized-name stress input from 5000 to ~300 chars.
- Add a budget-guard: stop testing and emit the report when low on turns.

Evidence: classification.json category `agent-flaky`; failing tail = screenshot/base64, no verdict.
