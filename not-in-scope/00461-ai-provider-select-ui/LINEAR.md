# DesignPen [AI panel]: 'ai provider select' fails QA — 4/4 runs report broken workflow (00461-ai-provider-select-ui)

Description:
In the DesignPen/OpenPencil design app's AI chat panel, provider/model switching works mechanically (settings gear's AI Provider selector + bottom-bar model selector, key entry, key persistence, history preserved across switches), but no selected provider ever responds, so the confirmation step — asking the new setup to draw a green ellipse — is impossible. Every "Draw a green ellipse" request across four providers (OpenRouter/Claude Sonnet 4.6, Anthropic/Claude Opus 4.6, OpenAI/GPT-5.3 Codex, Google AI/Gemini 3.1 Pro) immediately produced a generic red toast "An error occurred." with no assistant message and no ellipse (Layers stayed empty). Root cause: no outbound internet in the sandbox (openrouter.ai and api.openai.com fail DNS — DNS_PROBE_FINISHED_NO_INTERNET), no mocked AI endpoints, no working API keys, and no pre-connected provider. Secondary UX bugs: the error toast carries no detail, the failed user message silently disappears from the thread, and the toast's copy-error button produces nothing pasteable (app served over http, clipboard API likely unavailable).

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Open the AI chat panel via the right panel's AI tab or press Ctrl/Cmd+J; the panel starts in a "Connect an AI provider" state.
3. Connect the default provider (OpenRouter, model Claude Sonnet 4.6) with an API key.
4. Open the settings gear's AI Provider selector and switch to a different provider (e.g., Anthropic), then use the bottom-bar model selector to pick a different model (e.g., Claude Opus 4.6), entering an API key as prompted.
5. Ask the assistant to "Draw a green ellipse" and send the message.
6. Check the chat for a response and the canvas/Layers panel for the ellipse.

Actual Result:
- Every "Draw a green ellipse" request — tried with OpenRouter/Claude Sonnet 4.6, Anthropic/Claude Opus 4.6, OpenAI/GPT-5.3 Codex, and Google AI/Gemini 3.1 Pro — immediately produced a red toast "An error occurred." with no assistant message; no ellipse was created on the canvas (Layers stayed empty).
- External AI endpoints are unreachable in this environment (DNS_PROBE_FINISHED_NO_INTERNET for openrouter.ai and api.openai.com), no local mock is served by the app origin, no working API keys were provided, and no provider came pre-connected.
- The error toast is generic (no detail), the failed user message silently disappears from the thread, and the toast's copy-error button produced nothing pasteable (app is served over http, so clipboard API is likely unavailable).
- Provider/model switching, key entry, and key persistence all worked mechanically, and chat history was preserved across switches.

Expected Result:
After switching to a different provider and model, sending "Draw a green ellipse" should get an assistant response and a green ellipse drawn on the canvas, confirming the new setup responds — this requires a working or mocked AI provider in the environment. Chat failures should surface a detailed error, keep the failed message in the thread, and the copy-error button should work.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 4 of 4 completed runs failed (agent verdict: not-approve)
- Attempt transcripts:
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_1f5d40da-3d44-433c-afb2-22a16b6d8336.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_417cc184-358c-4084-9adf-4a64c161118f.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_733a940d-b45b-4a9c-b1c3-d69940f168ae.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_8729e0c0-9a44-4c36-942b-026b7138403b.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_a4a23cc5-933c-4046-8e9c-780c6126a5b2.txt`

Agent report (verbatim tail of failing run):

```
Google AI also fails instantly with the same generic "An error occurred." toast. The canvas and Layers panel remain empty — no ellipse was ever drawn. I've now confirmed the failure across four providers (OpenRouter, Anthropic, OpenAI, Google AI) and verified via direct navigation that external AI endpoints are unreachable in this environment (DNS_PROBE_FINISHED_NO_INTERNET), with no local mock served by the app origin.

**Summary of what I did and found:**

What worked:
1. **Opening the AI panel** — Ctrl/Cmd+J opened the AI tab in the right panel (the AI tab also appears next to Design/Code).
2. **Provider/model switching UI** — The panel started in a "Connect an AI provider" state (nothing pre-connected). I connected OpenRouter (default, model Claude Sonnet 4.6), then used the settings gear's **AI Provider selector** and the bottom-bar **model selector** to switch to Anthropic + Claude Opus 4.6, later OpenAI + GPT-5.3 Codex and Google AI + Gemini 3.1 Pro. Switching providers/models, key entry, and key persistence all worked mechanically, and chat history was preserved across switches.

What failed (blocker):
- **The assistant never responds.** Every "Draw a green ellipse" request — tried with OpenRouter/Claude Sonnet 4.6, Anthropic/Claude Opus 4.6, OpenAI/GPT-5.3 Codex, and Google AI/Gemini 3.1 Pro — immediately produced a red toast "An error occurred." with no assistant message, and no ellipse was created on the canvas (Layers stayed empty).
- Root cause: the sandbox has no outbound internet (openrouter.ai and api.openai.com fail DNS), no AI endpoints are mocked, no working API keys were provided, and no provider came pre-connected — so confirming that "the new setup responds" is impossible.
- Minor issues noticed: the error toast is generic (no detail), the failed user message silently disappears from the thread, and the toast's copy-error button produced nothing pasteable (app is served over http, so clipboard API is likely unavailable).

The provider/model switching itself worked in the UI, but the required confirmation step — getting the newly selected provider/model to respond and draw a green ellipse — could not be completed: every chat request fails with "An error occurred." because the AI provider endpoints are unreachable/unmocked in this environment.

verdict: not-approve
```
