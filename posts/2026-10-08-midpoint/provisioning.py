"""How midPoint writes a change to a target system: the provisioning subsystem.
Snake order: 1 the resource (top left) -> 2 the shadow (top right) -> 3 the connector (bottom right) -> 4 wait or retry (bottom left).
Drawn from Evolveum/midpoint at commit 160887ba (docs/resources: connid, resource-configuration/capabilities,
shadow, attribute-caching, entitlements, manual, asynchronous/outbound, propagation, maintenance-state;
docs/synchronization/consistency; provisioning/provisioning-impl ProvisioningUtil.java, provisioning/ucf-impl-builtin,
gui/admin-gui/pom.xml bundled connectors; repo/system-init initial system configuration).
Run: python3 provisioning.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, R, GW, T1, H1, T2, H2  # noqa: E402

d = Diagram("How midPoint writes to a target system",
            "In: the model decides that an account on a target system must be created, changed or deleted. "
            "1 The resource: a resource definition names the connector and its settings; the resource schema "
            "lists the object classes and attributes the connector reads from the system; object types say "
            "which objects are accounts and which are entitlements such as groups. Capabilities are native "
            "to the resource or simulated by midPoint. "
            "2 The shadow: midPoint keeps a shadow in its repository that links the user to the real account, "
            "groups are shadows too, and attributes are cached in the shadow (passive caching, on by default "
            "for new installations). "
            "3 The connector does the work, one of three kinds: ConnId connectors such as the bundled LDAP, CSV "
            "and DatabaseTable connectors; the built-in manual connector, which opens a case for a person; "
            "or the built-in asynchronous connector (experimental), which sends a message to a queue. Changes can be grouped "
            "and sent together with operation grouping: a grouping interval on the resource and a propagation task. "
            "4 Wait or retry: an operation that is not done yet, because the resource is down, a person still "
            "has to do it, or the resource is in maintenance mode (experimental) set by an admin, is kept in the shadow as a "
            "pending operation; a failed one is retried after 30 minutes, up to 3 times by default.")

d.pill(L, 16, GW, 48, "In: the model says an account must change")
d.arrow(f"M{L + GW / 2} 64V{T1 - 2}")

d.group(L, T1, GW, H1, "The resource", 1)
d.column(L, T1, [("Resource definition|which connector · its settings", "plan"),
                 ("Resource schema|object classes · attributes", "data"),
                 ("Object types|accounts · entitlements (groups)", "data")])
d.notes(L, T1, H1, "Capabilities: native, or simulated by midPoint", "")

d.group(R, T1, GW, H1, "The shadow", 2)
d.column(R, T1, [("Shadow|links the user to the account", "write"),
                 ("Groups|are shadows too", "write"),
                 ("Cached attributes|kept in the shadow", "data")])
d.notes(R, T1, H1, "Caching: on by default for new installs", "")

d.group(R, T2, GW, H2, "The connector", 3)
d.column(R, T2, [("ConnId connectors|LDAP · CSV · DatabaseTable …", "coding"),
                 ("Manual connector|opens a case for a person", "coding"),
                 ("Async connector|queue message · experimental", "coding")])
d.notes(R, T2, H2, "Optional grouping: an interval on the resource", "plus a propagation task")

d.group(L, T2, GW, H2, "Wait or retry", 4)
d.column(L, T2, [("Pending operation|kept in the shadow", "data"),
                 ("Retry|after 30 min · up to 3 times", "coding"),
                 ("Maintenance mode|admin sets it · experimental", "plan")])
d.notes(L, T2, H2, "Manual: done when the case is closed", "")

d.arrow(f"M{L + GW} {T1 + 200}H{R - 2}", label="change", at=(600, T1 + 188))
d.arrow(f"M{R + 430} {T1 + H1}V{T2 - 2}", label="operation", at=(R + 430, T1 + H1 + 24))
d.arrow(f"M{R} {T2 + 176}H{L + GW + 2}", label="not done yet", at=(600, T2 + 164))

d.save(Path(__file__).with_name("provisioning.svg"))
