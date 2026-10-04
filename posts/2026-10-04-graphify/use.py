"""graphify: how an assistant uses the graph, and how the graph stays current.  Drawn from the
graphify repo (https://github.com/Graphify-Labs/graphify, README.md sections "Make your assistant
always use the graph", "Recommended workflow" and "Using the graph directly", commit 48d7c0e).
Run: python3 use.py

Snake order: 1 the assistant (top left) -> 2 ask the graph (top right) -> 3 keep it current
(bottom, full width)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("graphify in use",
            "1 The assistant: graphify claude install writes a CLAUDE.md section that says to query the "
            "graph first, and a PreToolUse hook that fires before search commands and file reads and points "
            "the assistant to the graph. Platforms without hooks get an instruction file such as AGENTS.md. "
            "2 Ask the graph: the CLI has query, path and explain; an MCP server offers query_graph, "
            "get_node, get_neighbors and shortest_path, over stdio for one developer or HTTP for a team. "
            "Both read graph.json and return a small subgraph instead of raw files. "
            "3 Keep it current: after graphify hook install, git commit and branch switches rebuild the code "
            "part in the background with AST only and no API cost. After git pull or merge, run graphify "
            "update. When docs or papers change, run /graphify --update, which uses the LLM pass.")

L, R, W = 24, 624, 552
T1, H1 = 16, 476
T2, H2 = 524, 336

# 1 the assistant
d.group(L, T1, W, H1, "Your assistant", 1)
d.pill(L + 126, T1 + 68, 300, 52, "question about the code")
d.card(L + 30, T1 + 156, "CLAUDE.md|query the graph first", "plan", w=W - 60, h=80)
d.card(L + 30, T1 + 260, "PreToolUse hook|before grep and Read", "review", w=W - 60, h=80)
d.note(L + W / 2, T1 + 392, "no hooks on your platform:")
d.note(L + W / 2, T1 + 418, "an AGENTS.md-style file instead")

# 2 ask the graph
d.group(R, T1, W, H1, "Ask the graph", 2)
d.card(R + 30, T1 + 72, "CLI|query, path, explain", "coding", w=238, h=80)
d.card(R + 284, T1 + 72, "MCP server|stdio or HTTP", "coding", w=238, h=80)
d.card(R + 156, T1 + 230, "graph.json", "data", w=240, h=64)
d.arrow(f"M{R + 149} {T1 + 152}V{T1 + 200}H{R + 230}V{T1 + 230}")
d.arrow(f"M{R + 403} {T1 + 152}V{T1 + 200}H{R + 322}V{T1 + 230}")
d.pill(R + 126, T1 + 340, 300, 52, "a small subgraph", "front")
d.arrow(f"M{R + W / 2} {T1 + 294}V{T1 + 340}")
d.note(R + W / 2, T1 + 432, "not the raw files")

# 3 keep it current
d.group(L, T2, 1152, H2, "Keep it current", 3)
CW, CH = 340, 80
for i, (top, bot) in enumerate([("git commit, switch|rebuilds by itself", "AST only, no API cost"),
                                 ("git pull, merge|graphify update .", "you run it"),
                                 ("docs changed|/graphify --update", "LLM pass, costs tokens")]):
    x = L + 30 + i * 376
    d.card(x, T2 + 84, top, "write", w=CW, h=CH)
    d.note(x + CW / 2, T2 + 200, bot)
d.note(600, T2 + 270, "graphify hook install sets up the git hooks once per clone")

# hand-offs between stages, drawn last so they sit on top
d.arrow(f"M{L + W - 12} {T1 + 112}H{R + 30}", label="query", at=(L + W + 24, T1 + 100))
d.arrow(f"M{R + 126} {T1 + 366}H{L + W - 12}", label="subgraph", at=(657, T1 + 354))
d.arrow(f"M{R + W - 60} {T2}V{T1 + 262}H{R + 396}", back=True, label="rebuilds", at=(R + W - 60, T1 + 400))

d.save(Path(__file__).with_name("use.svg"))
