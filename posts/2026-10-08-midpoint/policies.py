"""midPoint policy rules: where a rule lives, when it fires, what it does, what it leaves behind.
Snake order: 1 where the rule lives (top left) -> 2 when it fires (top right) -> 3 what it does (bottom right)
-> 4 what is left (bottom left).
Drawn from Evolveum/midpoint at commit 160887ba (docs/roles-policies/policies/policy-rules.adoc,
infra/schema/src/main/resources/xml/ns/public/common/common-policy-3.xsd PolicyConstraintsType and PolicyActionsType).
Run: python3 policies.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, R, GW, T1, H1, T2, H2  # noqa: E402

d = Diagram("midPoint policy rules",
            "In: a change to a user, a role or an assignment. "
            "1 Where the rule lives: global rules in the system configuration are checked on every operation; "
            "rules in a policy or metarole reach every role that has it assigned, through an inducement; "
            "since midPoint 4.11 rules can sit in a task activity too, for example to stop an import after "
            "a number of changes. A rule written straight into one role works but is not recommended. "
            "2 When it fires, the constraints: conflicts, where exclusion keeps two roles apart (segregation "
            "of duties) and requirement needs them together; counts and changes, such as too few or too many "
            "assignees, or a change or new assignment; state, such as an object state or having an assignment. "
            "Constraints combine with and, or and not. "
            "3 What it does, the actions: block, where enforcement ends the change in an error and prune "
            "removes the conflicting assignments; ask a person, an approval now or a certification campaign "
            "later; just record, with a mark, a notification or a script. suspendTask stops a task; "
            "remediation is experimental. "
            "4 What is left: a mark on the object, so reports can find the objects that break a rule; "
            "an approved exception stored in the assignment, which turns the rule off for that user and that "
            "assignment; policySituation, used up to midPoint 4.8, is deprecated in favour of marks.")

d.pill(L, 16, GW, 48, "In: a change to a user · role · assignment")
d.arrow(f"M{L + GW / 2} 64V{T1 - 2}")

d.group(L, T1, GW, H1, "Where the rule lives", 1)
d.column(L, T1, [("Global|system configuration · every operation", "plan"),
                 ("Policy or metarole|reaches the roles that have it", "plan"),
                 ("Task activity|e.g. stop an import · 4.11+", "plan")])
d.notes(L, T1, H1, "Straight in one role: works, not recommended", "")

d.group(R, T1, GW, H1, "When it fires", 2)
d.column(R, T1, [("Conflicts|exclusion (SoD) · requirement", "review"),
                 ("Counts and changes|min · max assignees · modification", "review"),
                 ("State|object state · has assignment", "review")])
d.notes(R, T1, H1, "Combine them with and · or · not", "")

d.group(R, T2, GW, H2, "What it does", 3)
d.column(R, T2, [("Block|enforcement error · prune conflicts", "review"),
                 ("Ask a person|approval now · certification later", "critic"),
                 ("Just record|mark · notification · script", "write")])
d.notes(R, T2, H2, "suspendTask stops a task", "remediation: experimental")

d.group(L, T2, GW, H2, "What is left", 4)
d.column(L, T2, [("Mark on the object|reports find who breaks a rule", "data"),
                 ("Approved exception|kept in the assignment · rule off", "data")])
d.notes(L, T2, H2, "policySituation (4.8 and earlier):", "deprecated · use marks")

d.arrow(f"M{L + GW} {T1 + 200}H{R - 2}", label="rule", at=(600, T1 + 188))
d.arrow(f"M{R + 430} {T1 + H1}V{T2 - 2}", label="triggered", at=(R + 430, T1 + H1 + 24))
d.arrow(f"M{R} {T2 + 176}H{L + GW + 2}", label="result", at=(600, T2 + 164))

d.save(Path(__file__).with_name("policies.svg"))
