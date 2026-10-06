"""/idd-auto: plan, issue, implement, land, one issue at a time, then the final acceptance.
Drawn from maximalfocus/idd-skills at commit f905928 (skills/idd-auto/SKILL.md, CONSTITUTION.md
Articles 1 and 5, skills/idd-plan/scripts/init-implementation.sh).
Run: python3 auto.py

Group 2 is the loop (dashed arrow on its right edge: next issue). Group 3 runs once nothing is left;
a product bug goes back to the loop as one repair issue. Group 4 holds the stop rules."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("idd-auto loop",
            "You run /idd-auto with a project, once. "
            "1 Bind the target: the exact PRD and code pair, and if only the code repository is missing it is "
            "created, private; read the PRD, the tracker and GitHub fresh at every turn; done means every "
            "requirement has landed or been validated, with clean trees and no branch or batch left open. "
            "2 One issue at a time, in a loop: resume active work before starting new; /idd-plan then /idd-issue "
            "for the one next issue; /idd-implement, which waits for checks and reviews; /idd-land to merge, close "
            "and reconcile; then the next issue. "
            "3 When no issue is left, the whole product: merge the tracker batch, run /idd-acceptance as a "
            "required final gate, and turn a product bug into one repair issue under the same slice, back into "
            "the loop. A new feature stops for your OK, and the PRD changes first. "
            "4 It stops and never bends: a red check, a conflict or an open product choice becomes one precise "
            "blocker; if "
            "you can clear it, it asks one question and resumes; it never publishes, promotes or accepts "
            "residuals. There is no trace file: each turn reads GitHub and the PRD again. Finishing ends its "
            "authority, so a later request needs its own go-ahead.")

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


d.pill(L, 16, W, 48, "You: /idd-auto <project>, once")
d.arrow(f"M{L + W / 2} 64V{T1 - 2}")

d.group(L, T1, W, H1, "Bind the target", 1)
column(L, T1, [("Exact PRD and code pair|code repo missing? made, private", "plan"),
               ("Read PRD, tracker, GitHub|fresh at every turn", "plan"),
               ("Done means|every requirement landed or validated", "critic")])
notes(L, T1, H1, "Done also needs clean trees,", "no branch or batch left open")

d.group(R, T1, W, H1, "One issue at a time", 2)
loop = [("Resume active work|before starting new", "data"),
        ("/idd-plan, then /idd-issue|the one next issue", "plan"),
        ("/idd-implement|waits for checks and reviews", "coding"),
        ("/idd-land|merge, close, reconcile", "review")]
for i, (lbl, kind) in enumerate(loop):
    d.card(R + 30, T1 + 64 + i * (CH + GAP), lbl, kind, w=CW - 24, h=CH)
y_first, y_last = T1 + 64 + CH / 2, T1 + 64 + 3 * (CH + GAP) + CH / 2
d.arrow(f"M{R + 30 + CW - 24} {y_last}H{R + W - 12}V{y_first}H{R + 30 + CW - 22}", back=True)

d.group(R, T2, W, H2, "Then the whole product", 3)
column(R, T2, [("Merge the tracker batch", "write"),
               ("/idd-acceptance|a required final gate", "critic"),
               ("Product bug?|one repair issue, same slice", "coding")])
notes(R, T2, H2, "New feature? Stop for your OK,", "then the PRD changes first")

d.group(L, T2, W, H2, "Stops, never bends", 4)
column(L, T2, [("Red check, conflict, open choice|one precise blocker", "review"),
               ("You can clear it?|one question, then resume", "review"),
               ("Never|publish, promote, accept residuals", "review")])
notes(L, T2, H2, "No trace file: each turn reads", "GitHub and the PRD again")

d.arrow(f"M{L + W} {T1 + 200}H{R - 2}", label="start", at=(600, T1 + 188))
d.arrow(f"M{R + 420} {T1 + H1}V{T2 - 2}", label="none left", at=(R + 476, T1 + H1 + 24))
d.arrow(f"M{R + 160} {T2}V{T1 + H1 + 2}", back=True, label="repair issue", at=(R + 82, T1 + H1 + 24))

d.note(600, 888, "Finishing ends its authority: a later request needs its own go-ahead")

d.save(Path(__file__).with_name("auto.svg"))
