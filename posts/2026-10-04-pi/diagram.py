"""Pi, the coding agent: how one prompt runs.  Drawn from the pi repo
(https://github.com/earendil-works/pi, packages/coding-agent/docs/how-pi-works.md, the package
READMEs and package.json files, commit 2003871).  Run: python3 diagram.py

Snake order: 1 interfaces (top left) -> 2 build the request (top right) -> 3 agent loop
(bottom right) -> 4 pi-ai providers (bottom left)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("Pi coding agent architecture",
            "1 Interfaces: interactive terminal UI, print or JSON mode, RPC over JSONL on stdin and stdout, "
            "and the TypeScript SDK all drive the same agent and session. "
            "2 Build the request: the system prompt with context files, the active session branch as history, "
            "tool definitions (read, bash, edit, write by default) and skill descriptions. Extensions are "
            "TypeScript modules in the pi process that add tools, commands, providers and UI and can transform "
            "context. 3 Agent loop in pi-agent-core: send the request, stream back text and tool calls, run the "
            "tools (in parallel by default), record the results, and start another turn until no tool calls "
            "are left. 4 pi-ai: one API over many providers, such as Anthropic, OpenAI, Google and any "
            "OpenAI-compatible server.")

L, R, W = 24, 624, 552
T1, H1 = 16, 412
T2, H2 = 460, 396

# 1 interfaces
d.group(L, T1, W, H1, "Interfaces", 1)
d.sub(L + 12, T1 + 46, W - 24, 266, "pi-coding-agent, one per need")
for i, (lbl, k) in enumerate([("Interactive|terminal UI, pi-tui", None), ("Print / JSON|one prompt, or events", None),
                              ("RPC|JSONL on stdin / stdout", None), ("SDK|TypeScript, in process", None)]):
    d.card(L + 36 + (i % 2) * 252, T1 + 92 + (i // 2) * 104, lbl, "data", w=228, h=76)
d.note(L + W / 2, T1 + 344, "all four drive the same agent and session")
d.note(L + W / 2, T1 + 368, "prompt templates expand what you type")
d.note(L + W / 2, T1 + 392, "agent events stream back to the screen")

# 2 build the request
d.group(R, T1, W, H1, "Build the request", 2)
for i, lbl in enumerate(["System prompt|base + context files", "History|the active session branch",
                         "Tools|read · bash · edit · write", "Skills|descriptions only"]):
    d.card(R + 24 + (i % 2) * 260, T1 + 56 + (i // 2) * 82, lbl, "coding" if i == 2 else "data", w=244, h=66)
d.sub(R + 12, T1 + 230, W - 24, 168, "Extensions and resources")
d.note(R + W / 2, T1 + 284, "extensions: TypeScript in the pi process")
d.note(R + W / 2, T1 + 308, "they add tools, commands, providers, UI")
d.note(R + W / 2, T1 + 332, "skills: full text loaded only when needed")
d.note(R + W / 2, T1 + 356, "all shared as pi packages via npm or git")

# 3 agent loop
d.group(R, T2, W, H2, "Agent loop: pi-agent-core", 3)
A = (R + 36, T2 + 60)    # call the model
B = (R + 300, T2 + 60)   # tool calls?
C = (R + 300, T2 + 176)  # run tools
D = (R + 36, T2 + 176)   # record
d.card(*A, "Call the model|stream text + tool calls", "plan", w=220, h=64)
d.card(*B, "Any tool calls?|none: the run ends", "critic", w=220, h=64)
d.card(*C, "Run the tools|in parallel by default", "coding", w=220, h=64)
d.card(*D, "Record the results|then another turn", "write", w=220, h=64)
d.arrow(f"M{A[0] + 220} {A[1] + 32}H{B[0]}")
d.arrow(f"M{B[0] + 110} {B[1] + 64}V{C[1]}")
d.arrow(f"M{C[0]} {C[1] + 32}H{D[0] + 220}")
d.arrow(f"M{D[0] + 110} {D[1]}V{A[1] + 64}")
d.cycle(R + W / 2, T2 + 154, 10)
d.note(R + W / 2, T2 + 290, "steering message: goes in after this turn")
d.note(R + W / 2, T2 + 314, "follow-up message: goes in after the run")
d.note(R + W / 2, T2 + 338, "abort: stop, queued messages go back to the editor")

# 4 pi-ai
d.group(L, T2, W, H2, "pi-ai: one API, many providers", 4)
d.card(L + 166, T2 + 60, "Models|routes each call", "plan", w=220, h=64)
d.sub(L + 12, T2 + 148, W - 24, 160, "Providers: catalog, auth, stream")
for i, lbl in enumerate(["Anthropic", "OpenAI", "Google", "Bedrock", "OpenRouter", "OpenAI-compatible|Ollama, vLLM …"]):
    d.card(L + 30 + (i % 3) * 170, T2 + 186 + (i // 3) * 62, lbl, w=154, h=52 if i < 5 else 52)
d.note(L + W / 2, T2 + 334, "API key or OAuth subscription, via /login")
d.note(L + W / 2, T2 + 358, "switch model mid-session, keep the context")

# hand-offs between stages, drawn last so they sit on top
d.arrow(f"M{L + W} {T1 + 200}H{R}")                      # 1 -> 2
d.arrow(f"M{R + 146} {T1 + H1}V{T2 + 60}")               # 2 -> 3
d.arrow(f"M{R + 36} {T2 + 84}H{L + 386}")                # 3 -> 4: call
d.arrow(f"M{L + 386} {T2 + 108}H{R + 36}", back=True)         # 4 -> 3: stream

d.note(600, 884, "pi · github.com/earendil-works/pi · packages: pi-coding-agent → pi-agent-core → pi-ai, pi-tui")

d.save(Path(__file__).with_name("diagram.svg"))
