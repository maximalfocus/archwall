"""peerreview overview: set up, rounds until done, the stop rule, hand-over.
Drawn from maximalfocus/peerreview-skills at commit 2f8d61e (README.md, skills/peerreview/SKILL.md,
scripts/select-peer.sh, scripts/delivery-branch.sh, scripts/review-anchor.sh).
Run: python3 diagram.py

Snake order: 1 set up (top left) -> 2 rounds (top right) -> 3 stop rule (bottom right)
-> 4 hand over (bottom left)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("peerreview overview",
            "You run /peerreview on a repo; the --chat and --dry-run flags are optional. "
            "1 Set up: a private, temporary charter is written from your own docs, the peer is picked from "
            "another vendor (Claude Code and the Codex CLI review each other), and work moves to a review "
            "branch with a baseline commit. "
            "2 Rounds until done: the host reviews and runs the gate, the peer co-edits files but never "
            "commits, behind a git guard and a 30-minute deadline, the host re-checks the real diff and reruns "
            "the gate, then commits the round. "
            "If a round makes no progress, the loop stops and reports. "
            "3 Stop only when every check passes, the peer says CONVERGED in a read-only verdict, and at "
            "least one peer round ran; there is no upper cap. NOT CONVERGED sends it back for another round. "
            "4 Hand over: one squashed commit in a pull request, a converged tag where the next review "
            "starts, and an honest report. Lessons from a run go to /peerreview-evolve.")

L, R, W = 24, 624, 552
T1, H1 = 84, 380
T2, H2 = 500, 364
CW, CH, GAP = 492, 64, 16


def column(x, top, cards, gap=GAP):
    for i, (lbl, kind) in enumerate(cards):
        d.card(x + 30, top + 64 + i * (CH + gap), lbl, kind, w=CW, h=CH)


d.pill(L, 16, W, 48, "You: /peerreview [repo]  (flags: --chat, --dry-run)")
d.arrow(f"M{L + W / 2} 64V{T1 - 2}")

d.group(L, T1, W, H1, "Set up", 1)
column(L, T1, [("Charter|private, temporary, from your docs", "plan"),
               ("Pick the peer|another vendor: Claude Code ↔ Codex", "plan"),
               ("Review branch|baseline commit first", "data")])
d.note(L + W / 2, T1 + H1 - 52, "Docs conflict or say nothing:")
d.note(L + W / 2, T1 + H1 - 26, "stop and ask")

d.group(R, T1, W, H1, "Rounds, until done", 2)
column(R, T1, [("HOST reviews|runs the gate, writes findings", "review"),
               ("PEER co-edits|guarded, never commits", "coding"),
               ("HOST re-checks|reads the real diff, reruns gate", "review"),
               ("Commit the round|the HOST owns git", "write")])

d.group(R, T2, W, H2, "Stop only when", 3)
column(R, T2, [("Every check passes|gate green, no findings left", "critic"),
               ("PEER says CONVERGED|read-only, neutral prompt", "critic"),
               ("At least 1 peer round|no upper cap", "data")])
d.note(R + W / 2, T2 + H2 - 52, "No progress in a round:")
d.note(R + W / 2, T2 + H2 - 26, "stop and report")

d.group(L, T2, W, H2, "Hand over", 4)
column(L, T2, [("One squashed commit|pull request on evolve/<slug>", "write"),
               ("Converged tag|the next review starts here", "data"),
               ("Honest report|each check, peer tier, leftovers", "write")])
d.note(L + W / 2, T2 + H2 - 52, "Never \"perfect\": converged against")
d.note(L + W / 2, T2 + H2 - 26, "the charter, leftovers listed")

d.arrow(f"M{L + W} {T1 + 200}H{R - 2}", label="ready", at=(600, T1 + 188))
d.arrow(f"M{R + 380} {T1 + H1}V{T2 - 2}", label="each round", at=(R + 450, T1 + H1 + 24))
d.arrow(f"M{R + 220} {T2}V{T1 + H1 + 2}", back=True, label="NOT CONVERGED", at=(R + 150, T1 + H1 + 24))
d.arrow(f"M{R} {T2 + 180}H{L + W + 2}", label="done", at=(600, T2 + 168))

d.note(600, 888, "Lessons from a run go to /peerreview-evolve, which keeps or drops them")

d.save(Path(__file__).with_name("diagram.svg"))
