"""graphify side tools: beyond one repo.  Drawn from the graphify repo
(https://github.com/Graphify-Labs/graphify, README.md "Full command reference"; graphify/global_graph.py
(~/.graphify/global-graph.json); graphify/prs.py (gh CLI, --conflicts, --triage via the first backend
with a key); graphify/reflect.py (deterministic, no LLM, reflections/LESSONS.md); graphify/callflow_html.py;
graphify/export.py to_cypher and the --neo4j-push / --falkordb-push flags; pyproject.toml extras neo4j,
falkordb; commit 35adf43).  Run: python3 more.py

Snake order: 1 many repos (top left) -> 2 pull requests (top right) -> 3 work memory (bottom right)
-> 4 other views (bottom left)."""
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


d = Diagram("graphify side tools",
            "1 Many repos: graphify global add registers a project graph in one cross-project graph under "
            "~/.graphify; merge-graphs joins two graph.json files. "
            "2 Pull requests: graphify prs shows open PRs with CI, reviews and worktrees through the gh tool; "
            "--conflicts lists PRs that touch the same communities; --triage has an LLM rank the review queue, "
            "using the first backend that is set up. "
            "3 Work memory: save-result records whether an answer was useful, a dead end or corrected; reflect "
            "turns those records into LESSONS.md, with no LLM. "
            "4 Other views: callflow-html draws a Mermaid call-flow page; --neo4j-push and --falkordb-push load "
            "the graph into a graph database (neo4j or falkordb extra).")

d.group(L, T1, W, H1, "Many repos", 1)
col(L, T1, [("graphify global add|one graph across projects", "write"),
            ("merge-graphs|join two graph.json files", "coding")], h=80, gap=32, arrows=False)
d.note(L + W / 2, T1 + 320, "kept in ~/.graphify/")

d.group(R, T1, W, H1, "Pull requests", 2)
col(R, T1, [("graphify prs|CI, reviews, worktrees (gh)", "data"),
            ("--conflicts|PRs in the same communities", "critic"),
            ("--triage|an LLM ranks the review queue", "critic")], arrows=False)

d.group(R, T2, W, H2, "Work memory", 3)
col(R, T2, [("save-result|useful, dead end, corrected", "data"),
            ("reflect|writes LESSONS.md, no LLM", "write")], h=80, gap=32)
d.note(R + W / 2, T2 + 300, "with --graph, query and explain show it")

d.group(L, T2, W, H2, "Other views", 4)
col(L, T2, [("callflow-html|a Mermaid call-flow page", "write"),
            ("Neo4j, FalkorDB push|neo4j or falkordb extra", "write")], h=80, gap=32, arrows=False)

d.save(Path(__file__).with_name("more.svg"))
