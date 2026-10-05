"""graphify step 4: your assistant asks the graph first.  Drawn from the graphify repo
(https://github.com/Graphify-Labs/graphify, README.md "Make your assistant always use the graph",
"Strict mode", "Using the graph directly"; graphify/install.py _claude_pretooluse_hooks (matchers
Bash|Grep and Read|Glob, hook-guard); graphify/cli.py hook-guard (nudges only when a graph exists;
--strict blocks the first raw read per session) and query (default budget 2000); graphify/serve.py
(_bfs, _dfs, _subgraph_to_text, 10 MCP tools); pyproject.toml extra mcp; commit 35adf43).
Run: python3 use.py

Snake order: 1 install once (top left) -> 2 the hook (top right) -> 3 ask (bottom right)
-> 4 the answer (bottom left)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

L, R, W = 24, 624, 552
T1, H1 = 16, 412
T2, H2 = 460, 400


def col(x, top, cards, h=72, gap=24, arrows=True):
    """One column of wide cards, top to bottom, optionally joined by arrows."""
    for i, (lbl, kind) in enumerate(cards):
        y = top + 64 + i * (h + gap)
        d.card(x + 30, y, lbl, kind, w=492, h=h)
        if arrows and i:
            d.arrow(f"M{x + W / 2} {y - gap}V{y - 2}")


def grid(x, top, cards, h=80, gap=16, y0=64):
    """Two columns of cards, filled row by row."""
    for i, (lbl, kind) in enumerate(cards):
        d.card(x + 30 + (i % 2) * 254, top + y0 + (i // 2) * (h + gap), lbl, kind, w=238, h=h)


def handoffs(a, b, c, ya=T1 + 206, yc=T2 + 200):
    """Arrows between the four groups in snake order, with what each one carries."""
    if a:
        d.arrow(f"M{L + W} {ya}H{R - 2}", label=a, at=(600, ya - 12))
    if b:
        d.arrow(f"M{R + W / 2} {T1 + H1}V{T2 - 2}", label=b, at=(R + W / 2 + 14 + len(b) * 4.6, T1 + H1 + 21))
    if c:
        d.arrow(f"M{R} {yc}H{L + W + 2}", label=c, at=(600, yc - 12))


d = Diagram("graphify step 4: your assistant asks the graph first",
            "1 Install once: graphify claude install writes a CLAUDE.md section and a PreToolUse hook. Other "
            "assistants get AGENTS.md or a rules file instead. Opt-in strict mode on Claude Code blocks the first "
            "raw file read of a session. "
            "2 The hook: before a Grep or Bash search, and before a Read or Glob, it nudges the assistant to run "
            "graphify query, only when a graph exists. "
            "3 Ask: the CLI has query for a question, path from A to B, and explain for one concept; an MCP "
            "server (mcp extra) offers the same as tools. "
            "4 The answer: it finds the nodes that match the question, walks out from them breadth-first or "
            "depth-first, and returns a small subgraph as text, about 2,000 tokens by default, not whole files.")

d.group(L, T1, W, H1, "Install once", 1)
col(L, T1, [("graphify claude install|CLAUDE.md section + hook", "plan"),
            ("Other assistants|AGENTS.md or a rules file", "plan")], h=80, gap=32, arrows=False)
d.note(L + W / 2, T1 + 320, "opt-in --strict (Claude Code): blocks")
d.note(L + W / 2, T1 + 348, "the first raw file read of a session")

d.group(R, T1, W, H1, "The hook", 2)
col(R, T1, [("Before Grep or Bash|nudge: graphify query", "review"),
            ("Before Read or Glob|the same nudge", "review")], h=80, gap=32, arrows=False)
d.note(R + W / 2, T1 + 320, "only when a graph exists")

d.group(R, T2, W, H2, "Ask", 3)
grid(R, T2, [("query|a question", "coding"), ("path|from A to B", "coding"),
             ("explain|one concept", "coding"), ("MCP server|mcp extra", "coding")])
d.note(R + W / 2, T2 + 300, "MCP: one person on stdio,")
d.note(R + W / 2, T2 + 328, "a team on HTTP")

d.group(L, T2, W, H2, "The answer", 4)
col(L, T2, [("Find matching nodes|then walk out, BFS or DFS", "coding")], h=80)
d.pill(L + 126, T2 + 196, 300, 52, "a small subgraph", "front")
d.arrow(f"M{L + W / 2} {T2 + 144}V{T2 + 194}")
d.note(L + W / 2, T2 + 300, "about 2,000 tokens by default,")
d.note(L + W / 2, T2 + 328, "not whole files")

handoffs("hook", "graphify query", "graph.json")
d.save(Path(__file__).with_name("use.svg"))
