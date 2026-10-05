"""ScientistTwo: how it was tested.  Drawn from section 4.1, Tables 2 and 3, appendix A.1 of the
paper (arXiv:2609.19644v1, 17 Sep 2026, read 2026-10-05) and the Main Results table on
https://scientist-two.github.io/.
Run: python3 tested.py

Snake order: 1 test set (top left) -> 2 beat the best (top right) -> 3 AI reviewers (bottom right)
-> 4 compared with (bottom left)."""
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

d = Diagram("ScientistTwo: how it was tested",
            "1 Test set: 107 research problems, each the problem and code of an accepted paper: 38 from "
            "NeurIPS 2025, 5 from ICLR 2026 and 64 ICML 2026 spotlights. 2 Beat the best: it beat the human "
            "best result on 86 of the 107, 80.4 percent, with an average gain of 25.2 percent. 3 AI reviewers: "
            "ScholarPeer, which is also used inside the loop, rated its papers 7.5 out of 10 and accepted "
            "91.9 percent; the Stanford Agentic Reviewer, unseen during development, rated them 5.7 and "
            "accepted 72.1 percent. 4 Compared with: above the average accepted ICLR 2026 and NeurIPS 2025 "
            "paper under both reviewers, below ICML 2026 spotlights, and every other AI research agent "
            "got 0 percent acceptance from the Stanford reviewer.")

d.group(L, T1, W, H1, "Test set", 1)
full(L, T1 + 72, "NeurIPS 2025|38 accepted papers", "data")
full(L, T1 + 160, "ICLR 2026|5 accepted papers", "data")
full(L, T1 + 248, "ICML 2026|64 spotlight papers", "data")
notes(L, T1, H1, "107 problems, each with its code")

d.group(R, T1, W, H1, "Beat the best", 2)
full(R, T1 + 72, "86 of 107|beat the human best", "plan")
full(R, T1 + 184, "+25.2%|average gain", "plan")
notes(R, T1, H1, "80.4% success rate")

d.group(R, T2, W, H2, "AI reviewers", 3)
full(R, T2 + 72, "ScholarPeer|7.5 / 10, 91.9% accepted", "review")
full(R, T2 + 184, "Stanford Agentic Reviewer|5.7 / 10, 72.1% accepted", "review")
notes(R, T2, H2, "ScholarPeer is also used inside;", "Stanford was unseen in development")

d.group(L, T2, W, H2, "Compared with", 4)
full(L, T2 + 72, "Beats the average accepted|ICLR 2026, NeurIPS 2025 paper", "data")
full(L, T2 + 160, "Below the average|ICML 2026 spotlight", "data")
full(L, T2 + 248, "Every other AI agent|0% accepted by Stanford", "data")

across(T1 + 108, "results")
drop(R + W / 2, "86 papers")
across(T2 + 108, "scores", rtl=True)
d.save(Path(__file__).with_name("tested.svg"))
