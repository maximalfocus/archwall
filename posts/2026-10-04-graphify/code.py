"""graphify step 2a: the code pass, on your machine.  Drawn from the graphify repo
(https://github.com/Graphify-Labs/graphify, docs/how-it-works.md "Pass 1", "Parallel extraction",
"SHA256 cache"; ARCHITECTURE.md "Adding a new language extractor"; graphify/extract.py: call-graph pass
with confidence EXTRACTED 1.0 when type-qualified else INFERRED 0.85, _RATIONALE_PREFIXES,
ProcessPoolExecutor; graphify/cache.py file_hash (sha256); pyproject.toml extras sql, terraform, ocaml;
commit 35adf43).  Run: python3 code.py

Snake order: 1 parse (top left) -> 2 what it finds (top right) -> 3 link across files (bottom right)
-> 4 cache and hand over (bottom left)."""
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


d = Diagram("graphify step 2a: the code pass",
            "1 Parse: tree-sitter reads each code file on your machine, with no LLM and no cost, many files at "
            "once on all CPU cores. A few languages need an extra, for example SQL, Terraform or OCaml. "
            "2 What it finds: classes and functions, imports, calls, comments that explain the code such as "
            "# NOTE: and # WHY:, SQL tables and joins, and package manifests. "
            "3 Link across files: a second pass resolves calls between files. A call it can pin down exactly is "
            "EXTRACTED with score 1.0; a best guess by name is INFERRED with score 0.85. "
            "4 Cache and hand over: each file is fingerprinted with SHA256 so an unchanged file is skipped next "
            "time; the nodes and edges join the LLM pass output. A code-only folder needs no API key.")

d.group(L, T1, W, H1, "Parse", 1)
col(L, T1, [("tree-sitter|one grammar per language", "coding"),
            ("All CPU cores|many files at once", "coding")], h=80, gap=32)
d.note(L + W / 2, T1 + 320, "no LLM, nothing leaves the machine")
d.note(L + W / 2, T1 + 348, "SQL, Terraform, OCaml…: an extra each")

d.group(R, T1, W, H1, "What it finds", 2)
grid(R, T1, [("Classes, functions", "data"), ("Imports", "data"), ("Calls", "data"),
             ("Why-comments|# NOTE:, # WHY:", "data"), ("SQL tables, joins", "data"),
             ("Manifests|pyproject, go.mod", "data")], h=72, gap=14)

d.group(R, T2, W, H2, "Link across files", 3)
d.card(R + 30, T2 + 64, "Second pass|resolve calls between files", "coding", w=492, h=72)
d.card(R + 30, T2 + 196, "Exact match|EXTRACTED, 1.0", "plan", w=238, h=80)
d.card(R + 284, T2 + 196, "Best guess|INFERRED, 0.85", "critic", w=238, h=80)
d.arrow(f"M{R + 149} {T2 + 136}V{T2 + 194}")
d.arrow(f"M{R + 403} {T2 + 136}V{T2 + 194}")
d.note(R + W / 2, T2 + 330, "every edge carries its tag and score")

d.group(L, T2, W, H2, "Cache and hand over", 4)
col(L, T2, [("SHA256 per file|unchanged: skipped next time", "data"),
            ("Nodes + edges|merged with the LLM pass", "write")], h=80, gap=32)
d.note(L + W / 2, T2 + 330, "a code-only folder needs no API key")

handoffs("syntax trees", "symbols", "edges")
d.save(Path(__file__).with_name("code.svg"))
