"""graphify: keep the graph current and share it.  Drawn from the graphify repo
(https://github.com/Graphify-Labs/graphify, README.md "Team setup" and "Recommended workflow";
graphify/hooks.py (post-commit and post-checkout hooks, detached background rebuild, "code only",
merge driver for graph.json); graphify/watch.py watch() (code: rebuild now, docs: needs_update flag);
README.md "Shared HTTP server"; pyproject.toml extras watch, mcp; commit 35adf43).
Run: python3 current.py

Snake order: 1 set up once (top left) -> 2 by itself (top right) -> 3 you run it (bottom right)
-> 4 share with the team (bottom left)."""
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


def handoffs(a, b, c, ya=T1 + 206, yc=T2 + 200):
    """Arrows between the four groups in snake order, with what each one carries."""
    if a:
        d.arrow(f"M{L + W} {ya}H{R - 2}", label=a, at=(600, ya - 12))
    if b:
        d.arrow(f"M{R + W / 2} {T1 + H1}V{T2 - 2}", label=b, at=(R + W / 2 + 14 + len(b) * 4.6, T1 + H1 + 21))
    if c:
        d.arrow(f"M{R} {yc}H{L + W + 2}", label=c, at=(600, yc - 12))


d = Diagram("graphify: keep it current, share it",
            "1 Set up once per clone: graphify hook install adds a post-commit hook, a post-checkout hook and a "
            "git merge driver for graph.json. "
            "2 By itself: every git commit and every branch switch rebuilds the code part in the background, "
            "AST only, no API cost. "
            "3 You run it: after git pull or merge, graphify update; when docs or papers change, /graphify "
            "--update, which uses the LLM. With the watch extra, graphify watch rebuilds code at once and flags "
            "doc changes for --update. "
            "4 Share with the team: commit graph.json and GRAPH_REPORT.md; the merge driver keeps conflict "
            "markers out of graph.json; or serve one graph over HTTP for everyone, with an API key when it is "
            "open beyond localhost.")

d.group(L, T1, W, H1, "Set up once", 1)
col(L, T1, [("graphify hook install|once per clone", "plan"),
            ("Commit + checkout hooks|and a merge driver", "data")], h=80, gap=40)

d.group(R, T1, W, H1, "By itself", 2)
col(R, T1, [("git commit|rebuilds the code part", "coding"),
            ("git switch, checkout|rebuilds the code part", "coding")], h=80, gap=32, arrows=False)
d.note(R + W / 2, T1 + 320, "in the background,")
d.note(R + W / 2, T1 + 348, "AST only, no API cost")

d.group(R, T2, W, H2, "You run it", 3)
col(R, T2, [("After git pull|graphify update .", "coding"),
            ("Docs changed|/graphify --update (LLM)", "coding")], h=80, gap=32, arrows=False)
d.note(R + W / 2, T2 + 300, "watch extra: graphify watch rebuilds")
d.note(R + W / 2, T2 + 328, "code at once, flags doc changes")

d.group(L, T2, W, H2, "Share with the team", 4)
col(L, T2, [("Commit graph.json|and GRAPH_REPORT.md", "write"),
            ("Or one HTTP MCP server|one URL, API key", "coding")], h=80, gap=32, arrows=False)
d.note(L + W / 2, T2 + 300, "the merge driver keeps conflict")
d.note(L + W / 2, T2 + 328, "markers out of graph.json")

handoffs("hooks", "git pull", "graph.json")
d.save(Path(__file__).with_name("current.svg"))
