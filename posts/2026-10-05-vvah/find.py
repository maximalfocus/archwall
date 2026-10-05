"""VVAH phase 1: find where to look (auto-exclude, S0-S3).  Drawn from the community fork
maximalfocus/visa-vulnerability-agentic-harness (docs/architecture.md, docs/features.md,
vvaharness/orchestrator/scan.py for stage order, vvaharness/pipeline/stages/s*.py, commit 1c292e3).
Run: python3 find.py

Snake order: 1 inputs (top left) -> 2 map the code (top right) -> 3 threat model (bottom right)
-> 4 split the work (bottom left)."""
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

d = Diagram("VVAH phase 1: find where to look",
            "1 What goes in: your repo, plus optional files: known CVEs, design controls and a CMDB export. "
            "Missing files just mean less context; the CMDB is used when scoring the report. "
            "2 Map the code: an AI pass drops non-production files, S0 builds a static code map of where input "
            "reaches risky calls (in the default profile an AI helps label it), and S1 an AI explorer surveys the "
            "repo with read-only tools. "
            "3 Threat model, S2: assets worth protecting, trust boundaries where outsiders get in, and ranked "
            "threats; known CVEs raise a threat's likelihood. "
            "4 Split the work, S3: risk chunks, taint chunks, specialist chunks for 11 lenses, catch-all chunks "
            "for files no lens claimed, and threat chunks. Ten of the eleven lenses need their surface; logic-bug always runs.")

d.group(L, T1, W, H1, "What goes in", 1)
grid(L, T1, [("Your repo|code to scan", "data"), ("Known CVEs|optional", "data"),
             ("Design controls|optional", "data"), ("CMDB export|optional", "data")])
d.note(L + W / 2, T1 + 300, "missing files just mean less context")
d.note(L + W / 2, T1 + 328, "CMDB is used when scoring the report")

d.group(R, T1, W, H1, "Map the code", 2)
col(R, T1, [("Skip the noise|AI drops non-production files", "review"),
            ("S0 static code map|where input reaches risky calls", "coding"),
            ("S1 repo survey|AI explorer, read-only tools", "coding")])
d.note(R + W / 2, T1 + 380, "default profile: AI helps label the map")

d.group(R, T2, W, H2, "Threat model: S2", 3)
col(R, T2, [("Assets|what is worth protecting", "data"),
            ("Trust boundaries|where outsiders get in", "data"),
            ("Threats|tagged and ranked (STRIDE)", "plan")], arrows=False)
d.note(R + W / 2, T2 + 370, "known CVEs raise a threat's likelihood")

d.group(L, T2, W, H2, "Split the work: S3", 4)
grid(L, T2, [("Risk chunks|high-risk areas", "plan"), ("Taint chunks|input → risky call", "plan"),
             ("Specialist chunks|11 lenses", "plan"), ("Catch-all chunks|files no lens took", "plan"),
             ("Threat chunks|from the model", "plan")], h=72, gap=14)
d.note(L + W / 2, T2 + 342, "ten lenses need their surface")
d.note(L + W / 2, T2 + 368, "in the code; logic-bug always runs")

handoffs("repo", "context package", "threats")
d.note(600, 888, "Each step hands the next a typed file: ContextPackage → ThreatModel → TaskManifest")

d.save(Path(__file__).with_name("find.svg"))
