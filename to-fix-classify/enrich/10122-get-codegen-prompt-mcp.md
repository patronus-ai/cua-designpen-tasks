# pid 10122 — `set_text` "non-deterministic" line corruption on long multi-line content

## Root cause analysis

**No defect was found in the app's `set_text` write, transport, or read-back path — every stage is a single synchronous, lossless string hand-off.** After tracing the full pipeline, the evidence points away from the application and toward the *client composing the `set_text` argument* (the agent re-transcribing content). Findings, with the pipeline stages exonerated one by one:

1. **Write path is one synchronous assignment.** `set_text` (`packages/core/src/tools/modify/text.ts:15-20`) does `node.characters = text`; the proxy setter (`packages/core/src/figma-api/proxy.ts:208-210`) is `this[INTERNAL_GRAPH].updateNode(this[INTERNAL_ID], { text: v })`; `SceneGraph.updateNode` (`packages/core/src/scene-graph/index.ts:787-873`) ends in `Object.assign(node, changes)`. No chunking, no per-line diffing, no async step anywhere — a whole-string replace cannot duplicate one line while preserving the rest.
2. **Transport is a single JSON frame.** The MCP server forwards each tool call as one `ws.send(JSON.stringify({type:'request', id, ...body}))` (`packages/mcp/src/browser-rpc.ts:112`) and the bridge executes it in one `def.execute(figma, toolArgs)` (`src/app/automation/bridge/tool-handlers.ts:45`). JSON string encoding is lossless for `\n`, including trailing newlines. No `.trim()`/`trimEnd` exists in the schema layer (`packages/mcp/src/tool/schema.ts` uses plain `z.string()`), the tool layer, or the text modules (repo-wide grep for `trimEnd`/trailing-newline stripping in `packages/core/src` found nothing in this path).
3. **Read-back is verbatim.** `get_node` serialization emits `obj.characters = n.text` untouched (`packages/core/src/figma-api/serialization.ts:89`).
4. **The corrupted line pair is verbatim from `get_codegen_prompt`'s static payload.** The reported corruption — a line reading `` `textDecoration` → `text-transform` `` instead of `` `textDecoration` → `text-decoration` `` — is exactly the *adjacent* final two lines of the codegen prompt, `packages/core/src/tools/prompts/codegen.md:245-246`:
   ```
   - `textDecoration` → `text-decoration`
   - `textCase` → `text-transform`
   ```
   Both the source file and the built artifact (`packages/core/dist/tools/prompts/codegen.js`) are **correct**; `get_codegen_prompt` returns the constant unchanged (`packages/mcp/src/tool/registration.ts:196-204`, `async () => ok({ prompt: CODEGEN_PROMPT })`).

**Top hypothesis (ranked):**

1. **Client-side transcription error (most likely).** The reproduction flow was `get_codegen_prompt` → agent copies the prompt into `set_text`. An LLM re-typing ~250 lines occasionally fuses the two adjacent arrow-mapping lines (a classic pattern-completion slip on near-duplicate lines) and drops the file's trailing newline. This fully explains all three observed properties: non-determinism, correct storage on identical re-submit (the re-submit payload was itself correct), and the corruption being a duplicate of the *neighboring* line. The app stores exactly what it was sent.
2. **MCP client/harness JSON handling (unlikely).** A client that re-encodes arguments could in principle mangle content, but standard JSON codecs cannot selectively duplicate one interior line, and the trailing-newline drop would then be deterministic — contradicting "identical re-submit stores correctly".
3. **App-side race (no supporting evidence).** No async or line-oriented code exists between argument receipt and `node.text` assignment; ruled out by inspection (points 1-3 above).

Honest caveat: without the pid-10122 raw transcript (exact `set_text` argument bytes vs. stored bytes) hypothesis 1 cannot be proven from source alone; it is inferred from the exhaustive absence of any line-oriented or lossy code in the pipeline plus the exact-match to codegen.md:245-246.

## Proposed fix

The app needs no data-path change; the fix is verifiability and misuse-resistance:

1. **Echo a content digest instead of the raw text** from `set_text` (`packages/core/src/tools/modify/text.ts:19`): return `{ id, length: text.length, lines: <count>, sha256: <hex> }` (or at minimum `length`). Today it echoes the submitted `text` back, which cannot reveal client-side transcription because it round-trips the same wrong payload. A digest lets the agent compare against the intended source cheaply.
2. **Document verbatim-copy guidance** in the `set_text` description (`text.ts:11-14`): recommend reading back via `get_node` and comparing `characters` when setting long content.
3. Optionally add a `get_text` convenience (or document `get_node` → `characters`) so harnesses assert stored bytes, not tool echoes.

If the harness team wants a hard guarantee against trailing-newline ambiguity, additionally assert in a regression test that `set_text` preserves trailing `\n` end-to-end (test below pins that contract so any future "normalization" regression is caught).

## Acceptance criteria

- `set_text` with the full 246-line `CODEGEN_PROMPT` content (including its trailing newline) stores byte-identical text: `get_node(id).characters === submitted text`, including the final `\n`.
- 20 consecutive `set_text` calls with the same long multi-line payload each read back byte-identical (no non-determinism in-app).
- `set_text`'s response includes a `length` (and/or hash) field equal to the submitted string's length, allowing clients to detect their own transcription drift without re-fetching.
- `get_codegen_prompt` returns a prompt whose last two lines are exactly `` - `textDecoration` → `text-decoration` `` and `` - `textCase` → `text-transform` `` (guards the static asset against future accidental edits).

## Regression tests to add

Unit — `packages/core/src/tools/modify/` (new `text.test.ts` cases):

1. **Multi-line fidelity**: create a TEXT node; `setText.execute(figma, { id, text: sample })` where `sample` is 200+ lines containing adjacent near-duplicate lines (use the real `CODEGEN_PROMPT` constant); assert `figma.graph.getNode(id).text === sample` (strict equality, byte-for-byte).
2. **Trailing newline preserved**: `setText` with `"line1\nline2\n"`; assert stored text ends with `"\n"` and `text.length === 12`.
3. **Idempotent repeat**: loop 20× `setText` with the same payload; after each, assert strict equality with the input (catches any future async/derived-state race).
4. **Response contract**: assert the result object reports `length === payload.length` (once fix 1 lands).

Unit — prompt asset guard (`packages/core/src/tools/` or `tests/unit`):

5. Import `CODEGEN_PROMPT`; assert it contains the exact substring `` "`textDecoration` → `text-decoration`" `` and that `` "`textDecoration` → `text-transform`" `` does **not** occur.

Integration — `tests/integration/mcp`:

6. Over the real MCP bridge: `get_codegen_prompt` → take `prompt` verbatim → `create_shape TEXT` → `set_text` with the prompt → `get_node`; assert `characters` is strictly equal to the `prompt` string received (including trailing newline). This pins the *entire* transport + write + read path and isolates any future corruption to the client.
