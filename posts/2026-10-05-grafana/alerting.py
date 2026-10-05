"""Grafana: alert rules.  Drawn from grafana/grafana at commit 6b6eaf7:
pkg/services/ngalert/models/alert_rule.go (queries, condition, interval, For, KeepFiringFor, labels, annotations,
NoDataState, ExecErrState), pkg/setting/setting_unified_alerting.go:63-65 (10 s tick, 60 s default interval),
pkg/services/ngalert/eval/eval.go (same expression pipeline as panels; six states incl. Recovering),
schedule/recording_rule.go and conf/defaults.ini [recording_rules] enabled = true,
[unified_alerting.state_history] (annotations by default, Loki or Prometheus), api/lotex_ruler.go (rules kept
in Prometheus/Loki/Mimir are evaluated there), models/admin_configuration.go (internal, external or both
Alertmanagers).

Snake order: 1 an alert rule -> 2 the scheduler -> 3 state of each alert -> 4 hand-off.
Run: python3 alerting.py"""
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

d = Diagram("Grafana: alert rules",
            "1 An alert rule: queries and a condition (for example CPU above 90 percent), how often to check and how "
            "long it must hold, and labels and notes that say who it is for. "
            "2 The scheduler ticks every 10 seconds and runs rules that are due (every minute by default) through the "
            "same query engine as panels. Recording rules, on by default, save a result as a new metric. "
            "3 State of each alert: Normal, Pending, Alerting, then Recovering on the way back; No data and Error are "
            "handled as each rule says; history goes to annotations by default, or Loki or Prometheus. "
            "4 Hand-off: firing alerts go to the built-in Alertmanager, one per organisation, or to an external "
            "Alertmanager, or both. Rules kept inside Prometheus, Loki or Mimir are checked there; Grafana only "
            "shows and edits them.")

d.group(L, T1, W, H1, "An alert rule", 1)
col(L, T1, [("Queries + condition|e.g. CPU above 90%", "plan"),
            ("How often, how long|e.g. every 1 min, holds 5 min", "plan"),
            ("Labels and notes|who it is for, what to do", "data")], arrows=False)
notes(L, T1, H1, "rules kept in Prometheus or Loki are", "checked there; Grafana only shows them")

d.group(R, T1, W, H1, "The scheduler", 2)
col(R, T1, [("Ticks every 10 s|runs the rules that are due", "plan"),
            ("Runs the queries|same engine as panels", "coding"),
            ("Recording rules|save a result as a new metric", "write")], arrows=False)

d.group(R, T2, W, H2, "State of each alert", 3)
col(R, T2, [("Normal → Pending → Alerting|Recovering on the way back", "critic"),
            ("No data · Error|each rule says how to treat them", "critic"),
            ("History|annotations, or Loki / Prometheus", "data")], gap=20, arrows=False)

d.group(L, T2, W, H2, "Hand-off", 4)
col(L, T2, [("Built-in Alertmanager|one per organisation", "plan"),
            ("External Alertmanager|instead of it, or as well", "plan")], arrows=False)
notes(L, T2, H2, "next: notification policies,", "silences, contact points")

handoffs("rules", "results", "firing")

d.save(Path(__file__).with_name("alerting.svg"))
