"""ScientistTwo integrity: four checks that the paper matches its artifacts.  Drawn from section 4.2
("CoE Integrity Audit"), Table 7 of the paper (arXiv:2609.19644v1, 17 Sep 2026, read 2026-10-05)
and the Integrity section of https://scientist-two.github.io/.  The audit numbers are the full
system's row of Table 7 (49 papers, 1,814 references).
Run: python3 integrity.py

Snake order: 1 rerunnable (top left) -> 2 rules kept (top right) -> 3 real references (bottom right)
-> 4 method matches code (bottom left).  The four checks are side by side, not a flow."""
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

d = Diagram("ScientistTwo integrity checks",
            "Four properties, each with the agent that guards it and the audit result for the full system. "
            "1 Rerunnable: the Coding Agent is told to write self-contained scripts that can be rerun; every "
            "reported score reproduced, 49 of 49. 2 Rules kept: a validation filter uses the Coding Agent "
            "right after experiments to drop solutions that break the task rules or game the metric; 0 of 49 "
            "violated. 3 Real references: a search-backed model finds made-up citations and the Writer fixes "
            "the bibliography from live search; 0 of 1,814 references made up. 4 Method matches code: the "
            "Coding Agent audits the code against the paper and the Writer fixes the method section; 49 of 49 "
            "match.")

d.group(L, T1, W, H1, "Rerunnable", 1)
full(L, T1 + 72, "Coding agent|writes rerunnable scripts", "coding")
notes(L, T1, H1, "audit: every score reproduced,", "49 of 49 papers")

d.group(R, T1, W, H1, "Rules kept", 2)
full(R, T1 + 72, "Validation filter|drops rule-breaking code", "review")
notes(R, T1, H1, "runs right after experiments;", "audit: 0 of 49 broke rules")

d.group(R, T2, W, H2, "Real references", 3)
full(R, T2 + 72, "Search-backed model|finds made-up citations", "critic")
full(R, T2 + 184, "Writer|fixes the bibliography", "write")
down(R + W / 2, T2 + 144, T2 + 184)
notes(R, T2, H2, "audit: 0 of 1,814", "references made up")

d.group(L, T2, W, H2, "Method matches code", 4)
full(L, T2 + 72, "Coding agent|checks code against paper", "critic")
full(L, T2 + 184, "Writer|fixes the method section", "write")
down(L + W / 2, T2 + 144, T2 + 184)
notes(L, T2, H2, "audit: 49 of 49 match")
d.save(Path(__file__).with_name("integrity.svg"))
