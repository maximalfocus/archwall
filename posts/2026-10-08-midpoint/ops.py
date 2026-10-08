"""Running midPoint: install it, set up the repository, run the background tasks, watch and maintain it.
Snake order: 1 install (top left) -> 2 set up the repository (top right) -> 3 run tasks (bottom right) -> 4 watch and maintain (bottom left).
Drawn from Evolveum/midpoint at commit 160887ba (docs/deployment, gui/admin-gui/src/main/resources/application.yml,
repo/system-init/src/main/resources/config.xml, config/sql/README.txt, repo/task-quartz-impl TaskManagerConfiguration.java,
tools/ninja Command.java, docs/misc/notifications/configuration.adoc, model/report-impl ReportUtils.java)
and Evolveum/docs at 907aa8d (midpoint/get-started/install/containers/index.adoc).
Run: python3 ops.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, R, GW, T1, H1, T2, H2  # noqa: E402

d = Diagram("Running midPoint",
            "In: an admin installs and runs midPoint. "
            "1 Install: the distribution starts with bin/start.sh and listens on port 8080, the web app at "
            "/midpoint; the container image needs a database container next to it. The midpoint.home directory "
            "holds config.xml, keys, logs and connector files. "
            "2 Set up the repository: config.xml points to a native PostgreSQL repository; the schema scripts "
            "create the main, audit and Quartz tables; when installed midPoint loads initial objects such as "
            "the administrator user and the Superuser role. "
            "3 Run tasks: the task manager uses the Quartz scheduler with 10 worker threads per node by default; "
            "background tasks run live sync, reconciliation and import. In a cluster several nodes share one "
            "repository and take tasks first come, first served; clustered is false by default and must be "
            "set to true on every node. "
            "4 Watch and maintain: reports in CSV, HTML or XLSX and dashboards; notifications by mail, SMS, "
            "file or a custom transport; midpoint.log and Spring Boot actuator endpoints such as health and "
            "metrics; and the ninja command-line tool to import, export and upgrade.")

d.pill(L, 16, GW, 48, "In: an admin installs and runs midPoint")
d.arrow(f"M{L + GW / 2} 64V{T1 - 2}")

d.group(L, T1, GW, H1, "Install", 1)
d.column(L, T1, [("Distribution|bin/start.sh · port 8080", "coding"),
                 ("Container image|needs a database container", "coding"),
                 ("midpoint.home|config.xml · keys · logs · connectors", "write")])
d.notes(L, T1, H1, "Web app at /midpoint", "")

d.group(R, T1, GW, H1, "Set up the repository", 2)
d.column(R, T1, [("Native PostgreSQL|repository type native", "write"),
                 ("Schema scripts|main · audit · Quartz tables", "data"),
                 ("Initial objects|administrator · Superuser role", "data")])

d.group(R, T2, GW, H2, "Run tasks", 3)
d.column(R, T2, [("Task manager|Quartz · 10 threads per node", "plan"),
                 ("Background tasks|live sync · reconcile · import", "coding"),
                 ("Cluster|nodes share one repository", "coding")])
d.notes(R, T2, H2, "clustered: false by default", "set it to true on every node")

d.group(L, T2, GW, H2, "Watch and maintain", 4)
d.column(L, T2, [("Reports · dashboards|CSV · HTML · XLSX", "data"),
                 ("Notifications|mail · SMS · file · custom", "write"),
                 ("Logs · actuator|midpoint.log · health · metrics", "data"),
                 ("ninja tool|import · export · upgrade", "plan")], h=60, gap=14, first=60)

d.arrow(f"M{L + GW} {T1 + 200}H{R - 2}", label="config.xml", at=(600, T1 + 188))
d.arrow(f"M{R + 430} {T1 + H1}V{T2 - 2}", label="tasks stored", at=(R + 430, T1 + H1 + 24))
d.arrow(f"M{R} {T2 + 176}H{L + GW + 2}", label="results", at=(600, T2 + 164))

d.save(Path(__file__).with_name("ops.svg"))
