"""midPoint overview: read the sources, decide what should be, govern it, write it out to the targets.
Snake order: 1 read the sources (top left) -> 2 decide (top right) -> 3 govern (bottom right) -> 4 write it out (bottom left).
Drawn from Evolveum/midpoint at commit 160887ba (README.md, docs/synchronization, docs/roles-policies, docs/cases,
docs/certification, docs/repository) and Evolveum/docs at 907aa8d (midpoint/architecture/index.adoc).
Run: python3 diagram.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, R, GW, T1, H1, T2, H2  # noqa: E402

d = Diagram("midPoint overview",
            "In: HR, apps and directories each hold part of who works here and what they may use. "
            "1 Read the sources: connectors read the HR system, apps and directories; import, live sync and "
            "reconciliation bring changes in. Every account is linked to a user, never account to account. "
            "2 Decide what should be: mappings turn account data into user data and back, roles give access, "
            "policy rules such as segregation of duties check it. "
            "3 Govern: requests wait for approval, certification campaigns ask people to confirm or revoke "
            "access, and the audit trail and reports record it all. "
            "4 Write it out: connectors create, change and delete accounts and groups on the targets; "
            "midPoint keeps a shadow that links to each account and stores its objects in a PostgreSQL repository.")

d.pill(L, 16, GW, 48, "In: HR · apps · directories hold who has what")
d.arrow(f"M{L + GW / 2} 64V{T1 - 2}")

d.group(L, T1, GW, H1, "Read the sources", 1)
d.column(L, T1, [("HR system|the source of people", "data"),
                 ("Connectors|ConnId · apps · directories", "coding"),
                 ("Sync|import · live sync · reconcile", "plan")])
d.notes(L, T1, H1, "Account → user → account, never account → account", "")

d.group(R, T1, GW, H1, "Decide what should be", 2)
d.column(R, T1, [("Mappings|account data ⇄ user data", "plan"),
                 ("Roles|assignments give access", "plan"),
                 ("Policy rules|segregation of duties …", "review")])

d.group(R, T2, GW, H2, "Govern", 3)
d.column(R, T2, [("Approvals|requests wait for a yes", "review"),
                 ("Certification|confirm or revoke access", "critic"),
                 ("Audit · reports|who changed what", "data")])

d.group(L, T2, GW, H2, "Write it out", 4)
d.column(L, T2, [("Targets|accounts · groups via connectors", "coding"),
                 ("Shadows|midPoint's link to each account", "data"),
                 ("Repository|PostgreSQL", "write")])

d.arrow(f"M{L + GW} {T1 + 200}H{R - 2}", label="changes", at=(600, T1 + 188))
d.arrow(f"M{R + 430} {T1 + H1}V{T2 - 2}", label="what should be", at=(R + 430, T1 + H1 + 24))
d.arrow(f"M{R} {T2 + 176}H{L + GW + 2}", label="allowed", at=(600, T2 + 164))

d.save(Path(__file__).with_name("diagram.svg"))
