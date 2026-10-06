"""Triggers: provider events, by polling or by webhook; Open Flow drives them.
Drawn from oomol-lab/open-connector at commit 20c6c44 (docs/runtime-api.md "Provider Triggers",
docs/catalog-format.md "Trigger metadata", docs/cloudflare.md, src/triggers/).
Run: python3 triggers.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, R, GW, T1, H1, T2, H2  # noqa: E402

d = Diagram("Triggers",
            "In: Open Flow, a separate workflow engine, which owns the public webhook address, scheduling, "
            "checkpoints and de-duplication. "
            "1 Poll: a read operation with the last checkpoint returns at most 100 events a page; when hasMore is "
            "true, read again to get the next page. "
            "2 Webhook: reconcile creates or keeps the provider's hook and returns an opaque subscription ID; "
            "receive checks the provider's signature or secret on bodies up to 64 KiB. "
            "3 State: subscriptions are stored encrypted with SQL leases in SQLite, PostgreSQL or D1; stateful "
            "operations need a persistent token, and triggers work only with locally stored connections. "
            "4 Cleanup: a maintenance loop in Node, or a once-a-minute cron on Workers, removes revoked hooks; "
            "admins can cancel or abandon a subscription.")

d.pill(L, 16, GW, 48, "In: Open Flow, the workflow engine")
d.arrow(f"M{L + GW / 2} 64V{T1 - 2}")

d.group(L, T1, GW, H1, "Poll", 1)
d.column(L, T1, [("read|with the last checkpoint", "coding"),
                 ("≤ 100 events a page|hasMore → read again", "data")])
d.notes(L, T1, H1, "Open Flow keeps checkpoints,", "schedules and de-duplicates")

d.group(R, T1, GW, H1, "Webhook", 2)
d.column(R, T1, [("reconcile|create / keep the provider hook", "coding"),
                 ("receive|check signature · ≤ 64 KiB", "review")])
d.notes(R, T1, H1, "Hook IDs and secrets", "stay on the server")

d.group(R, T2, GW, H2, "State", 3)
d.column(R, T2, [("Subscriptions|encrypted · SQL leases", "write"),
                 ("Persistent token|needed for stateful ops", "review")])
d.notes(R, T2, H2, "Local connections only:", "not SaaS or Marketplace")

d.group(L, T2, GW, H2, "Cleanup", 4)
d.column(L, T2, [("Maintenance|Node loop · Workers cron", "plan"),
                 ("Admin|cancel · abandon", "review")])

d.arrow(f"M{L + GW} {T1 + 140}H{R - 2}", label="or", at=(600, T1 + 128))
d.arrow(f"M{R + 430} {T1 + H1}V{T2 - 2}", label="subscription", at=(R + 430, T1 + H1 + 24))
d.arrow(f"M{R} {T2 + 176}H{L + GW + 2}", label="revoked", at=(600, T2 + 164))

d.save(Path(__file__).with_name("triggers.svg"))
