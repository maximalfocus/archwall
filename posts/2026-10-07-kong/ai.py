"""Kong in front of LLMs: the open-source AI plugins, in the order they touch one chat call.
Snake order: 1 the app calls a route (top left) -> 2 shape the request (top right) -> 3 AI Proxy (bottom right) -> 4 answer back (bottom left).
Drawn from Kong/kong at commit 8927af6 (kong/llm/schemas/init.lua, kong/llm/drivers, kong/plugins/ai-*/handler.lua and schema.lua).
Run: python3 ai.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, R, GW, T1, H1, T2, H2  # noqa: E402

d = Diagram("Kong in front of LLMs",
            "In: an app sends a chat call to a Kong route. "
            "1 The app calls a route: a chat call (llm/v1/chat), a completions call (llm/v1/completions), "
            "or preserve, which is passed on without translation. "
            "2 Shape the request, in priority order: AI Request Transformer asks an LLM to rewrite the body, "
            "AI Prompt Template fills a named template's placeholders, AI Prompt Decorator adds chat messages "
            "before or after, and AI Prompt Guard checks allow and deny patterns. "
            "3 AI Proxy translates the call into the provider's format, adds the provider key as a header "
            "or parameter, and sends it to one of 9 providers: OpenAI, Azure, Anthropic, Cohere, Mistral, "
            "Llama 2, Gemini, Bedrock and Hugging Face. "
            "4 Answer back: the reply is translated back into the same call shape, AI Response Transformer can "
            "ask an LLM to rewrite it, and token statistics go to the log plugins only when log_statistics is "
            "on; prompts and replies are logged only when log_payloads is on. Both are off by default.")

d.pill(L, 16, GW, 48, "In: an app sends a chat call to a Kong route")
d.arrow(f"M{L + GW / 2} 64V{T1 - 2}")

d.group(L, T1, GW, H1, "The app calls a route", 1)
d.column(L, T1, [("Chat call|llm/v1/chat", "coding"),
                 ("Completions call|llm/v1/completions", "coding"),
                 ("Preserve|passed on as is", "coding")])
d.notes(L, T1, H1, "Same call shape for every provider", "")

d.group(R, T1, GW, H1, "Shape the request", 2)
d.column(R, T1, [("AI Request Transformer|an LLM rewrites the body", "write"),
                 ("AI Prompt Template|fills {{placeholders}}", "write"),
                 ("AI Prompt Decorator|adds messages before · after", "write"),
                 ("AI Prompt Guard|allow · deny patterns", "review")], h=60, gap=14, first=60)

d.group(R, T2, GW, H2, "AI Proxy", 3)
d.column(R, T2, [("Translate|into the provider's format", "coding"),
                 ("Add the provider key|header or parameter", "review"),
                 ("9 providers|OpenAI · Anthropic · Gemini …", "coding")])

d.group(L, T2, GW, H2, "Answer back", 4)
d.column(L, T2, [("Translate back|into the same call shape", "coding"),
                 ("AI Response Transformer|an LLM rewrites the reply", "write"),
                 ("Token statistics|to the log plugins", "data")])
d.notes(L, T2, H2, "Statistics · payload logs: off by default", "")

d.arrow(f"M{L + GW} {T1 + 200}H{R - 2}", label="call", at=(600, T1 + 188))
d.arrow(f"M{R + 430} {T1 + H1}V{T2 - 2}", label="prompt", at=(R + 430, T1 + H1 + 24))
d.arrow(f"M{R} {T2 + 176}H{L + GW + 2}", label="reply", at=(600, T2 + 164))

d.save(Path(__file__).with_name("ai.svg"))
