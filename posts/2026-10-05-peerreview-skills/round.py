"""One round of the loop.
Drawn from maximalfocus/peerreview-skills at commit 2f8d61e (skills/peerreview/SKILL.md Step 4,
scripts/claude-round.sh, scripts/codex-round.sh, scripts/round-support.sh).
Run: python3 round.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("peerreview one round",
            "1 The host reviews: it sweeps the charter, correctness and security first, re-sweeps every kind of "
            "defect already found, and runs the full gate. "
            "2 It writes a prompt file with the whole charter and its ranked findings, and the peer is told to "
            "form its own findings too. "
            "3 The peer co-edits through its driver script: minimal edits, no commit, and it reports the gate "
            "result. Each round has a 30 minute deadline by default. "
            "4 The host re-checks after the driver exits: the real git diff and status, the gate again, and "
            "every claimed fix is fact-checked. Then it commits the round. A round that makes things worse is "
            "reverted with tighter findings; a round with no progress stops the loop.")

L, R, W = 24, 624, 552
T1, H1 = 84, 380
T2, H2 = 500, 364
CW, CH, GAP = 492, 64, 16


def column(x, top, cards, gap=GAP):
    for i, (lbl, kind) in enumerate(cards):
        d.card(x + 30, top + 64 + i * (CH + gap), lbl, kind, w=CW, h=CH)


def notes(x, top, h, a, b):
    d.note(x + W / 2, top + h - 52, a)
    d.note(x + W / 2, top + h - 26, b)

d.pill(L, 16, W, 48, "In: the charter and the last committed state")
d.arrow(f"M{L + W / 2} 64V{T1 - 2}")

d.group(L, T1, W, H1, "HOST reviews", 1)
column(L, T1, [("Sweep the charter|correctness and security first", "review"),
               ("Re-sweep old defect kinds|every sibling, not one line", "review"),
               ("Run the full gate", "review"),
               ("Prompt file|whole charter + ranked findings", "write")])

d.group(R, T1, W, H1, "PEER co-edits", 2)
column(R, T1, [("Driver script|claude-, codex-, pi- or dsh-round", "coding"),
               ("Own findings too|not a confirm-my-work pass", "coding"),
               ("Minimal edits|no commit, no push", "coding")])
notes(R, T1, H1, "30 min deadline per round,", "set by an env var")

d.group(R, T2, W, H2, "HOST re-checks", 3)
column(R, T2, [("Wait for the driver to exit|a mid-flight tree can't be trusted", "review"),
               ("Real git diff and status|not the PEER's report", "review"),
               ("Rerun gate, fact-check fixes|a \"fix\" can be a regression", "review")])

d.group(L, T2, W, H2, "Commit the round", 4)
column(L, T2, [("peerreview: round N|HOST and PEER as co-authors", "write"),
               ("Worse than before?|revert, tighter findings", "review")])
notes(L, T2, H2, "No progress in a round:", "stop the loop and report")

d.arrow(f"M{L + W} {T1 + 200}H{R - 2}", label="prompt", at=(600, T1 + 188))
d.arrow(f"M{R + W / 2} {T1 + H1}V{T2 - 2}", label="edited files", at=(R + W / 2 + 70, T1 + H1 + 24))
d.arrow(f"M{R} {T2 + 176}H{L + W + 2}", label="checked", at=(600, T2 + 164))
d.arrow(f"M{L + W / 2} {T2}V{T1 + H1 + 2}", back=True, label="next round", at=(L + W / 2 + 70, T1 + H1 + 24))

d.note(600, 888, "The HOST owns git and the decision to stop; the PEER only edits")

d.save(Path(__file__).with_name("round.svg"))
