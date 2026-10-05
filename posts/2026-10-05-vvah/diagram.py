"""VVAH overview: the four phases from a repo to a reviewed fix.  Drawn from the community fork
maximalfocus/visa-vulnerability-agentic-harness (README.md, docs/architecture.md, docs/features.md,
commit 1c292e3).  Run: python3 diagram.py

Snake order: 1 find where to look (top left) -> 2 hunt and double-check (top right) ->
3 report (bottom right) -> 4 fix and grade (bottom left)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("VVAH overview",
            "Input: your code repository plus optional context files. "
            "1 Find where to look: S0 builds a static code map and S1 surveys the repo, S2 builds a threat model, "
            "S3 splits the work into chunks for the reviewers, including 11 specialist lenses. "
            "2 Hunt and double-check: S4 AI reviewers look for weaknesses in each chunk, optionally voting; "
            "S5 filters obvious mistakes with rules and one AI dedup call; S6 a fresh verifier tries to prove each finding wrong, "
            "with an optional live check. "
            "3 Report: S7 merges duplicates, S8 links findings into attack chains and re-ranks them, "
            "S9 writes a Markdown report and SARIF. "
            "4 Fix and grade, off in the default profile: S10 proposes a minimal code fix, S11 two AI reviewers "
            "grade it, and people review every finding and fix.")

L, R, W = 24, 624, 552
T1, H1 = 84, 360
T2, H2 = 480, 372
CW, CH, GAP = 492, 64, 26


def column(x, top, cards):
    ys = []
    for i, (lbl, kind, *cls) in enumerate(cards):
        y = top + 64 + i * (CH + GAP)
        d.card(x + 30, y, lbl, kind, w=CW, h=CH, **({"cls": cls[0]} if cls else {}))
        if i:
            d.arrow(f"M{x + W / 2} {y - GAP}V{y - 2}")
        ys.append(y)
    return ys


d.pill(L, 16, W, 48, "Your code repo  +  optional context files")
d.arrow(f"M{L + W / 2} 64V{T1 - 2}")

d.group(L, T1, W, H1, "Find where to look", 1)
column(L, T1, [("Map the code|S0 code map · S1 repo survey", "coding"),
               ("Threat model|S2: what is valuable, who attacks", "plan"),
               ("Split the work|S3: chunks for 11 specialist lenses", "plan")])

d.group(R, T1, W, H1, "Hunt and double-check", 2)
column(R, T1, [("Hunt in each chunk|S4: AI reviewers, optional vote", "coding"),
               ("Filter the obvious|S5: rules + one AI dedup", "review"),
               ("Try to prove it wrong|S6: verifier, optional live check", "critic")])

d.group(R, T2, W, H2, "Report", 3)
column(R, T2, [("Merge duplicates|S7: same root cause, one finding", "review"),
               ("Link into attack chains|S8: re-rank by real risk", "plan"),
               ("Write the report|S9: Markdown + SARIF", "write")])

d.group(L, T2, W, H2, "Fix and grade (opt-in)", 4)
column(L, T2, [("Propose a fix|S10: minimal code change", "coding"),
               ("Grade the fix|S11: two AI reviewers", "critic"),
               ("People decide|review every finding and fix", None, "human")])
d.note(L + W / 2, T2 + H2 - 22, "S10 and S11 are off in the default profile")

d.arrow(f"M{L + W} {T1 + 210}H{R - 2}", label="chunks", at=(600, T1 + 198))
d.arrow(f"M{R + W / 2} {T1 + H1}V{T2 - 2}", label="true positives", at=(R + W / 2 + 90, T1 + H1 + 24))
d.arrow(f"M{R} {T2 + 200}H{L + W + 2}", label="findings", at=(600, T2 + 188))

d.note(600, 884, "Every finding is a lead for a person to check, not a final answer")

d.save(Path(__file__).with_name("diagram.svg"))
