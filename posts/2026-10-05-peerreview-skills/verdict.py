"""When a run may stop: the convergence contract and the verdict.
Drawn from maximalfocus/peerreview-skills at commit 2f8d61e (skills/peerreview/SKILL.md Step 4 and Step 5,
Required-peer failure, Hard rules).
Run: python3 verdict.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("peerreview stop rule",
            "1 All must hold: every acceptance check is met with evidence, the full gate exits clean, the host has "
            "no findings left and has swept every lens it opened, and the tree is clean with everything committed. "
            "2 Then the verdict prompt: a read-only round with no edits, only neutral facts such as the raw gate "
            "output, and it says in its first paragraph that reading is allowed. "
            "3 The peer answers CONVERGED, no substantive defects remain, which ends the loop; or NOT CONVERGED "
            "with the defects named, which starts round N+1. "
            "4 Other endings: a round with no progress stops and reports; no reachable peer stops with no stand-in; "
            "and the result is never called perfect. At least one peer round always runs, with no upper cap.")

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

d.pill(L, 16, W, 48, "In: the committed state after the last edit round")
d.arrow(f"M{L + W / 2} 64V{T1 - 2}")

d.group(L, T1, W, H1, "All must hold", 1)
column(L, T1, [("Every acceptance check met|with evidence", "critic"),
               ("Full gate exits clean", "critic"),
               ("No findings left|every lens swept, not sampled", "critic"),
               ("Tree clean|everything committed", "critic")])

d.group(R, T1, W, H1, "Verdict prompt", 2)
column(R, T1, [("Read-only round|no edits allowed", "review"),
               ("Neutral facts only|raw gate output, no \"all green\"", "review"),
               ("Reading is allowed|said in the first paragraph", "review")])
notes(R, T1, H1, "A leading prompt invites", "false agreement")

d.group(R, T2, W, H2, "PEER answers", 3)
column(R, T2, [("CONVERGED|no substantive defects remain", "plan"),
               ("NOT CONVERGED|defects named → round N+1", "review")])
notes(R, T2, H2, "At least 1 peer round,", "no upper cap")

d.group(L, T2, W, H2, "Other endings", 4)
column(L, T2, [("No progress|stop and report", "data"),
               ("No peer reachable|stop, no stand-in", "data"),
               ("Never \"perfect\"|converged, leftovers listed", "data")])

d.arrow(f"M{L + W} {T1 + 200}H{R - 2}", label="then ask", at=(600, T1 + 188))
d.arrow(f"M{R + W / 2} {T1 + H1}V{T2 - 2}")

d.note(600, 888, "The HOST cannot declare convergence alone: the PEER has to say it")

d.save(Path(__file__).with_name("verdict.svg"))
