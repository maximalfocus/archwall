"""Grafana: what it keeps.  Drawn from grafana/grafana at commit 6b6eaf7:
contribute/architecture/k8s-inspired-backend-arch.md (/api and /apis, unified storage, resourceVersion, 409 on
conflict, resource_history, SQL instead of etcd), pkg/setting/setting_unified_storage.go:36-46 (playlists,
folders, dashboards, short URLs, preferences in unified storage), pkg/services/sqlstore/migrations (classic tables),
conf/defaults.ini ([database] type = sqlite3, mysql, postgres; [remote_cache] type = database, redis, memcached).

Layout: 1 two API doors (top left) -> 2 unified storage (top right) and 4 classic tables (bottom left)
-> 3 one SQL database (bottom right).
Run: python3 storage.py"""
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
        d.arrow(f"M{R + W / 2} {T1 + H1}V{T2 - 2}", label=b, at=(R + W / 2 + 14 + len(b) * 4.6, T1 + H1 + 25))
    if c:
        d.arrow(f"M{R} {yc}H{L + W + 2}", label=c, at=(600, yc - 12))

d = Diagram("Grafana: what it keeps",
            "1 Two API doors: the classic API under /api, where each feature has its own style, and the newer "
            "resource API under /apis, versioned and shaped like Kubernetes. /apis is meant to replace /api over time. "
            "2 Unified storage, behind /apis and, for these, /api too: dashboards, folders, playlists, short links and preferences; every change "
            "is kept with a version number, and an edit made from an old version is refused. "
            "4 Classic tables, behind /api: users, organisations, teams, data sources, alert rules, annotations, "
            "snapshots, stars and library panels. "
            "3 Both end up in one SQL database: a SQLite file by default, fine for one server, or MySQL or Postgres, "
            "needed when several servers share it. The cache also lives in this database by default; Redis or "
            "Memcached are options.")

d.group(L, T1, W, H1, "Two API doors", 1)
col(L, T1, [("Classic API|/api/..., one style per feature", None),
            ("Resource API|/apis/..., versioned, Kubernetes-style", None),
            ("Plan|/apis is meant to replace /api", "plan")], arrows=False)
notes(L, T1, H1, "dashboards and folders reach unified", "storage through either door")

d.group(R, T1, W, H1, "Unified storage", 2)
col(R, T1, [("Dashboards, folders, playlists|short links, preferences", "write"),
            ("Every change kept|with a version number", "data"),
            ("Old-version edits refused|no silent overwrite", "review")], gap=20, arrows=False)

d.group(R, T2, W, H2, "One SQL database", 3)
col(R, T2, [("SQLite file|the default, fine for one server", "write"),
            ("MySQL or Postgres|for several servers sharing it", "write")], arrows=False)
notes(R, T2, H2, "cache: here by default,", "or Redis / Memcached")

d.group(L, T2, W, H2, "Classic tables", 4)
col(L, T2, [("Users, organisations, teams|data sources, alert rules", "write"),
            ("Annotations, snapshots|stars, library panels", "write")], arrows=False)

d.arrow(f"M{L + W} {T1 + 140}H{R - 2}", label="both", at=(600, T1 + 128))
d.arrow(f"M{L + W / 2} {T1 + H1}V{T2 - 2}", label="/api", at=(L + W / 2 + 34, T1 + H1 + 21))
d.arrow(f"M{R + W / 2} {T1 + H1}V{T2 - 2}", label="rows", at=(R + W / 2 + 36, T1 + H1 + 21))
d.arrow(f"M{L + W} {T2 + 200}H{R - 2}", label="rows", at=(600, T2 + 188))

d.save(Path(__file__).with_name("storage.svg"))
