"""Pi overview: how one prompt runs, from the way in to the model provider.  Drawn from the pi repo
(https://github.com/earendil-works/pi, README.md, packages/coding-agent/docs/how-pi-works.md, cli.md,
cli-integration.md, packages/agent/README.md, packages/ai/README.md and src/providers/all.ts,
commit b2b5c42).  Run: python3 diagram.py

Snake order: 1 ways in (top left) -> 2 the agent session, pi-coding-agent (top right) ->
3 agent loop, pi-agent-core (bottom right) -> 4 pi-ai and the providers (bottom left)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("Pi coding agent overview",
            "1 Ways in: the terminal UI, print or JSON mode for scripts, RPC over JSONL on stdin and stdout, "
            "and the TypeScript SDK. All four use the same agent and session. "
            "2 The agent session in pi-coding-agent: it builds the context from the system prompt and the "
            "active session branch, holds the tools (read, bash, edit and write are on by default), loads "
            "extensions, and saves everything to a session file. "
            "3 The agent loop in pi-agent-core: call the model, check for tool calls (none ends the run), run "
            "the tools, record the results and go again. "
            "4 pi-ai: one API that routes each call to one of 42 built-in providers, such as Anthropic, "
            "OpenAI, Google, Bedrock or OpenRouter, or to any OpenAI-compatible server, and streams the "
            "answer back.")

L, R, W = 24, 624, 552
T1, H1 = 16, 412
T2, H2 = 460, 400

# 1 ways in
d.group(L, T1, W, H1, "Ways in", 1)
for i, lbl in enumerate(["Terminal UI|for people", "Print / JSON|for scripts",
                         "RPC|JSONL on stdin/out", "SDK|TypeScript, in process"]):
    d.card(L + 30 + (i % 2) * 254, T1 + 80 + (i // 2) * 112, lbl, w=238, h=84)
d.note(L + W / 2, T1 + 352, "all four use the same agent")
d.note(L + W / 2, T1 + 378, "and the same session")

# 2 the agent session
d.group(R, T1, W, H1, "Agent session", 2)
for i, (lbl, k) in enumerate([("Context|prompt + active branch", "data"), ("Tools|4 on by default", "coding"),
                              ("Extensions|add tools, commands", None), ("Session file|JSONL, a tree", "write")]):
    d.card(R + 18 + (i % 2) * 264, T1 + 80 + (i // 2) * 112, lbl, k, w=252, h=84)
d.note(R + W / 2, T1 + 352, "package: pi-coding-agent")
d.note(R + W / 2, T1 + 378, "saved automatically, unless --no-session")

# 3 agent loop
d.group(R, T2, W, H2, "Agent loop", 3)
CW, CH = 226, 76
A = (R + 30, T2 + 72)    # call the model
B = (R + 296, T2 + 72)   # tool calls?
C = (R + 296, T2 + 216)  # run tools
D = (R + 30, T2 + 216)   # record
d.card(*A, "Call the model", "plan", w=CW, h=CH)
d.card(*B, "Tool calls?|none: run ends", w=CW, h=CH)
d.card(*C, "Run the tools", "coding", w=CW, h=CH)
d.card(*D, "Record results|go again", "write", w=CW, h=CH)
d.arrow(f"M{A[0] + CW} {A[1] + CH / 2}H{B[0]}")
d.arrow(f"M{B[0] + CW / 2} {B[1] + CH}V{C[1]}", label="yes", at=(B[0] + CW / 2 + 26, B[1] + CH + 40))
d.arrow(f"M{C[0]} {C[1] + CH / 2}H{D[0] + CW}")
d.arrow(f"M{D[0] + CW / 2} {D[1]}V{A[1] + CH}")
d.cycle(R + W / 2, T2 + 182, 12)
d.note(R + W / 2, T2 + 352, "package: pi-agent-core")

# 4 pi-ai
d.group(L, T2, W, H2, "pi-ai: one API", 4)
d.card(L + 30, T2 + 72, "Models|routes each call", w=238, h=76)
d.sub(L + 12, T2 + 172, W - 24, 208, "42 built-in providers, e.g.")
for i, lbl in enumerate(["Anthropic", "OpenAI", "Google", "Bedrock", "OpenRouter", "Mistral"]):
    d.card(L + 26 + (i % 3) * 170, T2 + 214 + (i // 3) * 76, lbl, w=160, h=64)

# hand-offs between stages, drawn last so they sit on top
MID = (L + 268 + A[0]) / 2
d.arrow(f"M{L + W} {T1 + 200}H{R}", label="prompt", at=(600, T1 + 188))
d.arrow(f"M{A[0] + CW / 2} {T1 + H1}V{A[1]}", label="request", at=(A[0] + CW / 2 + 48, T1 + H1 + 22))
d.arrow(f"M{A[0]} {A[1] + 24}H{L + 268}", label="call", at=(MID, A[1] + 16))
d.arrow(f"M{L + 268} {A[1] + 54}H{A[0]}", back=True, label="stream", at=(MID, A[1] + 80))

d.note(600, 888, "pi · github.com/earendil-works/pi · MIT")

d.save(Path(__file__).with_name("diagram.svg"))
