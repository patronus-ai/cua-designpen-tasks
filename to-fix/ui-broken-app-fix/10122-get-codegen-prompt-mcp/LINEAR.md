# DesignPen [MCP set_text]: 'set_text long-content write' fails QA — 1/5 runs report broken workflow (10122-get-codegen-prompt-mcp)

Description:
The MCP `set_text` tool has a non-deterministic write/data-integrity bug on long content. While setting a text layer's content to the full text returned by `get_codegen_prompt`, the first `set_text` call stored a corrupted line: in the Text section, `` `textDecoration` → `text-transform` `` was stored (duplicating the `textCase` mapping) instead of the source's `` `textDecoration` → `text-decoration` ``. Re-issuing `set_text` with the byte-identical input stored the line correctly, proving the corruption is in the write path, not the input. A minor secondary issue: the text node drops a trailing newline from the submitted string. Also noted: the toolset offers no `get_text`/read-back tool, so content verification had to rely on the `set_text` return echo.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport) so the OpenPencil SPA is live and connected to the MCP server.
2. Via MCP, call `get_codegen_prompt` and keep the full returned text.
3. Create a text layer named Guidelines (`create_shape` type TEXT).
4. Call `set_text` on the layer with the full codegen prompt text.
5. Compare the stored/echoed content line by line against the source text, particularly the `textDecoration` mapping line in the Text section.

Actual Result:

- On the first `set_text` call, the stored content did not match the submitted text: the `textDecoration` line came back as `text-transform` (a duplicate of the `textCase` mapping) instead of `text-decoration`.
- A second `set_text` call with the identical input stored the line correctly — the same input produced two different results.
- The trailing newline of the source string was silently dropped.

Expected Result:
`set_text` should deterministically store exactly the submitted string; identical inputs must always produce identical stored content, with no corrupted or substituted lines.

Estimate: M (3 points) — intermittent corruption in the text write/serialization path; needs reproduction on long multi-line payloads and a regression test

Evidence:

- QA job `db76a8af-97c9-41fb-bbba-42d2d887d5b8`, model `claude-opus-4-8` — 1 of 5 runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_3b0daf2b-6953-4fbc-8abe-bb29db62a189.txt`

Agent report (verbatim tail of failing run):

```
...faithful. ✅ (Note: no `get_text`/`describe` read-back tool is available in this toolset, so content verification relied on the `set_text` return echo.)

## The problem I hit

On the **first `set_text` call**, the stored/returned content did **not match** the text I submitted. In the final **Text** section the line came back as:

- `` `textDecoration` → `text-transform` `` ❌ (corrupted — duplicated the `textCase` mapping)

instead of the source's:

- `` `textDecoration` → `text-decoration` `` ✅

I caught this in verification and re-issued `set_text` with the **identical** input; the second attempt stored the line correctly. The same input producing two different results points to a flaky write/data-integrity bug in `set_text` rather than the input itself. The final state is now correct.

Minor, non-blocking: the original prompt string ends with a trailing newline that the text node dropped — negligible whitespace, not meaningful content, so I left the (otherwise faithful) final content as-is rather than risk re-triggering the flaky write.

The end result is correct and verified, but the process did not go cleanly — the first write corrupted a line and required a corrective redo.

verdict: not-approve
```
