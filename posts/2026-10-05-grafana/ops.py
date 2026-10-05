"""Grafana: running it.  Drawn from grafana/grafana at commit 6b6eaf7: pkg/cmd/grafana (grafana server,
one binary), conf/defaults.ini (http_port = 3000; [database]; [remote_cache] type = database, redis, memcached;
[live] ha_engine empty = one server only, redis for several; [unified_alerting] ha_listen_address 0.0.0.0:9094
or ha_redis_*; [metrics] enabled; [tracing.opentelemetry] off; reporting_enabled = true), Dockerfile and
packaging/ (docker, deb, rpm, msi, mac), LICENSING.md (AGPL-3.0), pkg/extensions/main.go (Enterprise is a
separate build), pkg/services/featuremgmt/registry.go (398 flags, 59 GA), pkg/storage/unified/search (index per
server).

Snake order: 1 one program -> 2 several servers -> 3 keep them in step -> 4 watching Grafana.
Run: python3 ops.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

L, R, W = 24, 624, 552
T1, H1 = 16, 416
T2, H2 = 456, 404


def col(x, top, cards, h=72, gap=24, arrows=True):
    """One column of wide cards, top to bottom, optionally joined by arrows."""
    for i, (lbl, kind) in enumerate(cards):
        y = top + 64 + i * (h + gap)
        d.card(x + 30, y, lbl, kind, w=492, h=h)
        if arrows and i:
            d.arrow(f"M{x + W / 2} {y - gap}V{y - 2}")


def notes(x, top, hgt, *lines):
    """Up to two note lines at the foot of a group."""
    for i, s in enumerate(lines):
        d.note(x + W / 2, top + hgt - 22 - (len(lines) - 1 - i) * 26, s)


def handoffs(a, b, c, ya=T1 + 206, yc=T2 + 200):
    """Arrows between the four groups in snake order, with what each one carries."""
    if a:
        d.arrow(f"M{L + W} {ya}H{R - 2}", label=a, at=(600, ya - 12))
    if b:
        d.arrow(f"M{R + W / 2} {T1 + H1}V{T2 - 2}", label=b, at=(R + W / 2 + 14 + len(b) * 4.6, T1 + H1 + 21))
    if c:
        d.arrow(f"M{R} {yc}H{L + W + 2}", label=c, at=(600, yc - 12))

d = Diagram("Grafana: running it",
            "1 One program: grafana server serves the web app and the APIs on port 3000; it ships as Docker images, "
            "deb and rpm packages, and Windows and Mac builds; the open-source edition is AGPLv3 and Enterprise is a "
            "separate build. "
            "2 Several servers: a load balancer spreads users across copies of Grafana that share one MySQL or "
            "Postgres database and one cache. "
            "3 Keep them in step: alerting servers gossip on port 9094 or use Redis; live updates need Redis, "
            "otherwise they work on one server only; each server builds its own search index. "
            "4 Watching Grafana itself: metrics for Prometheus at /metrics, OpenTelemetry tracing off by default, "
            "logs, and 398 feature flags of which 59 are generally available. Usage stats go to stats.grafana.org "
            "by default.")

d.group(L, T1, W, H1, "One program", 1)
col(L, T1, [("grafana server|web app + APIs on port 3000", "coding"),
            ("Packages|Docker, deb, rpm, Windows, Mac", "data"),
            ("Two editions|open source (AGPLv3), Enterprise", "data")], arrows=False)

d.group(R, T1, W, H1, "Several servers", 2)
col(R, T1, [("Load balancer|spreads users", "plan"),
            ("Shared database|MySQL or Postgres", "write"),
            ("Shared cache|database, Redis or Memcached", "write")], arrows=False)

d.group(R, T2, W, H2, "Keep them in step", 3)
col(R, T2, [("Alerting|gossip on port 9094, or Redis", "review"),
            ("Live streaming|needs Redis, else one server", "review"),
            ("Search index|each server builds its own", "data")], gap=20, arrows=False)

d.group(L, T2, W, H2, "Watching Grafana", 4)
col(L, T2, [("/metrics|for Prometheus to scrape", "data"),
            ("Tracing|OpenTelemetry, off by default", "data"),
            ("Feature flags|398 in all, 59 generally available", "plan")], gap=20, arrows=False)
notes(L, T2, H2, "usage stats go to stats.grafana.org by default")

handoffs("scale out", "in sync", None)

d.save(Path(__file__).with_name("ops.svg"))
