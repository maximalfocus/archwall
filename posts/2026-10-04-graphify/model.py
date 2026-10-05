"""graphify data model: what one node and one edge hold.  Drawn from the graphify repo
(https://github.com/Graphify-Labs/graphify, ARCHITECTURE.md "Extraction output schema" and "Confidence
labels"; docs/how-it-works.md "Confidence tagging" (INFERRED rubric 0.55-0.95) and "The graph format";
graphify/report.py "Ambiguous Edges - Review These"; graphify/skill.md Step 5 (community_name in
graph.json); commit 35adf43).  Run: python3 model.py

Snake order: 1 a node (top left) -> 2 an edge (top right) -> 3 how sure (bottom right)
-> 4 stored as (bottom left)."""
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


d = Diagram("graphify data model",
            "1 A node: an id and a readable label; a file type of code, document, paper, image, rationale or "
            "concept; "
            "and the source file and line it came from. "
            "2 An edge: a source and a target node, a relation such as calls, imports or uses, and a confidence "
            "tag. "
            "3 How sure: EXTRACTED means it is stated in the source, score 1.0; INFERRED is a reasonable guess "
            "with a score from 0.55 to 0.95; AMBIGUOUS is uncertain and listed in the report for a person to "
            "check. "
            "4 Stored as: graph.json in NetworkX node-link format; hyperedges link groups of three or more "
            "nodes; after clustering each node also carries its community.")

d.group(L, T1, W, H1, "A node", 1)
col(L, T1, [("id + label|a stable name", "data"),
            ("file_type|code, doc, paper, image, rationale, concept", "data"),
            ("source_file + line|where it came from", "data")], arrows=False)

d.group(R, T1, W, H1, "An edge", 2)
col(R, T1, [("source → target|two node ids", "data"),
            ("relation|calls, imports, uses…", "data"),
            ("confidence|a tag, plus a score", "data")], arrows=False)

d.group(R, T2, W, H2, "How sure", 3)
col(R, T2, [("EXTRACTED|stated in the source, 1.0", "plan"),
            ("INFERRED|a reasonable guess, 0.55–0.95", "critic"),
            ("AMBIGUOUS|unsure, flagged in the report", "review")], arrows=False)

d.group(L, T2, W, H2, "Stored as", 4)
col(L, T2, [("graph.json|NetworkX node-link format", "write"),
            ("Hyperedges|one link for 3 or more nodes", "data")], h=80, gap=32, arrows=False)
d.note(L + W / 2, T2 + 330, "after clustering, each node gets its community")

handoffs("node ids", "tagged", "graph")
d.save(Path(__file__).with_name("model.svg"))
