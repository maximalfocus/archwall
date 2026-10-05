"""ScientistTwo stages 4–5: write, review, rebut.  Drawn from section 3.5, Figure 7 and appendix A.2 of
the paper (arXiv:2609.19644v1, 17 Sep 2026, read 2026-10-05); the overview figure on
https://scientist-two.github.io/ names the enhancer "Draft Enhancer", section 3.5 "Paper Enhancer".
Run: python3 writing.py

Snake order: 1 draft (top left) -> 2 review (top right) -> 3 rebuttal (bottom right)
-> 4 revise (bottom left), which goes back to the reviewer."""
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

d = Diagram("ScientistTwo stages 4–5: write, review, rebut",
            "1 Draft: an Initial Drafter, built on PaperOrchestra, turns the best idea, its results and the "
            "ablations into a full paper in ICLR 2025 format. 2 Review: a Peer Reviewer, ScholarPeer, lists "
            "strengths, weaknesses and questions and gives a score from 1 to 10; 8 or more goes on to the "
            "meta-review. 3 Rebuttal: below 8, a Rebuttal Planner picks new experiments that answer the "
            "reviewer, and a Rebuttal Coder runs them. 4 Revise: a Draft Enhancer puts the new results, "
            "tables and figures into the paper and sends it back to the reviewer, for at most 2 review "
            "rounds.")

d.group(L, T1, W, H1, "Draft", 1)
full(L, T1 + 72, "Best idea, results|and ablations", "data")
full(L, T1 + 200, "Initial drafter|built on PaperOrchestra", "write")
down(L + W / 2, T1 + 144, T1 + 200)
notes(L, T1, H1, "a full paper,", "in ICLR 2025 format")

d.group(R, T1, W, H1, "Review", 2)
full(R, T1 + 200, "Peer reviewer|ScholarPeer, scores 1-10", "review")
notes(R, T1, H1, "8 or more: on to meta-review")

d.group(R, T2, W, H2, "Rebuttal", 3)
full(R, T2 + 72, "Rebuttal planner|picks new experiments", "plan")
full(R, T2 + 184, "Rebuttal coder|runs them", "coding")
down(R + W / 2, T2 + 144, T2 + 184)
notes(R, T2, H2, "answers with experiments,", "not just new wording")

d.group(L, T2, W, H2, "Revise", 4)
full(L, T2 + 72, "Draft enhancer|updates text, tables, figures", "write")
notes(L, T2, H2, "at most 2 review rounds")

across(T1 + 236, "draft")
drop(R + W / 2, "below 8")
across(T2 + 220, "results", rtl=True)
d.arrow(f"M{L + W - 90} {T2}V{T2 - 16}H{R + 90}V{T1 + H1 + 2}", back=True)
d.text((L + W + R) / 2, T2 - 22, "revised", "al")
d.save(Path(__file__).with_name("writing.svg"))
