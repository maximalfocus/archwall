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
            "1 Interfaces: the terminal UI, print or JSON mode, RPC over JSONL on stdin and stdout, "
            "and the TypeScript SDK all share one agent and session. They send the prompt on. "
            "2 Build the request: the system prompt with context files, the active session branch as history, "
            "tool definitions (read, bash, edit, write by default) and skill descriptions. Extensions are "
            "TypeScript modules in the pi process that add tools, commands, providers and UI. "
            "3 Agent loop in pi-agent-core: call the model, check for tool calls (none ends the run), run the "
            "tools, record the results, and go again. A steering message goes in after the current turn, a "
            "follow-up after the run. 4 pi-ai: the loop calls one Models API, which routes each call to a "
            "provider such as Anthropic, OpenAI, Google, Bedrock, OpenRouter or any OpenAI-compatible server, "
            "and streams the answer back.")

L, R, W = 24, 624, 552
T1, H1 = 16, 412
T2, H2 = 460, 400

# 1 interfaces
d.group(L, T1, W, H1, "Interfaces", 1)
d.sub(L + 12, T1 + 58, W - 24, 280, "pi-coding-agent")
for i, lbl in enumerate(["Terminal UI|pi-tui", "Print / JSON|for scripts", "RPC|JSONL on stdio", "SDK|TypeScript"]):
    d.card(L + 30 + (i % 2) * 254, T1 + 112 + (i // 2) * 106, lbl, w=238, h=82)
d.note(L + W / 2, T1 + 378, "all four share one agent and session")

# 2 build the request
d.group(R, T1, W, H1, "Build the request", 2)
for i, (lbl, k) in enumerate([("System prompt|+ context files", "data"), ("History|active branch", "data"),
                              ("Tools|read, bash, edit, write", "coding"), ("Skills|descriptions only", "data")]):
    d.card(R + 18 + (i % 2) * 264, T1 + 64 + (i // 2) * 96, lbl, k, w=252, h=80)
d.sub(R + 12, T1 + 264, W - 24, 132, "Extensions")
d.note(R + W / 2, T1 + 338, "TypeScript in the pi process")
d.note(R + W / 2, T1 + 364, "add tools, commands, providers, UI")

# 3 agent loop
d.group(R, T2, W, H2, "Agent loop: pi-agent-core", 3)
CW, CH = 226, 76
A = (R + 30, T2 + 72)    # call the model
B = (R + 296, T2 + 72)   # tool calls?
C = (R + 296, T2 + 216)  # run tools
D = (R + 30, T2 + 216)   # record
d.card(*A, "Call the model", "plan", w=CW, h=CH)
d.card(*B, "Tool calls?|none: run ends", w=CW, h=CH)
d.card(*C, "Run the tools|in parallel", "coding", w=CW, h=CH)
d.card(*D, "Record results|go again", "write", w=CW, h=CH)
d.arrow(f"M{A[0] + CW} {A[1] + CH / 2}H{B[0]}")
d.arrow(f"M{B[0] + CW / 2} {B[1] + CH}V{C[1]}", label="yes", at=(B[0] + CW / 2 + 26, B[1] + CH + 40))
d.arrow(f"M{C[0]} {C[1] + CH / 2}H{D[0] + CW}")
d.arrow(f"M{D[0] + CW / 2} {D[1]}V{A[1] + CH}")
d.cycle(R + W / 2, T2 + 182, 12)
d.note(R + W / 2, T2 + 340, "steering: after this turn")
d.note(R + W / 2, T2 + 366, "follow-up: after the whole run")

# 4 pi-ai
d.group(L, T2, W, H2, "pi-ai: one API", 4)
d.card(L + 30, T2 + 72, "Models|routes each call", w=238, h=76)
d.sub(L + 12, T2 + 172, W - 24, 196, "Providers")
for i, lbl in enumerate(["Anthropic", "OpenAI", "Google", "Bedrock", "OpenRouter", "OpenAI-|compatible"]):
    d.card(L + 26 + (i % 3) * 170, T2 + 214 + (i // 3) * 72, lbl, w=160, h=62)

# hand-offs between stages, drawn last so they sit on top
MID = (L + 268 + A[0]) / 2
d.arrow(f"M{L + W - 12} {T1 + 200}H{R + 18}", label="prompt", at=(L + W + 24, T1 + 188))
d.arrow(f"M{A[0] + CW / 2} {T1 + H1}V{A[1]}", label="request", at=(A[0] + CW / 2 + 48, T1 + H1 + 22))
d.arrow(f"M{A[0]} {A[1] + 24}H{L + 268}", label="call", at=(MID, A[1] + 16))
d.arrow(f"M{L + 268} {A[1] + 54}H{A[0]}", back=True, label="stream", at=(MID, A[1] + 80))

d.note(600, 888, "pi · packages: pi-coding-agent → pi-agent-core → pi-ai, pi-tui")

d.save(Path(__file__).with_name("diagram.svg"))
