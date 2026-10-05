"""Pi and model providers: from picking a model to the provider's wire API, inside pi-ai.  Drawn from
the pi repo (https://github.com/earendil-works/pi, packages/ai/README.md "Providers and Models",
"Auth", "Cross-Provider Handoffs", packages/ai/src/providers/all.ts (42 built-in providers),
packages/coding-agent/docs/models.md, providers.md, virtual-models.md and custom-provider.md,
commit b2b5c42).  Run: python3 providers.py

Snake order: 1 pick a model (top left) -> 2 Models collection (top right) -> 3 the provider
(bottom right) -> 4 add your own (bottom left), which registers back into 2."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("Pi model providers",
            "1 Pick a model with /model or --model. A virtual model, added by an extension, picks a real "
            "model for each request. The model can change mid-session. "
            "2 pi-ai's Models collection holds the providers, 42 built in, and routes each request to the "
            "provider that owns the model. "
            "3 Each provider owns its model list, its sign-in (an API key, OAuth through /login saved in "
            "auth.json, or cloud credentials for Bedrock and Vertex), and the wire API it speaks, such as "
            "anthropic-messages, openai-responses or openai-completions. "
            "4 Add your own: models.json for endpoints that speak a supported API, such as Ollama, vLLM or "
            "LM Studio; the llama.cpp router for local models; or a provider extension for anything else.")

L, R, W = 24, 624, 552
T1, H1 = 16, 412
T2, H2 = 460, 400
CW = 492

# 1 pick a model
d.group(L, T1, W, H1, "Pick a model", 1)
d.card(L + 30, T1 + 72, "/model or --model", w=CW, h=64, cls="human")
d.card(L + 30, T1 + 168, "Virtual model|picks one per request", "plan", w=CW, h=76)
d.note(L + W / 2, T1 + 310, "virtual models come from extensions")

# 2 Models collection
d.group(R, T1, W, H1, "pi-ai: Models", 2)
d.card(R + 30, T1 + 80, "Models|routes to the owner", "plan", w=CW, h=84)
d.sub(R + 12, T1 + 196, W - 24, 140, "42 built-in providers")
d.note(R + W / 2, T1 + 266, "Anthropic, OpenAI, Google,")
d.note(R + W / 2, T1 + 292, "Bedrock, OpenRouter, Mistral …")

# 3 the provider
d.group(R, T2, W, H2, "Each provider owns", 3)
d.card(R + 30, T2 + 64, "Model list|catalog, can refresh", "data", w=CW, h=72)
d.card(R + 30, T2 + 160, "Sign-in|API key, /login, cloud", "review", w=CW, h=72)
d.card(R + 30, T2 + 256, "Wire API|e.g. openai-completions", "coding", w=CW, h=72)

# 4 add your own
d.group(L, T2, W, H2, "Add your own", 4)
d.card(L + 30, T2 + 64, "models.json|Ollama, vLLM, LM Studio", "write", w=CW, h=72)
d.card(L + 30, T2 + 160, "llama.cpp router|local GGUF models", "write", w=CW, h=72)
d.card(L + 30, T2 + 256, "Provider extension|custom sign-in or protocol", "coding", w=CW, h=72)

# hand-offs, drawn last so they sit on top
d.arrow(f"M{L + W} {T1 + 122}H{R}", label="model", at=(600, T1 + 110))
d.arrow(f"M{R + W / 2} {T1 + H1}V{T2}", label="request", at=(R + W / 2 + 44, T1 + H1 + 22))
d.arrow(f"M{L + W - 40} {T2}V{T1 + H1 + 16}H{R + 40}V{T1 + H1}", label="registers", at=(600, T1 + H1 + 22))

d.note(R + W / 2, T1 + 374, "switch models mid-session, history kept")
d.note(600, 888, "credentials: --api-key, then auth.json, models.json, env vars")

d.save(Path(__file__).with_name("providers.svg"))
