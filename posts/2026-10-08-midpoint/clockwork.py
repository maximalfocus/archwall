"""One change through midPoint's model: the clockwork drives it, the projector computes it, then it is checked and executed.
Snake order, three columns: 1 take the request, 2 compute the user, 3 compute the accounts (top row, left to right),
4 check, 5 execute, 6 finish (bottom row, right to left).
The clockwork docs list four states (INITIAL, PRIMARY, SECONDARY, FINAL); ModelState also has EXECUTION and
POSTEXECUTION, but ClockworkClick never switches to them, so they are left out.
Drawn from Evolveum/midpoint at commit 160887ba (docs/concepts/clockwork/clockwork-and-projector.adoc,
model-impl lens/ClockworkClick.java, lens/projector/Projector.java, projector/focus/AssignmentHolderProcessor.java,
projector/ProjectionValuesProcessor.java, workflow-impl wf/impl/hook/WfHook.java and processors/primary/PrimaryChangeProcessor.java,
notifications-impl NotificationHook.java).
Run: python3 clockwork.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, C3, CW3, T1, H1, T2, H2  # noqa: E402

d = Diagram("One change through the model",
            "In: a change from the GUI, from a service or found by synchronization. "
            "1 Take the request, state INITIAL: the clockwork loads the user and its accounts and audits "
            "the request. "
            "2 Compute the user, in the projector: inbound mappings bring account data into the user, the "
            "object template fills in user data, assignments are evaluated with the roles' inducements, "
            "and the user's policy rules are evaluated. "
            "3 Compute the accounts, one by one: outbound mappings turn user data into account data, the values "
            "are consolidated, strong and weak mappings merged, and the account's policy rules are evaluated. "
            "Nothing is changed yet; the result is a preview. "
            "4 Check, state PRIMARY: rules with the enforce action stop the change; the approvals hook may "
            "take the change into an approval case and continue in the background. "
            "5 Execute, state SECONDARY: the model is computed again, then the changes are written to the "
            "repository and through provisioning to the accounts, and audited; with provisioning dependencies "
            "this runs in several waves. "
            "6 Finish, state FINAL: the final execution is audited and the notifications hook sends notifications.")

x1, x2, x3 = C3
W3 = CW3 - 60

d.pill(24, 16, 1152, 48, "In: a change from the GUI · a service · synchronization")
d.arrow(f"M{x1 + CW3 / 2} 64V{T1 - 2}")

d.group(x1, T1, CW3, H1, "Take the request", 1)
d.column(x1, T1, [("Load|the user · its accounts", "data"),
                  ("Audit|stage: request", "data")], w=W3)
d.notes(x1, T1, H1, "State INITIAL", w=CW3)

d.group(x2, T1, CW3, H1, "Compute the user", 2)
d.column(x2, T1, [("Inbound|account data → user", "plan"),
                  ("Object template|fills in user data", "plan"),
                  ("Assignments|roles · inducements", "plan"),
                  ("Policy rules|for the user", "review")], h=60, gap=14, first=60, w=W3)

d.group(x3, T1, CW3, H1, "Compute the accounts", 3)
d.column(x3, T1, [("Outbound|user data → account", "plan"),
                  ("Consolidate|merge strong · weak", "plan"),
                  ("Policy rules|for each account", "review")], w=W3)
d.notes(x3, T1, H1, "Nothing changed yet: a preview", w=CW3)

d.group(x3, T2, CW3, H2, "Check", 4)
d.column(x3, T2, [("Enforce|a violation stops it", "review"),
                  ("Approvals hook|may open a case", "review")], w=W3)
d.notes(x3, T2, H2, "State PRIMARY", "Waits for approval in the background", w=CW3)

d.group(x2, T2, CW3, H2, "Execute", 5)
d.column(x2, T2, [("Execute|repository · provisioning", "coding"),
                  ("Audit|stage: execution", "data")], w=W3)
d.notes(x2, T2, H2, "State SECONDARY · computed again", "Dependencies: several waves", w=CW3)

d.group(x1, T2, CW3, H2, "Finish", 6)
d.column(x1, T2, [("Audit|final execution", "data"),
                  ("Notifications|hook in FINAL", "write")], w=W3)
d.notes(x1, T2, H2, "State FINAL", w=CW3)

ya = T1 + 280
d.arrow(f"M{x1 + CW3} {ya}H{x2 - 2}", label="request", at=((x1 + CW3 + x2) / 2, ya - 12))
d.arrow(f"M{x2 + CW3} {ya}H{x3 - 2}", label="user", at=((x2 + CW3 + x3) / 2, ya - 12))
d.arrow(f"M{x3 + CW3 / 2} {T1 + H1}V{T2 - 2}", label="preview", at=(x3 + CW3 / 2 + 50, T1 + H1 + 24))
yb = T2 + 240
d.arrow(f"M{x3} {yb}H{x2 + CW3 + 2}", label="allowed", at=((x2 + CW3 + x3) / 2, yb - 12))
d.arrow(f"M{x2} {yb}H{x1 + CW3 + 2}", label="done", at=((x1 + CW3 + x2) / 2, yb - 12))

d.save(Path(__file__).with_name("clockwork.svg"))
