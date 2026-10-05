"""ScientistTwo stage 5: meta-review, the last gate.  Drawn from section 3.6, Figure 7 and appendix
A.2 of the paper (arXiv:2609.19644v1, 17 Sep 2026, read 2026-10-05).
Run: python3 metareview.py

Snake order: 1 meta-review (top left) -> 2 revise the idea (top right) -> 3 compare (bottom right)
-> 4 redo (bottom left), which sends a new paper back to the meta-reviewer."""
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

d = Diagram("ScientistTwo stage 5: meta-review",
            "1 Meta-review: a Meta-Reviewer reads the paper and its review and decides accept or refine. "
            "Accept ends the run with the final paper and its code. 2 Revise the idea: on refine, a Full-Set "
            "Engineer changes the idea itself, guided by the meta-review. 3 Compare: a Result Comparison agent "
            "checks the new results against the old; if they are not better, the change is thrown away and "
            "the previous paper ships. 4 Redo: if better, the ablation, the draft and the review run again "
            "and the new paper returns to the meta-reviewer. In the paper's setting this happens at most once.")

d.group(L, T1, W, H1, "Meta-review", 1)
full(L, T1 + 72, "Meta-reviewer|meets the venue bar?", "review")
full(L, T1 + 200, "Accept|final paper + code", "plan")
d.ok(L + 490, T1 + 214)
down(L + W / 2, T1 + 144, T1 + 200)

d.group(R, T1, W, H1, "Revise the idea", 2)
full(R, T1 + 200, "Full-set engineer|changes the idea itself", "coding")
notes(R, T1, H1, "guided by the meta-review")

d.group(R, T2, W, H2, "Compare", 3)
full(R, T2 + 72, "Result compare|better than before?", "critic")
full(R, T2 + 184, "Not better|ship the previous paper", "data")
d.bad(R + 490, T2 + 198)
down(R + W / 2, T2 + 144, T2 + 184)

d.group(L, T2, W, H2, "Redo", 4)
full(L, T2 + 72, "Ablation, draft|and review again", "coding")
notes(L, T2, H2, "at most once in the paper")

across(T1 + 108, "refine")
drop(R + W / 2, "new results")
across(T2 + 108, "better", rtl=True)
drop(L + W / 2, "new paper", back=True, up=True)
d.save(Path(__file__).with_name("metareview.svg"))
