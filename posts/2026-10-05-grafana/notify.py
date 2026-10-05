"""Grafana: notifications.  Drawn from grafana/grafana at commit 6b6eaf7: the embedded Alertmanager from
github.com/grafana/alerting (go.mod), pkg/services/ngalert/models/notifications.go (group_by, group_wait,
group_interval, repeat_interval, mute_time_intervals; default grouping by folder and alert name),
notifier/autogen_alertmanager.go (a rule can name a contact point directly), notifier/silence_svc.go,
api/tooling/definitions/contact_points.go (23 contact point kinds), conf/defaults.ini
[unified_alerting.screenshots] capture = false (needs the image renderer), [unified_alerting] ha_* (gossip on
9094 or Redis; by default every server evaluates every rule, ha_single_node_evaluation opt-in).

Snake order: 1 route -> 2 hold back -> 3 contact points -> 4 extras.
Run: python3 notify.py"""
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

d = Diagram("Grafana: notifications",
            "1 Route: notification policies are a tree that matches alert labels; alerts are grouped, by folder and "
            "alert name by default, and timing settings say how long to wait and how often to repeat. A rule can also "
            "name a contact point directly. "
            "2 Hold back: silences mute matching alerts for a while; mute timings mute them at set times such as "
            "nights or weekends. "
            "3 Contact points, 23 kinds: chat such as Slack, Teams, Discord and Telegram; on-call such as PagerDuty, "
            "Opsgenie and Grafana OnCall; email, webhook, Kafka, MQTT, SNS and more. "
            "4 Extras: templates shape the message; screenshots are off by default and need the image renderer; "
            "several Grafana servers share silences and send each notification once.")

d.group(L, T1, W, H1, "Route", 1)
col(L, T1, [("Notification policies|a tree that matches labels", "plan"),
            ("Grouping|folder + alert name by default", "plan"),
            ("Timing|how long to wait, when to repeat", "plan")], arrows=False)
notes(L, T1, H1, "shortcut: a rule can name", "a contact point directly")

d.group(R, T1, W, H1, "Hold back", 2)
col(R, T1, [("Silences|mute matching alerts for a while", "review"),
            ("Mute timings|e.g. nights or weekends", "review")], arrows=False)

d.group(R, T2, W, H2, "Contact points: 23 kinds", 3)
col(R, T2, [("Chat|Slack · Teams · Discord · Telegram", "write"),
            ("On-call|PagerDuty · Opsgenie · OnCall", "write"),
            ("Email · webhook|Kafka · MQTT · SNS · more", "write")], gap=20, arrows=False)

d.group(L, T2, W, H2, "Extras", 4)
col(L, T2, [("Templates|shape the message text", "write"),
            ("Screenshots (off by default)|need the image renderer", "coding"),
            ("Several servers|share silences, send once", "review")], gap=20, arrows=False)

handoffs("alerts", "notifications", None)

d.save(Path(__file__).with_name("notify.svg"))
