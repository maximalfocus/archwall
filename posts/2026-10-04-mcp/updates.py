"""How MCP clients hear about changes: subscriptions/listen.  Drawn from
https://modelcontextprotocol.io/docs/learn/architecture (Notifications; Example step Real-time Updates)
and https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/subscriptions (Notification
Filter, Acknowledgment, Receiving Notifications, Cancellation) and .../changelog (major change 4:
request-scoped notifications stay on their own request's stream).
Protocol version 2026-07-28, read 2026-10-05.  Run: python3 updates.py

Snake order: 1 the client opens a stream (top left) -> 2 the server confirms (top right) ->
3 notices arrive (bottom right) -> 4 the client refreshes (bottom left)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

L, R, W = 24, 624, 552
T1, H1 = 16, 412
T2, H2 = 460, 400


def grid(x, top, cards, h=64, gap=16, y0=64):
    """Two columns of cards, filled row by row."""
    for i, (lbl, kind) in enumerate(cards):
        d.card(x + 30 + (i % 2) * 254, top + y0 + (i // 2) * (h + gap), lbl, kind, w=238, h=h)


def col(x, top, cards, h=72, gap=48, y0=64, arrows=True):
    """One column of wide cards, top to bottom, optionally joined by arrows."""
    for i, (lbl, kind) in enumerate(cards):
        y = top + y0 + i * (h + gap)
        d.card(x + 30, y, lbl, kind, w=492, h=h)
        if arrows and i:
            d.arrow(f"M{x + W / 2} {y - gap}V{y - 2}")


d = Diagram("How clients hear about changes",
            "1 The client opens a long-lived stream with subscriptions/listen and names what it wants: tool list "
            "changes, prompt list changes, resource list changes, or updates to particular resources. Nothing is "
            "sent unless asked for. "
            "2 The server confirms with an acknowledgment listing what it will send; types it does not support "
            "are left out, and list changes only come from servers that declared them. "
            "3 Notices such as notifications/tools/list_changed or notifications/resources/updated arrive on "
            "the stream, each tagged with the stream's id. Delivery is best effort, so clients poll as well. "
            "4 The client refreshes, for example with tools/list, and the host gives the model the new list. If "
            "the stream is lost, the client sends listen again. Progress notices travel on the reply of their own "
            "request, not on this stream.")

d.group(L, T1, W, H1, "Client opens a stream", 1)
d.card(L + 30, T1 + 64, "subscriptions/listen|names what it wants", "coding", w=492, h=72)
grid(L, T1, [("Tool list|changed", "data"), ("Prompt list|changed", "data"),
             ("Resource list|changed", "data"), ("One resource|updated", "data")], y0=160)
d.note(L + W / 2, T1 + 352, "opt-in: nothing comes unless asked")

d.group(R, T1, W, H1, "Server confirms", 2)
col(R, T1, [("acknowledged|what it will send", "plan")], arrows=False)
d.card(R + 30, T1 + 184, "Stream stays open", "data", w=492, h=60)
d.arrow(f"M{R + W / 2} {T1 + 136}V{T1 + 182}")
d.note(R + W / 2, T1 + 324, "types it can't do are left out;")
d.note(R + W / 2, T1 + 352, "list changes only if it declared them")

d.group(R, T2, W, H2, "Notices arrive", 3)
col(R, T2, [("notifications/tools/list_changed|the tool list changed", "data"),
            ("notifications/resources/updated|one resource changed", "data")], h=72, gap=24, arrows=False)
d.note(R + W / 2, T2 + 326, "each tagged with the stream's id;")
d.note(R + W / 2, T2 + 354, "best effort, so clients poll as well")

d.group(L, T2, W, H2, "Client refreshes", 4)
col(L, T2, [("tools/list again|fetch the new list", "coding"), ("New tools|reach the model", "plan")])
d.note(L + W / 2, T2 + 354, "stream lost? the client sends listen again")

d.arrow(f"M{L + W} {T1 + 100}H{R - 2}", label="filter", at=(600, T1 + 88))
d.arrow(f"M{R + W / 2} {T1 + H1}V{T2 - 2}", label="notices", at=(R + W / 2 + 50, T1 + H1 + 21))
d.arrow(f"M{R} {T2 + 182}H{L + W + 2}", label="notice", at=(600, T2 + 170))

d.note(600, 888, "Progress notices travel on the reply of their own request, not on this stream")

d.save(Path(__file__).with_name("updates.svg"))
