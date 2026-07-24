# pid 30016 — 5000-char set_text payload + screenshot drown the context

## Root cause
Marker-only reward; the 5000-char stress string plus screenshots flood the context so the agent never emits `adversarial-report: complete`. App + tools fine.

## Fix (prompt + tools)
- Cap stress string to ~300 chars.
- Drop screenshots and remove `browser_screenshot` from available_tools.
- Budget-guard to guarantee the marker.

## Disposition
PROMPT FIX applied. Retest on Taiga.
