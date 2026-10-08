"""Simulations: try a config change without touching real data, then switch it on.
Snake order: 1 mark it proposed (top left) -> 2 run a simulation (top right) -> 3 read the result (bottom right)
-> 4 switch it on (bottom left).
Drawn from Evolveum/midpoint at commit 160887ba (docs/simulation/index.adoc, docs/simulation/results/metrics.adoc,
docs/admin-gui/simulations.adoc, infra/schema/.../SimulationUtil.java, infra/schema/.../TaskExecutionMode.java,
common-tasks-3.xsd ExecutionModeType).
Run: python3 simulation.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, R, GW, T1, H1, T2, H2  # noqa: E402

d = Diagram("Simulations: try a change first",
            "In: a new or changed piece of config, such as a mapping, an object type or a whole resource. "
            "1 Mark it proposed: each config item has a lifecycle state, in the order draft, proposed, active, "
            "deprecated, archived. Draft and archived items are not used at all; proposed items are seen only "
            "by simulations; active and deprecated items are what production uses. "
            "2 Run a simulation: a task such as import, reconciliation, live sync or recompute runs in preview "
            "mode, where changes are computed but not applied. It uses the development config (active plus "
            "proposed items) or the production config (active plus deprecated items). The development config "
            "never runs in full mode, and approvals and notifications are skipped. "
            "3 Read the result: the simulation result lists what would change, with built-in metrics (added, "
            "modified, deleted) and event marks such as focus activated; it is shown in the GUI or exported "
            "as reports. "
            "4 Switch it on: set the new item from proposed to active and the old one from deprecated to "
            "archived, both at once for a seamless switch; from then on full mode writes the changes to the "
            "repository and the resources and records them in the audit log.")

d.pill(L, 16, GW, 48, "In: a new mapping · object type · resource")
d.arrow(f"M{L + GW / 2} 64V{T1 - 2}")

d.group(L, T1, GW, H1, "Mark it proposed", 1)
d.column(L, T1, [("Draft · archived|not used at all", "data"),
                 ("Proposed|seen only by simulations", "plan"),
                 ("Active · deprecated|what production uses", "coding")])
d.notes(L, T1, H1, "draft → proposed → active → deprecated → archived", "")

d.group(R, T1, GW, H1, "Run a simulation", 2)
d.column(R, T1, [("Preview mode|computed · not applied", "coding"),
                 ("Development config|active + proposed items", "data"),
                 ("Production config|active + deprecated items", "data")])
d.notes(R, T1, H1, "Import · reconcile · live sync · recompute …",
        "Approvals and notifications are skipped")

d.group(R, T2, GW, H2, "Read the result", 3)
d.column(R, T2, [("Simulation result|what would change", "write"),
                 ("Built-in metrics|added · modified · deleted", "critic"),
                 ("Event marks|e.g. focus activated", "critic")])
d.notes(R, T2, H2, "Shown in the GUI or exported as reports", "")

d.group(L, T2, GW, H2, "Switch it on", 4)
d.column(L, T2, [("Proposed → active|the new item goes live", "plan"),
                 ("Deprecated → archived|the old item retires", "plan"),
                 ("Full mode|writes · audits the changes", "coding")])
d.notes(L, T2, H2, "Both switches at once: no gap", "")

d.arrow(f"M{L + GW} {T1 + 200}H{R - 2}", label="proposed", at=(600, T1 + 188))
d.arrow(f"M{R + 430} {T1 + H1}V{T2 - 2}", label="would-be changes", at=(R + 430, T1 + H1 + 24))
d.arrow(f"M{R} {T2 + 176}H{L + GW + 2}", label="looks right", at=(600, T2 + 164))

d.save(Path(__file__).with_name("simulation.svg"))
