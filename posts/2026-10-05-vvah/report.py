"""VVAH phase 3: report (S7-S9).  Drawn from the community fork
maximalfocus/visa-vulnerability-agentic-harness (docs/architecture.md, docs/outputs.md,
vvaharness/pipeline/stages/s7_dedup.py, s8_chain.py, vvaharness/report/enrich.py, commit 1c292e3).
Run: python3 report.py

Snake order: 1 merge duplicates (top left) -> 2 chain (top right) -> 3 score and protect
(bottom right) -> 4 outputs (bottom left)."""
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

d = Diagram("VVAH phase 3: report",
            "1 Merge duplicates, S7: a rule pass joins findings in the same file, of the same type, on nearby lines; "
            "one AI call joins findings with the same root cause that one fix would close. "
            "2 Chain, S8: an AI sees all findings together, finds attack chains where small bugs combine, re-ranks "
            "by real exploitability, and checks combinations with known unpatched CVEs. "
            "3 Score and protect: CVSS 3.1 and CWE on every finding, optional business context from a CMDB export, "
            "MITRE ATT&CK candidate techniques as context that adds no finding, and secrets such as card numbers, "
            "SSNs and keys masked when the files are written. "
            "4 Outputs in security-scan/: report.md for people, report.sarif for tools, findings.json as typed "
            "data, and an optional upload to an ingest hub, the only path besides the AI provider that sends "
            "results off the machine.")

d.group(L, T1, W, H1, "Merge duplicates: S7", 1)
col(L, T1, [("Rule pass|same file, type, nearby line", "review"),
            ("AI pass|same root cause, one fix", "review")], h=80)
d.note(L + W / 2, T1 + 300, "fewer, cleaner findings")

d.group(R, T1, W, H1, "Chain: S8", 2)
col(R, T1, [("Find attack chains|small bugs that combine", "plan"),
            ("Re-rank|by real exploitability", "plan"),
            ("Known CVEs|check unpatched combos", "data")], arrows=False)

d.group(R, T2, W, H2, "Score and protect", 3)
grid(R, T2, [("CVSS 3.1 + CWE|severity, type", "critic"), ("Business context|CMDB, optional", "data"),
             ("ATT&CK|context only", "data"), ("Mask secrets|cards, SSNs, keys", "review")])
d.note(R + W / 2, T2 + 300, "ATT&CK adds no finding")
d.note(R + W / 2, T2 + 328, "and changes no score")

d.group(L, T2, W, H2, "Outputs: security-scan/", 4)
grid(L, T2, [("report.md|for people", "write"), ("report.sarif|for tools", "write"),
             ("findings.json|typed data", "write"), ("Upload|optional hub", "write")])
d.note(L + W / 2, T2 + 300, "besides the AI provider, the upload")
d.note(L + W / 2, T2 + 328, "is the only way results leave")

handoffs("unique", "final report", "S9")
d.save(Path(__file__).with_name("report.svg"))
