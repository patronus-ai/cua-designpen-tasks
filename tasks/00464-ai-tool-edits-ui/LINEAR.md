# DesignPen [toolbelt]: 'ai tool edits' fails QA — 5/5 runs report broken workflow (00464-ai-tool-edits-ui)

Description:
Asking the DesignPen/OpenPencil AI assistant to build design elements via tool edits never works: the assistant never responds and nothing is created on the canvas. The AI chat panel opens fine (right-panel "AI" tab and Ctrl/Cmd+J) and the connect flow and chat input work mechanically, but the panel is not pre-connected ("Connect an AI provider to start chatting") and every send of "Build a simple profile card: a frame containing a text title and a circle for the avatar" immediately produces a red toast "An error occurred." with no assistant reply. Root cause verified by the agent: the sandbox has no network route to any AI provider (DNS fails for openrouter.ai, api.anthropic.com, even example.com) and no local/mock AI endpoint exists. Additionally, the error toast's "copy details" button silently copies nothing (clipboard no-op on the insecure HTTP origin) and the error text is unhelpfully generic.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Open the AI chat panel via the right-panel "AI" tab or the Ctrl/Cmd+J shortcut.
3. Observe the "Connect an AI provider to start chatting" prompt; connect a provider (e.g. OpenRouter or Anthropic) with a test API key.
4. Type and send the message "Build a simple profile card: a frame containing a text title and a circle for the avatar".
5. Optionally reload the page, reconnect a provider, and send again.
6. Check the canvas and the Layers panel for any created frame, text, or circle.

Actual Result:

- Every send of the message immediately produces a red toast "An error occurred." with no assistant reply (tried both OpenRouter and Anthropic providers with test keys, including after a full page reload).
- Nothing is created on the canvas — Layers stays empty (no frame, text, or circle).
- Root cause: the sandbox has no network route to any AI provider — DNS resolution fails for openrouter.ai (including the exact `/api/v1/chat/completions` endpoint), api.anthropic.com, and even example.com — and there is no local/mock AI endpoint (localhost:11434 refused; the app's own origin only serves the SPA for every path).
- Minor additional bug: the error toast's "copy details" button silently copies nothing (clipboard no-op on this insecure HTTP origin), and the error message itself is an unhelpfully generic "An error occurred."

Expected Result:
The AI assistant should respond to the prompt and create the requested elements via tool edits — a frame containing a text title and a circle should appear on the canvas and in the Layers panel.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed (agent verdict: not-approve)
- Attempt transcripts:
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_2d24bc57-8fe7-4dee-bd05-7224d8a4fa71.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_3af96f7a-3ec8-4a70-9451-01a554179f79.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_51037b30-b2b1-4323-ade2-0b2b372909ca.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_66632a0d-d55e-4041-ab00-34c2afbc786d.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_85bc343f-726c-4761-addd-ab9f6665e736.txt`

Agent report (verbatim tail of failing run):

```
I completed the requested steps, but the AI assistant never actually responded. Here's a summary of what happened:

**What worked:**
- The AI chat panel opened fine, both via the right-panel "AI" tab and via the Ctrl/Cmd+J shortcut.
- The panel's connect flow and chat input worked mechanically: I connected a provider and typed/sent the exact message "Build a simple profile card: a frame containing a text title and a circle for the avatar" (it appears as a sent bubble in the chat).

**What failed:**
- The AI panel was not pre-connected — it demanded an AI provider + API key ("Connect an AI provider to start chatting"), and no key was provided by the environment.
- After connecting (tried both OpenRouter and Anthropic providers with test keys, including after a full page reload), every send of the message immediately produced a red toast **"An error occurred."** with no assistant reply, and nothing was created on the canvas (Layers stayed empty — no frame, text, or circle).
- I verified the root cause: the sandbox has no network route to any AI provider — DNS resolution fails for openrouter.ai (including the exact `/api/v1/chat/completions` endpoint), api.anthropic.com, and even example.com — and there is no local/mock AI endpoint (localhost:11434 refused; the app's own origin only serves the SPA for every path). So the chat request can never succeed in this environment.
- Minor additional bug: the error toast's "copy details" button silently copies nothing (clipboard no-op on this insecure HTTP origin), and the error itself is an unhelpfully generic "An error occurred."

So while the panel UI itself opens and accepts input, the core ask — getting the assistant to build the profile card — was blocked: the AI never responded and no design elements were created.

verdict: not-approve
```
