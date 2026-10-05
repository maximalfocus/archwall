"""ScientistTwo stage 2, outer loop: evolve ideas and pick the best.  Drawn from section 3.3,
Figure 6 and appendix A.2 of the paper (arXiv:2609.19644v1, 17 Sep 2026, read 2026-10-05).
Run: python3 evolve.py

Snake order: 1 traces (top left) -> 2 evolve (top right) -> 3 test (bottom right)
-> 4 pick the best (bottom left); test results update the traces."""
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

d = Diagram("ScientistTwo stage 2: evolve ideas, pick the best",
            "1 Traces: every idea tried so far, with what worked and what failed. 2 Evolve: an Idea Evolver "
            "reads the traces and writes new ideas; to avoid getting stuck it also takes the next untried "
            "seed idea by novelty; each round tests one of each. 3 Test: the implementer from the previous "
            "diagram runs each idea, and the results go back into the traces; up to 4 rounds, stopping early "
            "at 4 good ideas. 4 Pick the best: a Selector compares the good ideas on the full benchmark and "
            "picks one, with its results and code. If no idea is good after the last round, the whole run "
            "stops.")

d.group(L, T1, W, H1, "Traces", 1)
full(L, T1 + 72, "Execution traces|every idea tried so far", "data")
pair(L, T1 + 200, ("Good ideas|what worked", "data"), ("Bad ideas|what failed", "data"))
d.ok(L + 242, T1 + 214)
d.bad(L + 490, T1 + 214)

d.group(R, T1, W, H1, "Evolve", 2)
full(R, T1 + 72, "Idea evolver|writes better ideas", "plan")
full(R, T1 + 200, "Next seed idea|untried, by novelty", "data")
notes(R, T1, H1, "each round tests 2 ideas:", "1 evolved + 1 seed")

d.group(R, T2, W, H2, "Test", 3)
full(R, T2 + 72, "Implementer|slice first, then full", "coding")
notes(R, T2, H2, "up to 4 rounds, stops early", "once 4 ideas are good")

d.group(L, T2, W, H2, "Pick the best", 4)
full(L, T2 + 72, "Selector|picks the best good idea", "critic")
full(L, T2 + 184, "No good idea?|the whole run stops", "data")
d.bad(L + 490, T2 + 198)
notes(L, T2, H2, "out: best idea,", "its results and code")

across(T1 + 108, "traces")
drop(R + W / 2, "2 ideas")
across(T2 + 108, "good", rtl=True)
d.arrow(f"M{R + 90} {T2}V{T2 - 16}H{L + W - 90}V{T1 + H1 + 2}", back=True)
d.text((L + W + R) / 2, T2 - 22, "results", "al")
d.save(Path(__file__).with_name("evolve.svg"))
