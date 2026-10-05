"""ScientistTwo stage 3: ablation, find what really helps.  Drawn from section 3.4, Figure 7 and
appendix A.2 of the paper (arXiv:2609.19644v1, 17 Sep 2026, read 2026-10-05).
Run: python3 ablation.py

Snake order: 1 plan (top left) -> 2 run (top right) -> 3 judge (bottom right)
-> 4 refine (bottom left), which sends a better version back to planning."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

L, R, W = 24, 636, 540
T1, H1 = 16, 412
T2, H2 = 460, 400
FW, HW = 480, 232   # full-width card, half-width card


def full(x, y, label, kind=None, h=72):
    d.card(x + 30, y, label, kind, w=FW, h=h)


def pair(x, y, a, b, h=72):
    """Two half-width cards side by side; a and b are (label, kind)."""
    d.card(x + 30, y, a[0], a[1], w=HW, h=h)
    d.card(x + 278, y, b[0], b[1], w=HW, h=h)


def down(x, y0, y1):
    d.arrow(f"M{x} {y0}V{y1 - 2}")


def notes(x, top, h, *lines):
    """At most two note lines near the bottom of a group."""
    for i, s in enumerate(lines):
        d.note(x + W / 2, top + h - 70 + i * 28 + (14 if len(lines) == 1 else 0), s)


def across(y, label, back=False, rtl=False):
    """Arrow across the column gap at height y; rtl runs right group -> left group."""
    a, b = (R, L + W + 2) if rtl else (L + W, R - 2)
    d.arrow(f"M{a} {y}H{b}", back=back, label=label, at=((L + W + R) / 2, y - 12))


def drop(x, label, back=False, up=False):
    """Arrow across the row gap at x, label to its right; up runs bottom row -> top row."""
    a, b = (T2, T1 + H1 + 2) if up else (T1 + H1, T2 - 2)
    d.arrow(f"M{x} {a}V{b}", back=back, label=label, at=(x + 16 + len(label) * 4.6, T1 + H1 + 26))

d = Diagram("ScientistTwo stage 3: ablation",
            "1 Plan: an Ablation Planner takes the best idea, its results and code, and writes plans that each "
            "take out or change one part. 2 Run: an Ablation Coder runs every plan on the code, one result "
            "per part. 3 Judge: an Ablation Critic asks whether the breakdown is clean; if it is, the idea "
            "goes on to writing. 4 Refine: otherwise a Full-Set Engineer revises the method, and a Result "
            "Comparison agent keeps the new version only if it beats the old one; then the ablation runs "
            "again. In the paper's setting this refinement happens at most once.")

d.group(L, T1, W, H1, "Plan", 1)
full(L, T1 + 72, "Best idea|results + code", "data")
full(L, T1 + 200, "Ablation planner|one plan per part", "plan")
down(L + W / 2, T1 + 144, T1 + 200)

d.group(R, T1, W, H1, "Run", 2)
full(R, T1 + 200, "Ablation coder|runs every plan", "coding")
notes(R, T1, H1, "which part brings the gain?")

d.group(R, T2, W, H2, "Judge", 3)
full(R, T2 + 72, "Ablation critic|is the breakdown clean?", "critic")
pair(R, T2 + 184, ("Not yet|refine it", "data"), ("Clean|on to writing", "plan"))
d.ok(R + 490, T2 + 198)
down(R + 146, T2 + 144, T2 + 184)
down(R + 394, T2 + 144, T2 + 184)

d.group(L, T2, W, H2, "Refine", 4)
full(L, T2 + 72, "Full-set engineer|revises the method", "coding")
full(L, T2 + 184, "Result compare|better than before?", "critic")
down(L + W / 2, T2 + 144, T2 + 184)
notes(L, T2, H2, "worse: keep the old one", "at most once in the paper")

across(T1 + 236, "plans")
drop(R + W / 2, "results")
across(T2 + 220, "refine", rtl=True)
drop(L + W / 2, "better", back=True, up=True)
d.save(Path(__file__).with_name("ablation.svg"))
