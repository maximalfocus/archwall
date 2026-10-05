"""ScientistTwo overview: six agent groups in one closed loop.  Redrawn from the System overview
figure on https://scientist-two.github.io/#overview and section 3 of the paper
(arXiv:2609.19644v1, 17 Sep 2026, read 2026-10-05).
Run: python3 diagram.py

Snake order, three rows: 1 ideas (top left) -> 2 experiments (top right) -> 3 ablation (middle right)
-> 4 writer (middle left) -> 5 peer review (bottom left) -> 6 meta-review (bottom right).
Experiment results feed back to the ideas; review sends the draft back to the writer;
the meta-review can send the idea back to step 3."""
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

d = Diagram("ScientistTwo closed-loop research pipeline",
            "Input: a research problem with the current best paper and its code. 1 Ideas: find what the best "
            "method gets wrong and write new ideas, checked for novelty. 2 Experiments: a coding agent and a "
            "critic test each idea on a slice of the benchmark, then on all of it; results go back to evolve "
            "better ideas. 3 Ablation: take the best idea apart to see which parts help, and refine it. "
            "4 Writer: draft the paper and improve it. 5 Peer review: an AI reviewer scores it and a rebuttal "
            "agent answers with new experiments; the writer revises the draft. 6 Meta-review: accept, giving the final paper and code, or "
            "send the idea back to step 3 for one more fix.")

GH = 236
Y1, Y2, Y3 = 80, 364, 648
d.pill(L, 16, W * 2 + (R - L - W), 44, "Input: a research problem + the current best paper and its code")
d.arrow(f"M{L + W / 2} 60V{Y1 - 2}")


def stage(x, y, n, title, a, b, note=None):
    d.group(x, y, W, GH, title, n)
    pair(x, y + 64, a, b)
    if note:
        d.note(x + W / 2, y + GH - 30, note)


stage(L, Y1, 1, "Ideas", ("Limitation|finder", "plan"), ("Novelty|checker", "critic"), "seed ideas, most novel first")
stage(R, Y1, 2, "Experiments", ("Coding|agent", "coding"), ("Critic|agent", "critic"), "small slice first, then all data")
stage(R, Y2, 3, "Ablation", ("Ablation|study", "coding"), ("Ablation|critic", "critic"), "keep only the parts that help")
stage(L, Y2, 4, "Writer", ("Initial|drafter", "write"), ("Draft|enhancer", "write"), "a full paper")
stage(L, Y3, 5, "Peer review", ("Reviewer|scores 1-10", "review"), ("Rebuttal|new experiments", "coding"), "below 8: rebut, at most 2 rounds")
stage(R, Y3, 6, "Meta-review", ("Meta-|reviewer", "review"), ("Final paper|+ code", "plan"), "accept, or refine the idea once")
d.ok(R + 490, Y3 + 78)

mid = (L + W + R) / 2
across(Y1 + 84, "ideas")
across(Y1 + 160, "results", back=True, rtl=True)
d.arrow(f"M{R + W / 2} {Y1 + GH}V{Y2 - 2}", label="best idea", at=(R + W / 2 + 60, Y1 + GH + 30))
across(Y2 + 100, "idea", rtl=True)
d.arrow(f"M{L + W / 2} {Y2 + GH}V{Y3 - 2}", label="draft", at=(L + W / 2 + 40, Y2 + GH + 30))
d.arrow(f"M{L + 440} {Y3}V{Y2 + GH + 2}", back=True, label="revise", at=(L + 400, Y2 + GH + 30))
across(Y3 + 100, "paper")
d.arrow(f"M{R + 60} {Y3}V{Y2 + GH + 2}", back=True, label="refine", at=(R + 110, Y2 + GH + 30))
d.save(Path(__file__).with_name("diagram.svg"))
