"""Landing a review: a branch during the loop, one commit at the end.
Drawn from maximalfocus/peerreview-skills at commit 2f8d61e (scripts/delivery-branch.sh, scripts/review-anchor.sh,
scripts/chat-review-temp.sh, skills/peerreview/SKILL.md Step 3, Step 6, Path-scoped git policy).
Run: python3 deliver.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("peerreview landing",
            "1 During the review: work happens on the branch peerreview/<slug>, in its own worktree when installed "
            "skills point into this repo, and round commits are evidence, not product history. "
            "2 Landing: the rounds are squashed into one commit on evolve/<slug>, which is pushed and opened as a "
            "pull request; the base branch is never written. "
            "3 After: the maintainer merges with land-evolution.sh only on an explicit go-ahead, a converged tag "
            "peerreview/converged/... marks the reviewed commit, and the reviewed repo is pushed, failing loudly "
            "if it can't be. "
            "4 Exceptions: repos under ~/projects get no git writes at all; the --chat flag uses a temporary repo, "
            "answers in chat and deletes it; when an open pull request is named, the review runs on its branch.")

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

d.pill(L, 16, W, 48, "In: the repo you asked to review")
d.arrow(f"M{L + W / 2} 64V{T1 - 2}")

d.group(L, T1, W, H1, "During the review", 1)
column(L, T1, [("Review branch|peerreview/<slug>", "data"),
               ("Own worktree|if installed skills point here", "data"),
               ("Round commits|evidence, not history", "data")])
notes(L, T1, H1, "Baseline commit first, so each", "round's diff is its own")

d.group(R, T1, W, H1, "Land", 2)
column(R, T1, [("Squash to one commit|on evolve/<slug>", "write"),
               ("Subject checked first|type: lowercase description", "review"),
               ("Push and open a PR|base branch never written", "write")])

d.group(R, T2, W, H2, "After", 3)
column(R, T2, [("Converged tag|peerreview/converged/…", "data"),
               ("Push the reviewed repo|fail loud if it can't", "write"),
               ("Maintainer merges later|land-evolution.sh, on go-ahead", "plan")])

d.group(L, T2, W, H2, "Exceptions", 4)
column(L, T2, [("Repo under ~/projects|no git writes at all", "review"),
               ("Flag --chat|temp repo, answer in chat, deleted", "review"),
               ("Open PR named|review runs on its branch", "review")])

d.arrow(f"M{L + W} {T1 + 200}H{R - 2}", label="land", at=(600, T1 + 188))
d.arrow(f"M{R + W / 2} {T1 + H1}V{T2 - 2}", label="PR", at=(R + W / 2 + 30, T1 + H1 + 24))

d.note(600, 888, "The tag gives the next review a starting point: full, or the changes since")

d.save(Path(__file__).with_name("deliver.svg"))
