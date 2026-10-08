"""midPoint synchronization: how a change on a resource gets into midPoint.
Snake order: 1 spot the change (top left) -> 2 find the owner (top right) -> 3 name the situation (bottom right)
-> 4 react (bottom left).
Drawn from Evolveum/midpoint at commit 160887ba (docs/synchronization/flavors.adoc, situations.adoc,
docs/correlation/index.adoc, correlation-cases.adoc, docs/tasks/synchronization-tasks,
infra/schema .../common-provisioning-3.xsd SynchronizationSituationType and SynchronizationActionsType,
common-correlation-3.xsd thresholds, common-tasks-3.xsd work definitions,
model/model-impl .../sync/SynchronizationState.java, SynchronizationServiceImpl.java).
Run: python3 sync.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, R, GW, T1, H1, T2, H2  # noqa: E402

d = Diagram("How a change gets into midPoint",
            "In: an account changes on a resource, for example a new hire in the HR system. "
            "1 Spot the change: live sync polls the resource's change log every few seconds; reconciliation "
            "is a scheduled full compare, the safety net; import usually runs once; asynchronous update takes "
            "messages and is experimental. Discovery is a change found during an unrelated operation. "
            "2 Find the owner: an account already linked to a user keeps that owner; otherwise correlation "
            "rules (items, filter, expression, idmatch) look for a user and give a confidence; 1.0 means a "
            "sure match by default. Correlation runs before the inbound mappings. "
            "3 Name the situation, one of five: linked (has its owner), unlinked (owner found, not yet linked), "
            "unmatched (no owner), disputed (not sure who), deleted (the account is gone). Situations are only "
            "about links, not about whether the person should have the account. "
            "4 React: each situation has its reactions, such as link, add focus or synchronize; delete or "
            "inactivate the user or the account; create a correlation case so a person picks the owner. "
            "Then inbound mappings copy account data into the user.")

d.pill(L, 16, GW, 48, "In: an account changes, e.g. a new hire in HR")
d.arrow(f"M{L + GW / 2} 64V{T1 - 2}")

d.group(L, T1, GW, H1, "Spot the change", 1)
d.column(L, T1, [("Live sync|polls the change log · seconds", "coding"),
                 ("Reconciliation|scheduled full compare", "critic"),
                 ("Import|usually runs once", "coding"),
                 ("Async update|messages · experimental", "coding")], h=56, gap=10, first=54)
d.notes(L, T1, H1, "Discovery: found during another operation", "")

d.group(R, T1, GW, H1, "Find the owner", 2)
d.column(R, T1, [("Already linked?|then it keeps that owner", "plan"),
                 ("Correlation rules|items · filter · expression · idmatch", "plan"),
                 ("Confidence|1.0 = sure match by default", "critic")])
d.notes(R, T1, H1, "Runs before the inbound mappings", "")

d.group(R, T2, GW, H2, "Name the situation", 3)
d.column(R, T2, [("linked|has its owner", "data"),
                 ("unlinked · unmatched|owner found · no owner", "data"),
                 ("disputed · deleted|not sure who · account gone", "data")])
d.notes(R, T2, H2, "Only about links, not who should have access", "")

d.group(L, T2, GW, H2, "React", 4)
d.column(L, T2, [("Reactions per situation|link · add focus · synchronize", "plan"),
                 ("Delete or inactivate|the user or the account", "coding"),
                 ("Correlation case|a person picks the owner", "review"),
                 ("Inbound mappings|account data → user", "write")], h=60, gap=14, first=60)

d.arrow(f"M{L + GW} {T1 + 200}H{R - 2}", label="change", at=(600, T1 + 188))
d.arrow(f"M{R + 430} {T1 + H1}V{T2 - 2}", label="owner or none", at=(R + 430, T1 + H1 + 24))
d.arrow(f"M{R} {T2 + 176}H{L + GW + 2}", label="situation", at=(600, T2 + 164))

d.save(Path(__file__).with_name("sync.svg"))
