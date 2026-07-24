# DesignPen [MCP tools]: 'set font range' fails QA — 5/5 runs report broken workflow (10100-set-font-range-mcp)

Description:
The `set_font_range` MCP tool in the DesignPen/OpenPencil design app returns success but its `size` parameter never surfaces in any readable node property. After setting a text layer's content to 'Hello world' and calling `set_font_range` on characters 0-5 with size 30 (tool returns `{"id":"0:3","range":{"start":0,"end":5}}`), `get_node` still reports `fontSize: 14` with no mixed-style or range-override indicator. A control test applying `set_font_range` to the entire range (0-11) on a scratch node showed the same thing — `fontSize` stays 14 — so either the write silently fails to persist or the read API doesn't expose range styling at all. Additionally there is no MCP delete tool, so diagnostic nodes cannot be cleaned up.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Using MCP tools, create a text layer named "Greeting".
3. Call `set_text` to set its content to 'Hello world'.
4. Call `set_font_range` on characters 0-5 with size 30 — it returns success.
5. Call `viewport_zoom_to_fit`.
6. Call `get_node` on the text layer and inspect `fontSize`.
7. Control test: create another text node, set the same text, and call `set_font_range` on the entire range (0-11) with size 30, then `get_node` it again.

Actual Result:

- `set_font_range` returns success: `{"id":"0:3","range":{"start":0,"end":5}}`.
- `get_node` still reports `fontSize: 14` with no mixed-style or range-override indicator — the size-30 change is not observable in read-back.
- The full-range (0-11) control test on a scratch node also still reports `fontSize: 14`, so the `size` parameter never surfaces in any readable property.
- Side effect: the diagnostic scratch node remains on canvas because no delete tool is available in the MCP set.

Expected Result:
After a successful `set_font_range` with size 30, the styling should persist and be observable via `get_node` — either as an updated/mixed `fontSize` or an explicit range-style indicator — so the change can be verified with the available MCP read tools.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed (agent verdict: not-approve)
- Attempt transcripts:
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_3f9f0166-908c-4f6e-8a10-c9023edec9ec.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_4542efe7-4f08-4caa-92bb-f36f9af9dbd4.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_5ef9a0cc-b4b6-4a73-af46-f37c2cc452c4.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_cda36303-5eeb-491b-b37b-5ef98db832b0.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_ec2ad432-ba0e-42d8-8de6-7df8c4403e4a.txt`

Agent report (verbatim tail of failing run):

```
All steps are complete. Here is my report:

## What I did
1. **Created** a TEXT layer named **"Greeting"** (id `0:3`) at (100, 100), 300×60.
2. **set_text** → content set to `"Hello world"`.
3. **set_font_range** on characters **0–5** with **size 30** → tool returned success: `{"id":"0:3","range":{"start":0,"end":5}}`.
4. **viewport_zoom_to_fit** on the node → viewport centered at (250, 130) on bounds 300×60.

## Verification results
- `find_nodes(name="Greeting", type=TEXT)` → exactly **1 match**, id `0:3` ✅
- `get_node("0:3")` → `name: "Greeting"`, `type: TEXT`, `characters: "Hello world"` ✅
- **However**: `get_node` reports `fontSize: 14` with no mixed-style or range-override indicator, so the size-30 change on "Hello" is **not observable** in the read-back.
- **Control test**: I created a scratch node "FontTest" (`0:4`), set the same text, and applied `set_font_range` to the *entire* range (0–11) with size 30. `get_node` *still* reported `fontSize: 14`. This shows the `size` parameter of `set_font_range` never surfaces in any readable property — either the write silently fails to persist, or the read API doesn't expose range styling at all. Either way, the requested styling **cannot be confirmed** with the available MCP tools.
- Side effect: the diagnostic "FontTest" node remains on canvas, as no delete tool is available.

## Summary
The layer creation, text content, and zoom all worked and verified correctly. But the core `set_font_range` requirement could not be verified: despite two successful-looking responses, the node still reads `fontSize: 14`, and a full-range control test proved the size change never appears in read-back — indicating a silent failure or a reporting gap in the tooling.

The font-size change on characters 0–5 could not be confirmed; `get_node` contradicts the expected result even after a successful `set_font_range` response, and a full-range control test showed the same inconsistency.

verdict: not-approve
```
