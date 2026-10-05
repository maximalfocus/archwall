"""/idd-publish: prepare while private, scan everything, then make only the code repo public.
Drawn from maximalfocus/idd-skills at commit f905928 (skills/idd-publish/SKILL.md,
skills/idd-publish/scripts/scan-exposure.sh, skills/idd-plan/scripts/protect-main.sh, README.md
Publication boundary).
Run: python3 publish.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("idd-publish",
            "You run /idd-publish with a project, explicitly. "
            "1 Prepare, still private: reconcile the tracker at this pre-publish milestone; one preparation issue "
            "goes through plan, issue, implement and land; a license, MIT by default, green tests and an "
            "end-to-end check. The preparation change is scanned before it is pushed. "
            "2 Scan every commit: every commit message and every file on every ref, old pull request refs too, "
            "since GitHub keeps them, for secrets and private names from a built-in list plus your terms. A hit "
            "in a commit message cannot be purged: publish from a new repository, or you accept it knowingly. "
            "3 Check by hand: issues, comments, reviews and their edit history; Actions runs, logs and artifacts; "
            "branches, tags, releases, repository metadata, and package and documentation links. Any match "
            "blocks the visibility change. "
            "4 Flip and verify: the code repository becomes public and the PRD repository stays private; check "
            "while signed out that the code is readable and the PRD is denied; re-apply protection, so the "
            "rulesets are now enforced. Publishing is not deploying: no hosting, release or package.")

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


d.pill(L, 16, W, 48, "You: /idd-publish <project>, explicitly")
d.arrow(f"M{L + W / 2} 64V{T1 - 2}")

d.group(L, T1, W, H1, "Prepare, still private", 1)
column(L, T1, [("Reconcile the tracker|a pre-publish milestone", "plan"),
               ("One preparation issue|plan → issue → implement → land", "coding"),
               ("License, MIT by default|green tests, end-to-end check", "review")])
notes(L, T1, H1, "The preparation change is scanned", "before it is pushed")

d.group(R, T1, W, H1, "Scan every commit", 2)
column(R, T1, [("Every commit message|and every file, on every ref", "review"),
               ("Old PR refs too|GitHub keeps them", "review"),
               ("Secrets, private names|a built-in list + your terms", "review")])
notes(R, T1, H1, "A hit in a commit message can't be purged:", "new repo, or you accept it knowingly")

d.group(R, T2, W, H2, "Check by hand", 3)
column(R, T2, [("Issues, comments, reviews|and their edit history", "critic"),
               ("Actions runs, logs, artifacts", "critic"),
               ("Branches, tags, releases|metadata, package and doc links", "critic")])
notes(R, T2, H2, "Any match blocks", "the visibility change")

d.group(L, T2, W, H2, "Flip and verify", 4)
column(L, T2, [("Code repo → public|the PRD repo stays private", "write"),
               ("Check signed out|code readable, PRD denied", "review"),
               ("Re-apply protection|rulesets now enforced", "review")])

d.arrow(f"M{L + W} {T1 + 200}H{R - 2}", label="landed", at=(600, T1 + 188))
d.arrow(f"M{R + W / 2} {T1 + H1}V{T2 - 2}", label="clean", at=(R + W / 2 + 34, T1 + H1 + 24))
d.arrow(f"M{R} {T2 + 176}H{L + W + 2}", label="clean", at=(600, T2 + 164))

d.note(600, 888, "Publishing is not deploying: no hosting, release or package")

d.save(Path(__file__).with_name("publish.svg"))
