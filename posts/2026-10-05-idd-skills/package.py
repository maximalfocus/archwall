"""What is in the box: ten skills, bundled scripts, the rule files, and GitHub as the place they act.
Drawn from maximalfocus/idd-skills at commit f905928 (README.md Skill, Install and Layout, CLAUDE.md,
CONSTITUTION.md Articles 4 and 5, skills/*/SKILL.md compatibility lines, skills/*/scripts/).
Run: python3 package.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("idd-skills package",
            "The skills run inside Claude Code, Codex, Pi or OpenCode. "
            "1 Ten skills, plain text: /idd, /idd-plan, /idd-issue, /idd-implement, /idd-land, /idd-auto, "
            "/idd-acceptance, /idd-promote, /idd-publish and /idd-evolve. "
            "2 They run bundled scripts: repo setup and merges (init-*.sh, land.sh, promote.sh), branch rules "
            "(protect-main.sh), and gates for PRD size, the tracker, line width and exposure. Fixed steps are "
            "scripts; judgment stays in the skill text. "
            "3 GitHub is reached through git and the gh command: the fixed steps by the bundled scripts, and the "
            "issues, pull requests and visibility change by the agent following the skill text. Per product: a "
            "code repository, plus a private PRD repository for planning. "
            "4 Rules in the box: CONSTITUTION.md says how the method may change, conventions.md sets names, "
            "branches and line width, and each skill file has a size cap between 60 and 160 lines. validate.sh "
            "checks them and is run before every commit. "
            "Install all ten with npx skills add maximalfocus/idd-skills --skill '*'.")

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


d.pill(L, 16, W, 48, "Inside Claude Code, Codex, Pi or OpenCode")
d.arrow(f"M{L + W / 2} 64V{T1 - 2}")

d.group(L, T1, W, H1, "Ten skills, plain text", 1)
skills = [("/idd", "plan"), ("/idd-plan", "plan"), ("/idd-issue", "write"), ("/idd-implement", "coding"),
          ("/idd-land", "review"), ("/idd-auto", "plan"), ("/idd-acceptance", "critic"),
          ("/idd-promote", "write"), ("/idd-publish", "review"), ("/idd-evolve", "plan")]
for i, (lbl, kind) in enumerate(skills):
    d.card(L + 30 + (i % 2) * 252, T1 + 64 + (i // 2) * 60, lbl, kind, w=240, h=50)

d.group(R, T1, W, H1, "Bundled scripts", 2)
column(R, T1, [("Repo setup and merges|init-*.sh, land.sh, promote.sh", "coding"),
               ("Branch rules on GitHub|protect-main.sh", "review"),
               ("Gates|PRD size, tracker, line width, exposure", "review")])
notes(R, T1, H1, "Fixed steps are scripts;", "the agent runs git and gh too")

d.group(R, T2, W, H2, "GitHub, through git and gh", 3)
column(R, T2, [("Issues and pull requests", "write"),
               ("Merges and branches", "data"),
               ("Settings, rulesets|and visibility", "review")])
notes(R, T2, H2, "Per product: a code repo, plus", "a private PRD repo for planning")

d.group(L, T2, W, H2, "Rules in the box", 4)
column(L, T2, [("CONSTITUTION.md|how the method may change", "review"),
               ("conventions.md|names, branches, line width", "review"),
               ("Size caps|each skill file 60 to 160 lines", "data")])
notes(L, T2, H2, "validate.sh checks them,", "run before every commit")

d.arrow(f"M{L + W} {T1 + 200}H{R - 2}", label="run", at=(600, T1 + 188))
d.arrow(f"M{R + W / 2} {T1 + H1}V{T2 - 2}", label="git, gh", at=(R + W / 2 + 44, T1 + H1 + 24))

d.note(600, 888, "Install all ten: npx skills add maximalfocus/idd-skills --skill '*'")

d.save(Path(__file__).with_name("package.svg"))
