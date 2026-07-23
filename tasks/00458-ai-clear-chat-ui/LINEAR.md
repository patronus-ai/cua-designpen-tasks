# DesignPen [AI panel]: 'ai clear chat' fails QA — 5/5 runs report broken workflow (00458-ai-clear-chat-ui)

Description:
In the DesignPen/OpenPencil design app's AI chat panel, the assistant can never actually respond in this environment, so the "ask the assistant to draw a purple circle" portion of the flow is impossible. The panel requires connecting an external AI provider + API key (the app accepts any placeholder key without validation), but all provider API endpoints (openrouter.ai, api.anthropic.com, api.openai.com) fail DNS resolution in the sandbox and there is no local mock endpoint (localhost:11434 refused). Sending a message fails either completely silently (OpenRouter — no reply and no error at all, a UX bug in itself) or with only a generic red toast "An error occurred." (Anthropic, OpenAI) with no details; nothing is ever drawn. Opening the panel (AI tab / Ctrl+J) and the Clear button in the chat toolbar both work correctly — Clear wipes all messages and returns the panel to its empty state.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Open the AI chat panel via the right panel's AI tab (or press Ctrl/Cmd+J).
3. Connect an AI provider (e.g., OpenRouter, Anthropic, or OpenAI) using any placeholder API key — the app accepts it without validation.
4. Type a message asking the assistant to draw a purple circle and send it.
5. Wait for the assistant's reply and for the circle to appear on the canvas.
6. Click the Clear button in the chat toolbar to wipe the conversation.

Actual Result:
- OpenRouter: the message is sent but the assistant never replies and no error is shown at all (silent failure, waited 60+ seconds).
- Anthropic and OpenAI: an immediate generic red toast "An error occurred." appears with no details; no assistant reply ever renders and no circle is drawn (canvas and Layers panel remain empty).
- Root cause: all provider API endpoints (openrouter.ai, api.anthropic.com, api.openai.com) fail DNS resolution in this sandbox, and there is no local mock endpoint (localhost:11434 refused), so the assistant can never respond or "finish"; the "Get an OpenRouter API key" link leads to unreachable openrouter.ai.
- The Clear button in the chat toolbar works correctly, wiping all messages and returning the panel to its empty state ("Describe what you want to create or change.").

Expected Result:
After sending the request, the assistant should respond and draw a purple circle on the canvas (requiring a working or mocked AI provider in the environment), and any send failure should surface an actionable error rather than failing silently. The Clear button should then wipe the conversation — this last part already works.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed (agent verdict: not-approve)
- Attempt transcripts:
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_421c47ee-22d2-49fe-8986-2fce4d52096e.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_8e4d8162-b9b2-4eb5-a25a-edd424b17e67.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_c2febc50-e8e8-4985-8287-a94bd05b9b41.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_da95cdc0-b49d-4665-af2d-d336ef374f9a.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_f15acd81-b17c-42b1-80f2-166fabaa5563.txt`

Agent report (verbatim tail of failing run):

```
The conversation has been fully cleared — the chat shows only the empty-state message "Describe what you want to create or change." with no message bubbles remaining.

**Summary of what I did and found:**

1. **Opened the AI chat panel** — via the right panel's AI tab (and confirmed Ctrl/Cmd+J toggles the same panel).
2. **Connecting a provider was required** — the panel demanded an AI provider + API key before chatting. No credentials were available in this environment; the "Get an OpenRouter API key" link leads to openrouter.ai, which is unreachable from this sandbox. I connected using placeholder keys (the app accepts any key without validation).
3. **Asked the assistant to draw a purple circle** — this failed with every provider I tried:
   - **OpenRouter**: the message was sent but the assistant never replied and *no error was shown at all* (silent failure, waited 60+ seconds).
   - **Anthropic** and **OpenAI**: an immediate generic red toast **"An error occurred."** appeared with no details, no assistant reply ever rendered, and no circle was drawn (canvas and Layers panel remained empty).
   - Root cause: all provider API endpoints (openrouter.ai, api.anthropic.com, api.openai.com) fail DNS resolution in this sandbox, and there's no local mock endpoint (localhost:11434 refused), so the assistant can never respond or "finish."
4. **Cleared the conversation** — the Clear button in the chat toolbar worked correctly, wiping all messages and returning the panel to its empty state.

**Problems encountered:** The central step of the task — having the assistant actually draw a purple circle — was impossible. The AI chat requires an external API key/provider, no working provider or mock exists in this environment, sends fail either silently (OpenRouter path, a UX bug in itself) or with only a generic "An error occurred." toast with no actionable detail, and nothing was ever drawn. Only the panel-opening and Clear-button portions of the flow worked as described.

verdict: not-approve
```
