# DesignPen [MCP tools]: 30016-set-text context flood — NOT an app bug (prompt fix)

No Linear issue — the failing runs drowned their own output.

Description:
Reward is marker-only (`adversarial-report: complete`). The prompt required a 5000-character set_text payload and a browser screenshot; both failing tails were nothing but a repeating '0123456789' flood with no final message or verdict.

Fix applied (definition.yaml + available_tools):
- Cap the oversized set_text stress string from 5000 to ~300 chars.
- Remove the browser-screenshot step and `browser_screenshot` from available_tools; verify via MCP read tools only.
- Add a budget-guard: stop testing and emit the report when low on turns.

Evidence: classification.json category `agent-flaky`; both failing tails = '0123456789' flood, no verdict.
