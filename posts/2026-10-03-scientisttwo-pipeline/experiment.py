"""ScientistTwo stage 2: testing one idea, small data first.  Drawn from section 3.2, Figure 5 and
appendix A.2 of the paper (arXiv:2609.19644v1, 17 Sep 2026, read 2026-10-05).
Run: python3 experiment.py

Snake order: 1 baseline (top left) -> 2 try on a slice (top right) -> 3 verdict (bottom right)
-> 4 full benchmark (bottom left)."""
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

d = Diagram("ScientistTwo stage 2: test an idea, small first",
            "1 Baseline: a Baseline Coder reruns the best paper's main experiments on a slice of the benchmark, "
            "giving baseline results and code. 2 Try on a slice: a Subset Coder builds the idea by changing "
            "that code, and a Subset Critic compares the results with the baseline. 3 Verdict: good means "
            "scale up; bad means the idea is dropped; engineer means it shows promise and a Subset Engineer "
            "tunes it, for at most 2 rounds, after which it counts as bad. 4 Full benchmark: a Full-Set Coder "
            "runs the idea on every dataset, and a Full-Set Critic and Engineer do the final check. Out come "
            "the code, the results, good or bad, and lessons for the next round.")

d.group(L, T1, W, H1, "Baseline", 1)
full(L, T1 + 72, "Baseline coder|reruns the best paper", "coding")
full(L, T1 + 200, "Baseline result|on the small slice", "data")
down(L + W / 2, T1 + 144, T1 + 200)
notes(L, T1, H1, "a slice of the benchmark first,", "to save compute")

d.group(R, T1, W, H1, "Try on a slice", 2)
full(R, T1 + 72, "Subset coder|builds the idea", "coding")
full(R, T1 + 200, "Subset critic|better than baseline?", "critic")
down(R + W / 2, T1 + 144, T1 + 200)

d.group(R, T2, W, H2, "Verdict", 3)
pair(R, T2 + 64, ("Good|scale up", "plan"), ("Bad|dropped", "data"))
d.ok(R + 242, T2 + 78)
d.bad(R + 490, T2 + 78)
full(R, T2 + 160, "Engineer|tune it, at most 2 rounds", "coding")
notes(R, T2, H2, "still not good after that:", "counted as bad")

d.group(L, T2, W, H2, "Full benchmark", 4)
full(L, T2 + 72, "Full-set coder|runs every dataset", "coding")
full(L, T2 + 184, "Full-set critic|and engineer: final check", "critic")
down(L + W / 2, T2 + 144, T2 + 184)
notes(L, T2, H2, "out: code, results,", "good or bad, lessons")

across(T1 + 108, "baseline")
drop(R + W * 0.3, "verdict")
d.arrow(f"M{R + 510} {T2 + 196}H{R + 525}V{T1 + H1 + 2}", back=True, label="tuned", at=(R + 485, T1 + H1 + 26))
across(T2 + 100, "good", rtl=True)
d.save(Path(__file__).with_name("experiment.svg"))
