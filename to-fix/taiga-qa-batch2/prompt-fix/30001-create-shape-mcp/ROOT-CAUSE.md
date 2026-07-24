# pid 30001 — screenshot/base64 + 5000-char payload flood the context

## Root cause
Marker-only reward; the prompt's own instructions (browser screenshot + 5000-char name) flood the transcript so the agent never reaches `adversarial-report: complete`. App + tools fine (4/5 passed).

## Fix (prompt + tools)
- Drop browser screenshots (MCP task) and remove `browser_screenshot` from available_tools.
- Cap oversized-name stress input to ~300 chars.
- Budget-guard so the marker is always emitted before turn exhaustion.

## Disposition
PROMPT FIX applied. Retest on Taiga.
