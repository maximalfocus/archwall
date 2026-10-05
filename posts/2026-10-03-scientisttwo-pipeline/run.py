"""ScientistTwo: models, time and cost.  Drawn from section 4 ("Common Setup", "Generalizability
Across Coding Agents", "Cost Analysis"), Figure 10, Table 8 and appendix A.2 of the paper
(arXiv:2609.19644v1, 17 Sep 2026, read 2026-10-05).  Figure 10's caption says 2.5 days on average,
the text 2-3 days; the cost is $3,765 in the text and "approximately $3,800" in Limitations.
Run: python3 run.py

Snake order: 1 models (top left) -> 2 swap the coder (top right) -> 3 time (bottom right)
-> 4 cost (bottom left).  Side by side, not a flow."""
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

d = Diagram("ScientistTwo: models, time and cost",
            "1 Models: Gemini 3.6 Flash runs most agents; the idea experiment coder, the ablation agent, the "
            "rebuttal agent and the draft enhancer use Claude Code with Opus 4.8. 2 Swap the coder: on 5 "
            "ICLR 2026 tasks Claude Code was replaced with Antigravity on Gemini 3.8 Flash, and it still found "
            "new best methods. 3 Time: about 2 to 3 days per problem, most of it in idea refinement and the "
            "review loops, where code runs on benchmarks. 4 Cost: $3,765 per problem on average, tokens plus "
            "virtual machines, measured on 33 NeurIPS 2025 problems.")

d.group(L, T1, W, H1, "Models", 1)
full(L, T1 + 72, "Gemini 3.6 Flash|most agents")
full(L, T1 + 184, "Claude Code, Opus 4.8|four named agents", "coding")
notes(L, T1, H1, "experiment coder, ablation,", "rebuttal, draft enhancer")

d.group(R, T1, W, H1, "Swap the coder", 2)
full(R, T1 + 72, "Antigravity|on Gemini 3.8 Flash", "coding")
notes(R, T1, H1, "tried on 5 ICLR 2026 tasks,", "still found new best methods")

d.group(R, T2, W, H2, "Time", 3)
full(R, T2 + 72, "2 to 3 days|per problem", "data")
notes(R, T2, H2, "most of it: idea refinement", "and the review loops")

d.group(L, T2, W, H2, "Cost", 4)
full(L, T2 + 72, "$3,765 on average|tokens + virtual machines", "data")
notes(L, T2, H2, "measured on 33 NeurIPS 2025", "problems")
d.save(Path(__file__).with_name("run.svg"))
