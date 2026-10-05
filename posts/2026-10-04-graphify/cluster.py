"""graphify step 3: build the map and write the outputs.  Drawn from the graphify repo
(https://github.com/Graphify-Labs/graphify, graphify/build.py build() with dedup on by default and
--dedup-llm tiebreaker; graphify/dedup.py; graphify/cluster.py (Leiden via graspologic, Louvain fallback,
low-cohesion re-split, label_communities_by_hub); graphify/analyze.py god_nodes top_n=10,
surprising_connections top_n=5, suggest_questions top_n=7, find_import_cycles; graphify/skill.md Steps
4-6b (html community view over 5000 nodes, exports only on their flags, shrink guard); README.md
"Common commands"; pyproject.toml extras leiden, svg, neo4j; commit 35adf43).  Run: python3 cluster.py

Snake order: 1 one graph (top left) -> 2 communities (top right) -> 3 what matters (bottom right)
-> 4 graphify-out (bottom left)."""
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


d = Diagram("graphify step 3: build the map",
            "1 One graph: build() merges the code pass and the LLM pass into one NetworkX graph, then drops "
            "duplicates, the same thing found under two names; --dedup-llm lets an LLM settle close calls. "
            "2 Communities: Leiden groups nodes that link a lot (leiden extra; otherwise Louvain from NetworkX). "
            "Weak, loose groups are split again. Each one is named after its busiest node, or by an LLM. "
            "No embeddings, no vector store. "
            "3 What matters: the 10 most linked nodes (god nodes), the 5 most surprising cross-file links, up "
            "to 7 suggested questions, and import cycles. "
            "4 graphify-out: graph.json, graph.html (a community view above 5,000 nodes), GRAPH_REPORT.md, and "
            "exports only on a flag: Obsidian, wiki, SVG (svg extra), GraphML, Neo4j. A rebuild will not "
            "overwrite a bigger graph without --force.")

d.group(L, T1, W, H1, "One graph", 1)
col(L, T1, [("Merge|code pass + LLM pass", "write"),
            ("Drop duplicates|same thing, two names", "review")], h=80, gap=40)
d.note(L + W / 2, T1 + 330, "--dedup-llm: an LLM settles close calls")

d.group(R, T1, W, H1, "Communities", 2)
col(R, T1, [("Leiden (leiden extra)|else Louvain", "plan"),
            ("Split loose groups|low cohesion: split again", "plan"),
            ("Name each one|busiest node, or an LLM", "plan")])
d.note(R + W / 2, T1 + 388, "no embeddings, no vector store")

d.group(R, T2, W, H2, "What matters", 3)
grid(R, T2, [("God nodes|top 10 most linked", "critic"), ("Surprises|top 5 cross-file", "critic"),
             ("Questions|up to 7 to ask", "critic"), ("Import cycles", "critic")])

d.group(L, T2, W, H2, "graphify-out/", 4)
grid(L, T2, [("graph.json|the full graph", "write"), ("graph.html|click, filter, search", "write"),
             ("GRAPH_REPORT.md|the highlights", "write"), ("Exports on a flag|Obsidian, wiki, SVG…", "write")])
d.note(L + W / 2, T2 + 300, "a rebuild won't overwrite a bigger graph")
d.note(L + W / 2, T2 + 328, "unless you pass --force")

handoffs("graph", "communities", "report")
d.save(Path(__file__).with_name("cluster.svg"))
