"""Grafana: plugins.  Drawn from grafana/grafana at commit 6b6eaf7: pkg/plugins/plugins.go (types),
pkg/services/pluginsintegration/pipeline/pipeline.go (discovery keeps datasource, app, panel),
pkg/plugins/manager/pipeline/doc.go (discovery, bootstrap, validation, initialization),
pkg/setting/setting_plugins.go:35-55 (18 preinstalled plugins), public/app/plugins/panel (28 panels),
pkg/plugins/models.go (signature types), pkg/plugins/manager/signature/authorizer.go (unsigned only in dev mode
or allow_loading_unsigned_plugins), pkg/plugins/backendplugin/grpcplugin (separate process over gRPC),
public/app/features/plugins/importer (module.js loaded in the browser), conf/defaults.ini [plugins].

Snake order: 1 three kinds -> 2 where they come from -> 3 loading checks -> 4 two halves at run time.
Run: python3 plugins.py"""
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

d = Diagram("Grafana: plugins",
            "1 Three kinds of plugin: a data source connects to a system, a panel is a way to draw data, an app adds "
            "whole pages and dashboards, such as the Drilldown apps. "
            "2 Where they come from: built in (28 panels and a few data sources), installed at start from "
            "grafana.com (18 by default, including Prometheus, Loki, MySQL and the Drilldown apps), or added by an "
            "admin from the catalog. "
            "3 Loading checks: Grafana finds each plugin and reads its plugin.json, checks its signature "
            "(Grafana, commercial, community or private; unsigned plugins are blocked unless allowed by name), "
            "then starts it and registers its permissions. "
            "4 Two halves at run time: the front half is JavaScript loaded in the browser; the back half, if any, "
            "is its own program that talks to Grafana over gRPC; apps can also add links and parts to other pages.")

d.group(L, T1, W, H1, "Three kinds", 1)
col(L, T1, [("Data source|connects to one kind of system", "coding"),
            ("Panel|one way to draw data", "write"),
            ("App|whole pages, e.g. Drilldown", "plan")], arrows=False)

d.group(R, T1, W, H1, "Where they come from", 2)
col(R, T1, [("Built in|28 panels, a few data sources", "data"),
            ("Installed at start|18 by default, from grafana.com", "data"),
            ("Catalog|admins add more", "data")], arrows=False)
notes(R, T1, H1, "Prometheus, Loki, MySQL ... are installed,", "not built in")

d.group(R, T2, W, H2, "Loading checks", 3)
col(R, T2, [("Find it|read plugin.json", "plan"),
            ("Check the signature|unsigned: blocked by default", "review"),
            ("Start it|run its program, add permissions", "coding")], gap=20)
notes(R, T2, H2, "signed by Grafana, a company, the", "community, or privately for one site")

d.group(L, T2, W, H2, "Two halves at run time", 4)
col(L, T2, [("Front half|JavaScript in the browser", "coding"),
            ("Back half (if any)|own program, talks gRPC", "coding"),
            ("Extension points|apps add links to other pages", "plan")], arrows=False)
notes(L, T2, H2, "back half: queries, health checks,", "streaming, its own HTTP routes")

handoffs("ships as", "plugin files", "running")

d.save(Path(__file__).with_name("plugins.svg"))
