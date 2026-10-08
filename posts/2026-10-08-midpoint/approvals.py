"""Access requests and approvals: request a role, check the rules, approve in stages, finish.
Snake order: 1 request (top left) -> 2 check the rules (top right) -> 3 approve (bottom right) -> 4 finish (bottom left).
Drawn from Evolveum/midpoint at commit 160887ba (docs/admin-gui/request-access/index.adoc, docs/cases/approval,
docs/cases/escalation.adoc, docs/cases/notifications.adoc, docs/misc/deputy.adoc, infra/schema common-workflows-3.xsd,
model/workflow-impl ApprovalSchemaHelper, WorkItemCompletion, ConfigurationHelper, AssignmentPolicyAspectPart).
Run: python3 approvals.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, R, GW, T1, H1, T2, H2  # noqa: E402

d = Diagram("Access requests and approvals",
            "In: a user asks for a role in Request access. "
            "1 Request: pick the people, myself or a group, pick roles from a role catalog sorted like an e-shop, "
            "and submit the shopping cart after solving conflicts. The request is just the change itself: "
            "adding an assignment. "
            "2 Check the rules: policy rules say who must approve; with no such rule the default rule asks the "
            "role's approvers; a role with no approvers is assigned at once. "
            "3 Approve: approval runs in stages, one after another; all approvers in a stage must approve by "
            "default, or the first one decides; each approver gets a work item to approve or reject; deputies "
            "can decide for the approver; timed actions at a deadline escalate, delegate or complete the "
            "work item, for example reject it. "
            "4 Finish: approved, the change goes ahead; rejected, it is dropped; notifications go out as cases "
            "and work items open and close. A configured stage that finds no approvers rejects by default.")

d.pill(L, 16, GW, 48, "In: a user asks for a role in Request access")
d.arrow(f"M{L + GW / 2} 64V{T1 - 2}")

d.group(L, T1, GW, H1, "Request", 1)
d.column(L, T1, [("Pick people|myself or a group", "coding"),
                 ("Role catalog|roles sorted like an e-shop", "data"),
                 ("Shopping cart|solve conflicts · submit", "coding")])
d.notes(L, T1, H1, "The request is the change itself: a new assignment", "")

d.group(R, T1, GW, H1, "Check the rules", 2)
d.column(R, T1, [("Policy rules|say who must approve", "plan"),
                 ("Default rule|the role's approvers", "plan"),
                 ("Role has no approvers|assigned at once", "coding")])

d.group(R, T2, GW, H2, "Approve", 3)
d.column(R, T2, [("Stages|all must approve by default", "review"),
                 ("Work items|approve or reject", "review"),
                 ("Deputies|decide for the approver", "review"),
                 ("Timed actions|escalate · delegate · reject", "critic")], h=60, gap=14, first=60)

d.group(L, T2, GW, H2, "Finish", 4)
d.column(L, T2, [("Approved|the change goes ahead", "coding"),
                 ("Rejected|the change is dropped", "review"),
                 ("Notifications|cases · work items", "data")])
d.notes(L, T2, H2, "A rule stage with no approvers rejects by default", "")

d.arrow(f"M{L + GW} {T1 + 200}H{R - 2}", label="assignment", at=(600, T1 + 188))
d.arrow(f"M{R + 430} {T1 + H1}V{T2 - 2}", label="approval needed", at=(R + 430, T1 + H1 + 24))
d.arrow(f"M{R} {T2 + 176}H{L + GW + 2}", label="decision", at=(600, T2 + 164))

d.save(Path(__file__).with_name("approvals.svg"))
