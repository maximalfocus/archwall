"""/idd: one request goes to the one phase that owns it, and routing adds no authority.
Drawn from maximalfocus/idd-skills at commit f905928 (skills/idd/SKILL.md, CONSTITUTION.md Articles 1
and 5, scripts/validate.sh router checks).
Run: python3 router.py

Group 1 orients; group 2 holds the phases /idd may infer, group 3 the ones it reaches only by name;
group 4 holds the rules for both."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("idd router",
            "You type /idd and a request, for example /idd 6. "
            "1 Orient first: run protect-main.sh ensure, which prints the integration and release branches, then "
            "read the request: an issue number, a PRD pair, a phase named in words; then load that one phase's "
            "SKILL.md and run it in full. If a skill it needs is missing, it stops and names it. "
            "2 Phases it may infer: an issue number or URL goes to /idd-implement; what to do next goes to "
            "/idd-plan in its read-only default mode; checking the finished product goes to /idd-acceptance. "
            "3 Only when the request names it: /idd-issue, /idd-land, /idd-auto, /idd-promote, /idd-publish, "
            "/idd-evolve, and the /idd-plan modes bootstrap, reconstruct and reconcile. Never from state, history "
            "or an earlier turn. "
            "4 Routing adds no authority: if two phases fit or none does, it asks one question and never guesses; "
            "one phase per request; the same gates as calling the phase directly; and it says in one line which "
            "phase it chose and why. A missing PRD pair is a question, never a reason to bootstrap.")

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


d.pill(L, 16, W, 48, "You: /idd <request>, e.g. /idd 6")
d.arrow(f"M{L + W / 2} 64V{T1 - 2}")

d.group(L, T1, W, H1, "Orient first", 1)
column(L, T1, [("protect-main.sh ensure|prints integration and release", "review"),
               ("Read the request|issue number? PRD pair? phase named?", "plan"),
               ("Load the one phase|its SKILL.md, run in full", "plan")])
notes(L, T1, H1, "A skill it needs is missing?", "It stops and names it")

d.group(R, T1, W, H1, "Can be inferred", 2)
column(R, T1, [("Issue number or URL|→ /idd-implement", "coding"),
               ("What should I do next?|→ /idd-plan, read-only", "plan"),
               ("Check the finished product|→ /idd-acceptance", "critic")])

d.group(R, T2, W, H2, "Only when you name it", 3)
named = [("/idd-issue", "write"), ("/idd-land", "review"), ("/idd-auto", "plan"), ("/idd-promote", "write"),
         ("/idd-publish", "review"), ("/idd-evolve", "plan")]
for i, (lbl, kind) in enumerate(named):
    d.card(R + 30 + (i % 2) * 252, T2 + 60 + (i // 2) * 58, lbl, kind, w=240, h=48)
d.card(R + 30, T2 + 234, "/idd-plan bootstrap, reconstruct, reconcile", "plan", w=CW, h=48)
notes(R, T2, H2, "Never from state, history", "or an earlier turn")

d.group(L, T2, W, H2, "Routing adds no authority", 4)
column(L, T2, [("Two fit, or none?|ask one question, never guess", "review"),
               ("One phase per request|never two at once", "review"),
               ("Same gates|as calling the phase directly", "review")])
notes(L, T2, H2, "Says which phase it chose", "and why, in one line")

d.arrow(f"M{L + W} {T1 + 200}H{R - 2}", label="infer", at=(600, T1 + 188))
d.arrow(f"M{L + W - 70} {T1 + H1}V{T1 + H1 + 18}H{R + W / 2}V{T2 - 2}", label="named",
        at=(700, T1 + H1 + 24))

d.note(600, 888, "No PRD pair yet? That is a question, never a reason to bootstrap")

d.save(Path(__file__).with_name("router.svg"))
