"""How midPoint gives access: an assignment gives a user a role, inducements carry it down to accounts and groups.
Snake order: 1 assign (top left) -> 2 business role (top right) -> 3 application role (bottom right) -> 4 on the target (bottom left).
Drawn from Evolveum/midpoint at commit 160887ba (docs/roles-policies/roles: index, pdrbac, mining, role-autoassignment,
roles-services-and-orgs; docs/admin-gui/request-access; docs/concepts/activation; infra/schema common-core-3.xsd;
repo/system-init initial-objects/archetype 022, 028) and Evolveum/docs at 907aa8d
(midpoint/architecture/concepts/inducement-assignment-entitlement.adoc).
Run: python3 roles.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, R, GW, T1, H1, T2, H2  # noqa: E402

d = Diagram("How midPoint gives access",
            "In: a user who needs access. "
            "1 Assign: the user asks for a role in the role catalog and an approval follows, or midPoint assigns "
            "it on its own through an archetype, the org structure or an autoassign rule; an assignment can carry "
            "valid-from and valid-to dates. Orgs and services also act as roles. "
            "2 Business role: groups the access one job needs; conditions and parameters let one role serve "
            "many places, and the relation (member, owner, approver) changes what it gives. Role mining suggests "
            "new business roles from existing access. "
            "3 Application role: the access in one application, induced by business roles and not meant to be "
            "assigned directly; existing entitlements can be imported as application roles. Business role and "
            "application role are archetypes that ship with midPoint. "
            "4 On the target: an inducement makes the account and puts an entitlement, such as a group, on it, "
            "in LDAP, Active Directory and other systems. Entitlements belong to accounts, not users.")

d.pill(L, 16, GW, 48, "In: a user who needs access")
d.arrow(f"M{L + GW / 2} 64V{T1 - 2}")

d.group(L, T1, GW, H1, "Assign", 1)
d.column(L, T1, [("Request access|role catalog · approval", "review"),
                 ("Automatic|archetype · org · autoassign", "plan"),
                 ("Valid from · to|dates on the assignment", "data")])
d.notes(L, T1, H1, "Orgs and services also act as roles", "")

d.group(R, T1, GW, H1, "Business role", 2)
d.column(R, T1, [("Business role|the access one job needs", "plan"),
                 ("Conditions · parameters|one role · many places", "plan"),
                 ("Relation|member · owner · approver", "plan")])
d.notes(R, T1, H1, "Role mining suggests new ones", "")

d.group(R, T2, GW, H2, "Application role", 3)
d.column(R, T2, [("Application role|access in one application", "plan"),
                 ("Imported|from existing entitlements", "data"),
                 ("Archetypes|business · application role", "data")])
d.notes(R, T2, H2, "Not meant to be assigned directly", "")

d.group(L, T2, GW, H2, "On the target", 4)
d.column(L, T2, [("Account|made by a construction", "coding"),
                 ("Entitlement|a group on the account", "coding"),
                 ("Target system|LDAP · Active Directory …", "coding")])
d.notes(L, T2, H2, "Entitlements go on accounts, not users", "")

d.arrow(f"M{L + GW} {T1 + 200}H{R - 2}", label="assignment", at=(600, T1 + 188))
d.arrow(f"M{R + 430} {T1 + H1}V{T2 - 2}", label="inducement", at=(R + 430, T1 + H1 + 24))
d.arrow(f"M{R} {T2 + 176}H{L + GW + 2}", label="inducement", at=(600, T2 + 164))

d.save(Path(__file__).with_name("roles.svg"))
