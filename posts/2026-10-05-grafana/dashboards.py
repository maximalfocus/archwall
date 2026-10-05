"""Grafana: dashboards.  Drawn from grafana/grafana at commit 6b6eaf7: kinds/dashboard/dashboard_kind.cue
(panels, templating, time, refresh, links, annotations), apps/dashboard/kinds/v2/dashboard_spec.cue (Grid, Rows,
AutoGrid, Tabs layouts), pkg/setting/setting_folder.go (nested folders, depth 4), conf/defaults.ini
(versions_to_keep = 20; [provisioning] enabled; Bitbucket and GitLab repositories Enterprise),
apps/provisioning (Git Sync repository types), pkg/services/provisioning (files at start),
pkg/setting/setting_unified_storage.go (dashboards and folders in unified storage),
pkg/storage/unified/search/bleve.go (search index per server).

Snake order: 1 how they get in -> 2 what one holds -> 3 kept in order -> 4 saved and found.
Run: python3 dashboards.py"""
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

d = Diagram("Grafana: dashboards",
            "1 How dashboards get in: built in the web app, imported from grafana.com or a JSON file, loaded from "
            "files when Grafana starts, or synced from Git (GitHub, any git server or a local folder; Bitbucket and "
            "GitLab are Enterprise). "
            "2 What a dashboard holds: panels, each a query plus a chart; variables shown as drop-downs; a time "
            "range and refresh; a layout of grid, rows, tabs or auto grid. "
            "3 Kept in order: nested folders up to 4 levels, the last 20 versions with restore, library panels "
            "reused across dashboards, playlists and stars. "
            "4 Saved and found: each dashboard is one JSON document in Grafana's database; every server keeps its "
            "own search index for finding dashboards by title, tag or folder.")

d.group(L, T1, W, H1, "How they get in", 1)
col(L, T1, [("Build in the web app|drag panels, pick queries", None),
            ("Import|from grafana.com or a JSON file", None),
            ("Files at start|a provisioning folder", None),
            ("Git Sync|GitHub, git, a local folder", None)], h=64, gap=12, arrows=False)
notes(L, T1, H1, "Git Sync to Bitbucket or GitLab: Enterprise")

d.group(R, T1, W, H1, "What one holds", 2)
col(R, T1, [("Panels|each a query plus a chart", "data"),
            ("Variables|drop-downs at the top", "data"),
            ("Time range and refresh|e.g. last 6 hours, every 30 s", "data"),
            ("Layout|grid, rows, tabs or auto grid", "data")], h=64, gap=12, arrows=False)

d.group(R, T2, W, H2, "Kept in order", 3)
col(R, T2, [("Folders|nested, up to 4 levels", "plan"),
            ("Versions|last 20 kept, restore any", "write"),
            ("Library panels|one panel reused on many", "data"),
            ("Playlists and stars|cycle on a TV, mark favourites", "data")], h=64, gap=12, arrows=False)

d.group(L, T2, W, H2, "Saved and found", 4)
col(L, T2, [("One JSON document|in Grafana's database", "write"),
            ("Search index|built on each server", "data"),
            ("Search|by title, tag or folder", "coding")])

handoffs("JSON", "dashboard", "saved")

d.save(Path(__file__).with_name("dashboards.svg"))
