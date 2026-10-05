"""Grafana: how a panel gets its data.  Drawn from grafana/grafana at commit 6b6eaf7:
packages/grafana-runtime/src/utils/DataSourceWithBackend.ts (POST /api/ds/query),
public/app/core/services/FetchQueueWorker.ts (5 parallel, 1000 with HTTP/2), pkg/api/api.go:503 (datasources:query),
pkg/services/query/query.go (group by data source, run in parallel), pkg/expr (math, reduce, resample, threshold, SQL),
pkg/services/pluginsintegration/coreplugin/coreplugins.go (built-in backends), grpcplugin (external over gRPC),
pkg/api/pluginproxy/ds_proxy.go (proxy adds stored credentials), pkg/services/caching/service.go (OSS cache is a no-op),
packages/grafana-data/src/transformations (transformations run in the browser).

Snake order: 1 in the browser -> 2 on the server -> 3 fetch from the source -> 4 back to the panel.
Run: python3 query.py"""
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

d = Diagram("Grafana: how a panel gets its data",
            "1 In the browser: a panel builds its query with the dashboard's time range and variables; a queue "
            "sends at most 5 data requests at a time, or 1000 with HTTP/2, and sends them to /api/ds/query. "
            "2 On the server: Grafana checks the caller is signed in and may query data sources, then the query "
            "service splits the request by data source and runs them in parallel, up to one per CPU core by default. In open source any member of an "
            "organisation may query any data source; per data source permissions are Enterprise. "
            "3 Fetch from the source: a data source plugin asks your system. A few plugins are built into Grafana; "
            "the rest run as their own program and talk to Grafana over gRPC. Browser-only plugins go through "
            "a proxy that adds the stored password. "
            "4 Back to the panel: answers come back as data frames; optional expressions do maths, reduce, "
            "resample or SQL on the server, transformations join or filter in the browser, and the visualization "
            "draws the result. Query caching is Enterprise only.")

d.group(L, T1, W, H1, "In the browser", 1)
col(L, T1, [("Panel builds its query|with time range and variables", "coding"),
            ("Request queue|5 at a time, 1000 with HTTP/2", "plan"),
            ("Send to the server|POST /api/ds/query", "coding")], gap=20)
notes(L, T1, H1, "Explore in the browser sends", "the same call")

d.group(R, T1, W, H1, "On the server", 2)
col(R, T1, [("Check the caller|signed in, may query data sources", "review"),
            ("Split by data source|one query list per source", "plan"),
            ("Run them in parallel|up to one per CPU core", "plan")], gap=20)
notes(R, T1, H1, "open source: members may query any source", "per-source permissions: Enterprise")

d.group(R, T2, W, H2, "Fetch from the source", 3)
col(R, T2, [("Built-in plugin|runs inside Grafana", "coding"),
            ("Installed plugin|own program, talks gRPC", "coding"),
            ("Your system answers|Prometheus, MySQL, CloudWatch ...", "data")], gap=20, arrows=False)
notes(R, T2, H2, "browser-only plugins use a proxy", "that adds the stored password")

d.group(L, T2, W, H2, "Back to the panel", 4)
col(L, T2, [("Expressions (optional)|maths, reduce, SQL on the server", "coding"),
            ("Transformations|join, filter, rename in the browser", "coding"),
            ("Visualization draws it|time series, table, gauge ...", "write")], gap=20)
notes(L, T2, H2, "query caching: Enterprise only")

handoffs("request", "one call per source", "frames")

d.save(Path(__file__).with_name("query.svg"))
