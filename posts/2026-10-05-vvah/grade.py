"""VVAH phase 4b: grade the fix (S11, validate).  Drawn from the community fork
maximalfocus/visa-vulnerability-agentic-harness (docs/validation.md,
vvaharness/validation/constants/scoring.py for the weights, commit 1c292e3).  Run: python3 grade.py

Snake order: 1 find what to grade (top left) -> 2 review panel (top right) -> 3 four weighted
checks (bottom right) -> 4 verdict (bottom left)."""
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

d = Diagram("VVAH phase 4b: grade the fix",
            "1 Find what to grade: fix records under security-remediation/; a discover step with no AI picks the "
            "cases still open. It is off in the default scan; the validate command runs it any time. "
            "2 Review panel, read-only: an orchestrator runs the session, a security architect asks whether the "
            "root cause is fixed, and a penetration tester tries to get around the fix. A cross-repo reviewer "
            "joins only for fixes that span 2 or more repos. "
            "3 Four weighted checks: root cause 43 percent, every instance 25, no new bugs 19, best practice 14. "
            "4 Verdict: fixed at a score of 0.80 or more, partially fixed at 0.50 or more, not fixed below 0.50, "
            "or inconclusive when the reviewers split. If root cause or no new bugs fails, the best result is "
            "partially fixed. The case becomes validated, failed or open.")

d.group(L, T1, W, H1, "Find what to grade", 1)
col(L, T1, [("Fix records|security-remediation/", "data"),
            ("Discover|picks open cases, no AI", "review")], h=80)
d.note(L + W / 2, T1 + 300, "off in the default scan;")
d.note(L + W / 2, T1 + 328, "the validate command runs it any time")

d.group(R, T1, W, H1, "Review panel, read-only", 2)
d.card(R + 30, T1 + 64, "Orchestrator|runs the session", "plan", w=492, h=72)
d.card(R + 30, T1 + 176, "Security architect|root cause fixed?", "critic", w=238, h=80)
d.card(R + 284, T1 + 176, "Pen tester|can I still get in?", "critic", w=238, h=80)
d.arrow(f"M{R + 149} {T1 + 136}V{T1 + 174}")
d.arrow(f"M{R + 403} {T1 + 136}V{T1 + 174}")
d.note(R + W / 2, T1 + 310, "a cross-repo reviewer joins")
d.note(R + W / 2, T1 + 338, "only for fixes across 2+ repos")

d.group(R, T2, W, H2, "Four weighted checks", 3)
col(R, T2, [("Root cause · 43%", "critic"), ("Every instance · 25%", "critic"),
            ("No new bugs · 19%", "critic"), ("Best practice · 14%", "critic")], h=60, gap=14, arrows=False)

d.group(L, T2, W, H2, "Verdict", 4)
grid(L, T2, [("Fixed|score ≥ 0.80", "plan"), ("Partially fixed|score ≥ 0.50", "data"),
             ("Not fixed|score < 0.50", "data"), ("Inconclusive|reviewers split", "data")])
d.ok(L + 248, T2 + 78)
d.note(L + W / 2, T2 + 300, "root cause or new bugs fail →")
d.note(L + W / 2, T2 + 328, "at best partially fixed")

handoffs("one case", "votes per check", "score")
d.note(600, 888, "The case becomes validated, failed or open; failed and open can be graded again")
d.save(Path(__file__).with_name("grade.svg"))
