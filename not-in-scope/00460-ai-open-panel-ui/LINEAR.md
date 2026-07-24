# DesignPen [AI panel]: 'ai open panel' fails QA — 5/5 runs report broken workflow (00460-ai-open-panel-ui)

Description:
In the DesignPen/OpenPencil design app, opening the AI chat panel works via both documented paths (right-panel AI tab and Ctrl/Cmd+J shortcut, which toggles the panel with chat history preserved), but the assistant never responds to any request, so asking it to add a rectangle to the canvas fails every time. The panel requires connecting a provider first ("Connect an AI provider to start chatting"); with a placeholder OpenRouter key the chat UI appears (Claude Sonnet 4.6 model selector + "Describe a change…" input) and messages send successfully, but every send triggers a red toast "An error occurred." with no detail, no assistant message, and no rectangle — the canvas stays blank and the Layers panel empty. Root cause appears environmental: the sandbox has no internet (openrouter.ai and api.anthropic.com return DNS_PROBE_FINISHED_NO_INTERNET), no valid/mocked provider is provisioned, no same-origin mock endpoint exists (all app routes serve the SPA), and the AI settings offer no offline/demo mode.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Open the AI chat panel via the AI tab in the right panel (Design / Code / AI tablist), or press Ctrl/Cmd+J.
3. Connect a provider in the "Connect an AI provider to start chatting" view (e.g., OpenRouter with a placeholder API key) to reveal the chat UI.
4. Type "Add a rectangle to the canvas" into the "Describe a change…" input and send it.
5. Wait for the assistant's response and check the canvas and Layers panel for the new rectangle.

Actual Result:
- The message is typed and sent successfully and appears as a user bubble, but the assistant never responds; every sent message triggers a red toast "An error occurred." with no further detail, no assistant message, and no loading indicator on the first attempt (the toast apparently disappeared before it could initially be seen). Retried three times with the same result.
- No rectangle is ever added — the canvas remains blank and the Layers panel is empty.
- The sandbox has no internet access (openrouter.ai and api.anthropic.com return DNS_PROBE_FINISHED_NO_INTERNET), no valid/mocked AI provider or API key is provisioned, no same-origin mock endpoint exists (all app routes serve the SPA), and the AI settings offer no offline/demo mode.

Expected Result:
After sending "Add a rectangle to the canvas", the assistant should respond and add a rectangle to the canvas (visible on the canvas and in the Layers panel), which requires a working or mocked AI provider in the environment; failures should surface a detailed error rather than a bare "An error occurred." toast. Panel opening via the AI tab and Cmd+J already works.

Estimate: S (2 points) — small handler/layout fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed (agent verdict: not-approve)
- Attempt transcripts:
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_9de91b69-798c-4e06-8052-b9ee0966fcb4.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_a9c30027-290b-4008-9470-6c54a81995c1.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_f7eabb69-b39b-44a9-8e8d-297de0be5c10.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_fb759f16-c1df-4913-a0c5-0df3fe20e9d0.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_fddee037-734f-4e36-ae6f-41ac5ba914e4.txt`

Agent report (verbatim tail of failing run):

```
I have completed the requested steps and verified the final state. Here's a summary of what happened:

**What I did:**
1. Opened the AI chat panel via the **AI tab** in the right panel (Design / Code / AI tablist). I also verified the **Cmd+J (Ctrl+J) shortcut** correctly toggles the AI panel closed and open, with chat history preserved.
2. The AI panel first required connecting a provider ("Connect an AI provider to start chatting" with OpenRouter/Anthropic/OpenAI/etc. options and an API key field). No pre-configured provider existed, so I connected using a placeholder OpenRouter key, which revealed the chat UI (Claude Sonnet 4.6 model selector + "Describe a change…" input).
3. Asked the assistant to **"Add a rectangle to the canvas"** — the message was typed and sent successfully, and it appears as a user bubble in the chat. I retried two more times.

**What went wrong:**
- The assistant **never responded**. Every sent message triggers a red toast: **"An error occurred."** — with no further detail in the UI, no assistant message, no loading indicator on the first attempt (the toast apparently disappeared before I could see it initially).
- **No rectangle was ever added** — the canvas remains blank and the Layers panel is empty.
- Root cause appears environmental: the sandbox has no internet access (direct checks of `openrouter.ai` and `api.anthropic.com` return DNS_PROBE_FINISHED_NO_INTERNET), and no valid/mocked AI provider or API key was provisioned, so the AI chat request can never succeed. There is also no same-origin mock endpoint (all app routes serve the SPA), and the AI settings offer no offline/demo mode.

So while the panel opened fine via both methods and the message was successfully submitted, the core goal — the assistant actually adding a rectangle to the canvas — failed with an error every time, blocked by the lack of a working AI provider in this environment.

verdict: not-approve
```
