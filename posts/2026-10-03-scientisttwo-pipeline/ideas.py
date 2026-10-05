"""ScientistTwo stage 1: generating seed ideas.  Drawn from section 3.1, Figure 4 and appendix A.2
of the paper (arXiv:2609.19644v1, 17 Sep 2026, read 2026-10-05).
Run: python3 ideas.py

Snake order: 1 find limitations (top left) -> 2 check the list (top right)
-> 3 first idea (bottom right) -> 4 more ideas, ranked (bottom left)."""
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

d = Diagram("ScientistTwo stage 1: seed ideas",
            "1 Find limitations: the input is a research problem with the current best paper and its code; "
            "a Limitation Extractor lists what that method gets wrong. 2 Check the list: a Limitation "
            "Verifier asks whether the list is enough to guide an improvement; if not, the extractor adds "
            "what is missing, for at most 16 rounds. 3 First idea: an Initial Idea Generator writes one idea "
            "that targets the limitations, and a Novelty Checker scores how new it is against 2 reference "
            "papers found with Google Search. 4 More ideas: an Idea Generator keeps adding different, more "
            "novel ideas; the seed ideas are ranked by novelty so the most original are tried first.")

d.group(L, T1, W, H1, "Find limitations", 1)
full(L, T1 + 72, "Research problem|best paper + its code", "data")
full(L, T1 + 200, "Limitation|extractor", "plan")
down(L + W / 2, T1 + 144, T1 + 200)

d.group(R, T1, W, H1, "Check the list", 2)
full(R, T1 + 200, "Limitation verifier|enough to improve on?", "critic")
notes(R, T1, H1, "something missing? find more,", "at most 16 rounds")

d.group(R, T2, W, H2, "First idea", 3)
full(R, T2 + 72, "Initial idea|generator", "plan")
full(R, T2 + 184, "Novelty checker|scores how new it is", "critic")
down(R + W / 2, T2 + 144, T2 + 184)
notes(R, T2, H2, "compares with 2 papers", "found on Google Search")

d.group(L, T2, W, H2, "More ideas", 4)
full(L, T2 + 72, "Idea generator|adds newer, different ideas", "plan")
full(L, T2 + 184, "Seed ideas|ranked by novelty", "data")
down(L + W / 2, T2 + 144, T2 + 184)
notes(L, T2, H2, "the most original ones", "are tried first")

across(T1 + 222, "list")
across(T1 + 260, "more", back=True, rtl=True)
drop(R + W / 2, "full list")
across(T2 + 220, "idea", rtl=True)
d.save(Path(__file__).with_name("ideas.svg"))
