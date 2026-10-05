"""Grafana overview: who comes in, the one server program, the data it reads, what it keeps and sends.
Drawn from grafana/grafana at commit 6b6eaf7 (contribute/architecture/k8s-inspired-backend-arch.md,
AGENTS.md, conf/defaults.ini, pkg/setting/setting_plugins.go for the preinstalled data sources,
pkg/services/ngalert/api/tooling/definitions/contact_points.go for the 23 contact point kinds).
Run: python3 diagram.py

Snake order: 1 ways in (top left) -> 2 the Grafana server (top right) -> 3 your data, where it lives
(bottom right); the server also saves to and sends from 4 (bottom left)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("Grafana overview",
            "People use the web app in a browser; scripts and tools use the HTTP APIs; config files and Git "
            "repositories can load dashboards and settings. "
            "1 Ways in: the web app, the HTTP APIs, files and Git. "
            "2 The Grafana server is one program: sign-in and permissions check every request, dashboards and "
            "folders are saved as JSON documents, the query engine asks data sources and can do maths on the "
            "answers, and alerting checks rules on a timer. "
            "3 Your data stays where it is: data source plugins talk to metrics, logs and traces stores such as "
            "Prometheus, Loki and Tempo, and to databases and clouds such as MySQL, Postgres and CloudWatch. "
            "Your data lives in your own systems and panels ask them again on every load. "
            "4 What Grafana keeps and sends: its own database (a SQLite file by default, or MySQL or Postgres), "
            "alert notifications to 23 kinds of contact point such as Slack, email and PagerDuty, and an optional "
            "image renderer that runs as a separate service.")

L, R, W = 24, 624, 552
T1, H1 = 84, 380
T2, H2 = 500, 364
CW, CH, GAP = 492, 64, 16


def column(x, top, cards, gap=GAP):
    for i, (lbl, kind) in enumerate(cards):
        d.card(x + 30, top + 64 + i * (CH + gap), lbl, kind, w=CW, h=CH)


d.pill(L, 16, W, 48, "People · scripts and tools · files and Git")
d.arrow(f"M{L + W / 2} 64V{T1 - 2}")

d.group(L, T1, W, H1, "Ways in", 1)
column(L, T1, [("Web app in the browser|dashboards · Explore · alerts", None),
               ("HTTP APIs|/api (classic) and /apis (new)", None),
               ("Files and Git|loaded at start, or synced", None)], gap=36)

d.group(R, T1, W, H1, "Grafana server: one program", 2)
column(R, T1, [("Sign-in and permissions|checks every request", "review"),
               ("Dashboards and folders|saved as JSON documents", "write"),
               ("Query engine|asks data sources, can do maths", "coding"),
               ("Alerting|checks rules on a timer", "critic")])

d.group(R, T2, W, H2, "Your data stays where it is", 3)
column(R, T2, [("Data source plugins|one per kind of system", "coding"),
               ("Metrics, logs, traces|Prometheus · Loki · Tempo", "data"),
               ("Databases and clouds|MySQL · Postgres · CloudWatch", "data")])
d.note(R + W / 2, T2 + H2 - 52, "The data lives in your own systems;")
d.note(R + W / 2, T2 + H2 - 26, "each panel load asks again")

d.group(L, T2, W, H2, "What Grafana keeps and sends", 4)
column(L, T2, [("Grafana's own database|SQLite file, or MySQL / Postgres", "write"),
               ("Alert notifications|Slack, email, PagerDuty: 23 kinds", "write"),
               ("Image renderer (optional)|separate service for PNGs", "coding")])
d.note(L + W / 2, T2 + H2 - 52, "database: users, dashboards, rules,")
d.note(L + W / 2, T2 + H2 - 26, "data source passwords (encrypted)")

d.arrow(f"M{L + W} {T1 + 200}H{R - 2}", label="requests", at=(600, T1 + 188))
d.arrow(f"M{R + 380} {T1 + H1}V{T2 - 2}", label="queries", at=(R + 440, T1 + H1 + 24))
d.arrow(f"M{R + 300} {T2}V{T1 + H1 + 2}", back=True, label="data", at=(R + 250, T1 + H1 + 24))
d.arrow(f"M{R + 60} {T1 + H1}V{T1 + H1 + 18}H{L + W / 2}V{T2 - 2}")
d.text(L + W / 2 + 130, T1 + H1 + 24, "saves · sends", "al")

d.note(600, 888, "Most data sources are plugins Grafana installs at start; only a few are built in")

d.save(Path(__file__).with_name("diagram.svg"))
