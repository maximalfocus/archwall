"""VVAH phase 2: hunt and double-check (S4-S6).  Drawn from the community fork
maximalfocus/visa-vulnerability-agentic-harness (docs/features.md sections 2, 9, 10,
vvaharness/pipeline/stages/s4_deepdive.py, s5_prefilter.py, s6_verify.py, commit 1c292e3).
Run: python3 check.py

Snake order: 1 hunt (top left) -> 2 filter (top right) -> 3 prove it wrong (bottom right)
-> 4 optional live check (bottom left)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

L, R, W = 24, 624, 552
T1, H1 = 16, 412
T2, H2 = 460, 400


def col(x, top, cards, h=72, gap=24, arrows=True):
    """One column of wide cards, top to bottom, optionally joined by arrows."""
    for i, (lbl, kind) in enumerate(cards):
        y = top + 64 + i * (h + gap)
        d.card(x + 30, y, lbl, kind, w=492, h=h)
        if arrows and i:
            d.arrow(f"M{x + W / 2} {y - gap}V{y - 2}")


def grid(x, top, cards, h=80, gap=16, y0=64):
    """Two columns of cards, filled row by row."""
    for i, (lbl, kind) in enumerate(cards):
        d.card(x + 30 + (i % 2) * 254, top + y0 + (i // 2) * (h + gap), lbl, kind, w=238, h=h)


def handoffs(a, b, c, ya=T1 + 206, yc=T2 + 200):
    """Arrows between the four groups in snake order, with what each one carries."""
    if a:
        d.arrow(f"M{L + W} {ya}H{R - 2}", label=a, at=(600, ya - 12))
    if b:
        d.arrow(f"M{R + W / 2} {T1 + H1}V{T2 - 2}", label=b, at=(R + W / 2 + 14 + len(b) * 4.6, T1 + H1 + 21))
    if c:
        d.arrow(f"M{R} {yc}H{L + W + 2}", label=c, at=(600, yc - 12))

d = Diagram("VVAH phase 2: hunt and double-check",
            "1 Hunt, S4: an AI reviewer goes through each chunk, guided by a language lens (42 languages) and, for "
            "specialist chunks, one of 11 specialist lenses. Optional voting runs each chunk 3 times and keeps what "
            "2 runs agree on; only the full profile turns it on. "
            "2 Filter, S5: rules drop findings in test or mock paths, in files that do not exist, with low "
            "confidence, or with no source or sink; one AI dedup call (on by default) merges look-alikes. "
            "3 Prove it wrong, S6: a fresh verifier per finding re-reads the code and hunts for defences. A true "
            "positive gets a CVSS score and moves on; a false positive is kept in the audit trail. "
            "4 Live check, beta and opt-in: exploit verification tests web-API findings against a running copy of "
            "the app. It only adds evidence and never drops a finding.")

d.group(L, T1, W, H1, "Hunt: S4", 1)
d.card(L + 30, T1 + 64, "AI reviewer per chunk|looks for weaknesses", "coding", w=492, h=72)
d.card(L + 30, T1 + 176, "Language lens|42 languages", "data", w=238, h=72)
d.card(L + 284, T1 + 176, "Specialist lens|11 kinds", "data", w=238, h=72)
d.arrow(f"M{L + 149} {T1 + 176}V{T1 + 138}")
d.arrow(f"M{L + 403} {T1 + 176}V{T1 + 138}")
d.note(L + W / 2, T1 + 310, "optional vote: 3 runs, 2 must agree")
d.note(L + W / 2, T1 + 338, "on in the full profile only")

d.group(R, T1, W, H1, "Filter: S5", 2)
grid(R, T1, [("Test or mock|path", "review"), ("File not there|made-up path", "review"),
             ("Low confidence|below the bar", "review"), ("No evidence|no source, sink", "review")])
d.note(R + W / 2, T1 + 300, "one AI dedup call, on by default")
d.note(R + W / 2, T1 + 328, "merges look-alikes")

d.group(R, T2, W, H2, "Prove it wrong: S6", 3)
d.card(R + 30, T2 + 64, "Fresh verifier per finding|re-reads code, hunts for defences", "critic", w=492, h=72)
d.card(R + 30, T2 + 196, "True positive|gets a CVSS score", "plan", w=238, h=80)
d.card(R + 284, T2 + 196, "False positive|kept for audit", "data", w=238, h=80)
d.ok(R + 248, T2 + 210)
d.bad(R + 502, T2 + 210)
d.arrow(f"M{R + 149} {T2 + 136}V{T2 + 194}")
d.arrow(f"M{R + 403} {T2 + 136}V{T2 + 194}")
d.note(R + W / 2, T2 + 330, "true positives go on to the report")

d.group(L, T2, W, H2, "Live check (beta, opt-in)", 4)
col(L, T2, [("Exploit verification|tests a running copy of the app", "critic"),
            ("Only adds evidence|never drops a finding", "data")], h=80)
d.note(L + W / 2, T2 + 300, "off unless an API collection is set")
d.note(L + W / 2, T2 + 328, "details in the next diagram")

handoffs("findings", "survivors", "API")
d.save(Path(__file__).with_name("check.svg"))
