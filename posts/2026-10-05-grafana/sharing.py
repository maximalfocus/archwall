"""Grafana: sharing outside the team.  Drawn from grafana/grafana at commit 6b6eaf7: conf/defaults.ini
[snapshots] enabled, external_enabled = true, external_snapshot_url = https://snapshots.raintank.io;
pkg/api/api.go:605 (GET /api/snapshots/:key has no sign-in check); docs share-dashboards-panels (snapshot keeps
the data, strips queries and links); [public_dashboards] enabled = true; pkg/services/publicdashboards
(anyone with the link, saved queries run server-side as a service identity, time picker and annotations optional,
email sharing Enterprise plus flag publicDashboardsEmailSharing); pkg/services/rendering (image renderer at
[rendering] server_url).

Snake order: 1 a link -> 2 a snapshot -> 3 a public dashboard -> 4 an image.
Run: python3 sharing.py"""
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

d = Diagram("Grafana: sharing outside the team",
            "1 A link: points to the live dashboard; the viewer must sign in; it can be shortened; dashboards can also be exported as JSON. "
            "2 A snapshot: a copy of the data with queries and links removed; anyone with its key can view it; there "
            "is an option, shown by default, to publish it to snapshots.raintank.io. "
            "3 A public dashboard: anyone with the link can view it without signing in; it runs only the saved "
            "queries, as Grafana and not as a user; time picker and annotations are optional; sharing only with "
            "named emails is Enterprise. "
            "4 An image: a PNG of a panel or dashboard, made by the image renderer, a separate service that must be "
            "set up; scheduled PDF reports are Enterprise.")

d.group(L, T1, W, H1, "A link", 1)
col(L, T1, [("Link to the live dashboard|viewer must sign in", "data"),
            ("Short link|same view, shorter URL", "data"),
            ("Export|the dashboard as JSON", "write")], arrows=False)

d.group(R, T1, W, H1, "A snapshot", 2)
col(R, T1, [("Copy of the data|queries and links removed", "write"),
            ("Anyone with the key|can view it", "review"),
            ("Publish to raintank.io|option shown by default", "data")], arrows=False)

d.group(R, T2, W, H2, "A public dashboard", 3)
col(R, T2, [("Anyone with the link|no sign-in", "review"),
            ("Runs saved queries only|as Grafana, not as a user", "coding"),
            ("Time picker, annotations|optional", "data")], gap=20, arrows=False)
notes(R, T2, H2, "share only with named emails: Enterprise")

d.group(L, T2, W, H2, "An image", 4)
col(L, T2, [("Image renderer|separate service, must be set up", "coding"),
            ("PNG|of a panel or a whole dashboard", "write")], arrows=False)
notes(L, T2, H2, "scheduled PDF reports: Enterprise")

d.note(600, 886, "From most closed (1) to most open (3): only 3 needs no sign-in and no key")

d.save(Path(__file__).with_name("sharing.svg"))
