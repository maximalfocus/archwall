"""ScientistTwo: the one pattern every stage uses.  Drawn from Listing 1 and Table 1 of the paper
(arXiv:2609.19644v1, 17 Sep 2026, read 2026-10-05): each stage makes a candidate with a specialist
agent, a critic accepts, rejects or asks for a refinement, and refinement loops up to a round limit.
Run: python3 pattern.py

Snake order: 1 make (top left) -> 2 judge (top right) -> 3 verdict (bottom right)
-> 4 refine (bottom left), which sends a new version back to the critic."""
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

d = Diagram("ScientistTwo: one pattern at every stage",
            "1 Make: a specialist agent makes a candidate, such as limitations, ideas, code and results, "
            "or a draft. 2 Judge: a critic agent asks a stage-specific question, such as is it new, or is it "
            "better than the baseline, and answers accept, refine or reject. 3 Verdict: accept moves the "
            "candidate on to the next stage; reject drops it. 4 Refine: a refine agent fixes the candidate "
            "using the critic's notes and sends the new version back to the critic. Every loop has a round "
            "limit. From Listing 1 and Table 1 of the paper.")

d.group(L, T1, W, H1, "Make", 1)
full(L, T1 + 72, "Specialist agent|makes a candidate", "plan")
pair(L, T1 + 200, ("Ideas or|limitations", "data"), ("Code and|results", "data"))
d.card(L + 154, T1 + 296, "A draft|paper", "data", w=HW, h=72)

d.group(R, T1, W, H1, "Judge", 2)
full(R, T1 + 72, "Critic agent|accept, refine or reject", "critic")
notes(R, T1, H1, "asks one question per stage,", "e.g. is it new? is it better?")

d.group(R, T2, W, H2, "Verdict", 3)
pair(R, T2 + 72, ("Accept|next stage", "plan"), ("Reject|dropped", "data"), h=80)
d.ok(R + 242, T2 + 86)
d.bad(R + 490, T2 + 86)
notes(R, T2, H2, "same rule from idea to paper")

d.group(L, T2, W, H2, "Refine", 4)
full(L, T2 + 72, "Refine agent|fixes it from the notes", "coding")
notes(L, T2, H2, "every loop has a round limit")

across(T1 + 108, "output")
d.arrow(f"M{R} {T1 + 330}H{(L + W + R) / 2}V{T2 + 108}H{L + W + 2}", label="refine", at=((L + W + R) / 2, T1 + 318))
drop(R + W / 2, "accept / reject")
drop(L + W / 2, "new version", back=True, up=True)
d.save(Path(__file__).with_name("pattern.svg"))
