# DesignPen [AI panel]: 'ai stop generation' fails QA — 4/4 runs report broken workflow (00463-ai-stop-generation-ui)

Description:
The stop-generation control in the DesignPen/OpenPencil AI chat panel cannot be exercised because AI generation never starts. The panel opens (Ctrl+J worked; Cmd+J did nothing in this environment) and provider connection/key-saving succeeds for OpenRouter, Anthropic, OpenAI, Google AI, and OpenAI-compatible providers, but every send of a large job (e.g. "Create a fifty-frame wireframe set for a mobile app") fails instantly with a generic red toast "An error occurred." The assistant never starts streaming, never creates a frame, and the send button never changes into a stop button — so there is nothing to interrupt. The agent diagnosed the root cause: the sandbox has no outbound network (DNS fails for api.anthropic.com, api.openai.com, openrouter.ai, generativelanguage.googleapis.com) and no mock AI backend exists on the app origin or localhost.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Open the AI chat panel via Ctrl+J or the "AI" tab in the right panel header (Cmd+J did nothing in this environment).
3. Connect an AI provider (e.g. OpenRouter or Anthropic) with an API key — key-saving succeeds.
4. Type the large job "Create a fifty-frame wireframe set for a mobile app" into the chat input and send it.
5. Watch the chat panel for streaming output and for the send button to turn into a stop button.

Actual Result:

- Every send fails instantly with a generic red toast "An error occurred."
- The assistant never starts streaming, never creates a single frame, and the send button never changes into a stop button — the stop-during-streaming behavior cannot be exercised at all.
- Diagnosis: the sandbox has no outbound network — `api.anthropic.com`, `api.openai.com`, `openrouter.ai`, `generativelanguage.googleapis.com` all fail DNS resolution (`DNS_PROBE_FINISHED_NO_INTERNET`); no mock AI backend was found (same-origin `/v1` / `/api/v1`, `mockServiceWorker.js`, `.web` hosts, localhost ports like 11434 all probed).
- The error toast's copy button could not be used to read details (clipboard paste does not work in the headless browser).
- Also: Cmd+J did not open the panel; only Ctrl+J worked.

Expected Result:
Sending a large job should start a streaming AI generation that creates frames, with the send button replaced by a stop button; clicking stop mid-stream should cut the generation off early.

Estimate: M (3 points) — scoped feature fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 4 of 4 completed runs failed (agent verdict: not-approve)
- Attempt transcripts:
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_74831cc3-e550-422d-86f9-9417fd6703a5.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_7a8ab671-f6c5-496d-b7a9-38be65450b61.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_c03cd2c1-3bdc-4ac6-b2e9-fb2c36f99789.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_c3f85186-c122-4c7f-bf2e-574b6fe92a85.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_cfa478eb-eec1-4ef6-92d3-67ca7f213c96.txt`

Agent report (verbatim tail of failing run):

```
## Summary of what happened

**What I did:**
1. **Opened the AI chat panel** — Cmd+J did nothing in this environment, but **Ctrl+J opened the AI tab** in the right panel successfully (the AI tab button is also visible in the panel header).
2. The panel required connecting an AI provider. I connected several providers with test API keys (connection/key-saving itself succeeded each time): **OpenRouter, Anthropic (Claude Sonnet 4.6), OpenAI (GPT-5.3 Codex), Google AI (Gemini 3.1 Pro), and OpenAI-compatible** with custom base URLs.
3. **Sent the large job** "Create a fifty-frame wireframe set for a mobile app" repeatedly (visible as user bubbles in the chat).

**The blocker:** Every single send failed **instantly** with a generic red toast **"An error occurred."** The assistant never started streaming, never created a single frame, and the send button never changed into a stop button — so there was nothing to interrupt and the stop-during-streaming behavior could not be exercised at all.

**Diagnosis performed:** I verified the sandbox has no outbound network — `api.anthropic.com`, `api.openai.com`, `openrouter.ai`, `generativelanguage.googleapis.com` all fail DNS resolution (`DNS_PROBE_FINISHED_NO_INTERNET`). Only `http://cua_designpen.web` (a static file server — it serves the SPA and real 404s for unknown files) and an empty `localhost:80` respond. I probed for a mock AI backend (same-origin `/v1`, `/api/v1` base URLs through the app, `mockServiceWorker.js`, numerous `.web` hosts, localhost ports like 11434) and found none. The error toast's copy button couldn't be exploited to read details since clipboard paste doesn't work in this headless browser.

**Conclusion:** The chat UI itself opens and accepts prompts, but AI generation is completely non-functional in this environment (no reachable provider API and no mock backend), so the core of the task — clicking the stop button mid-stream while frames are being created — was impossible to perform and verify.

verdict: not-approve
```
