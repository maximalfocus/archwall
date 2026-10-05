"""herdr data model: session > workspace > tab > pane, and the agent inside a pane.  Drawn from
https://github.com/herdrdev/herdr (docs/next/website/src/content/docs/concepts.mdx, agent-automation.mdx,
persistence-remote.mdx; src/persist/snapshot.rs; src/layout.rs; commit e35f393).  Run: python3 model.py

Snake order: 1 session (top left) -> 2 workspace (top right) -> 3 tab (bottom right)
-> 4 pane and agent (bottom left)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

L, R, W = 24, 624, 552
T1, H1 = 16, 412
T2, H2 = 460, 400


def col(x, top, cards, h=72, gap=24, arrows=True):
    """One column of wide cards, top to bottom, optionally joined by arrows."""
    for i, (lbl, kind) in enumerate(cards):
        y = top + 64 + i * (h + gap)
        d.card(x + 30, y, lbl, kind, w=492, h=h)
        if arrows and i:
            d.arrow(f"M{x + W / 2} {y - gap}V{y - 2}")


def grid(x, top, cards, h=80, gap=16, y0=64):
    """Two columns of cards, filled row by row."""
    for i, (lbl, kind) in enumerate(cards):
        d.card(x + 30 + (i % 2) * 254, top + y0 + (i // 2) * (h + gap), lbl, kind, w=238, h=h)


def handoffs(a, b, c, ya=T1 + 206, yc=T2 + 200):
    """Arrows between the four groups in snake order, with what each one carries."""
    if a:
        d.arrow(f"M{L + W} {ya}H{R - 2}", label=a, at=(600, ya - 12))
    if b:
        d.arrow(f"M{R + W / 2} {T1 + H1}V{T2 - 2}", label=b, at=(R + W / 2 + 14 + len(b) * 4.6, T1 + H1 + 21))
    if c:
        d.arrow(f"M{R} {yc}H{L + W + 2}", label=c, at=(600, yc - 12))

d = Diagram("herdr data model",
            "1 Session: one herdr server with its own panes, sockets and saved state. herdr attaches to the "
            "default session; named sessions such as herdr session attach work are separate servers sharing one config file. "
            "2 Workspace: the top-level container, one per repo, task or investigation. Its status rolls up from "
            "the agents inside it. IDs look like w1. "
            "3 Tab: a layout inside a workspace, such as agents, logs or review, kept as a split tree; panes split "
            "right or down. IDs look like w1:t1. "
            "4 Pane and agent: a pane is a real terminal with an ID like w1:p1. An agent is a process herdr "
            "recognises in a pane and may carry a name such as reviewer. Each pane saves its directory, label and "
            "agent session reference.")

d.group(L, T1, W, H1, "Session", 1)
col(L, T1, [("One herdr server|own panes, sockets, saved state", "coding"),
            ("Named sessions|herdr session attach work", "data")], h=80, arrows=False)
d.note(L + W / 2, T1 + 300, "plain herdr: the default session")
d.note(L + W / 2, T1 + 328, "all sessions share one config file")

d.group(R, T1, W, H1, "Workspace", 2)
col(R, T1, [("One per repo or task|top-level container", "data"),
            ("Status rolls up|a blocked agent marks it blocked", "critic")], h=80, arrows=False)
d.note(R + W / 2, T1 + 300, "IDs like w1")

d.group(R, T2, W, H2, "Tab", 3)
col(R, T2, [("A layout|agents, logs, review …", "data"),
            ("Split tree|panes split right or down", "data")], h=80, arrows=False)
d.note(R + W / 2, T2 + 300, "IDs like w1:t1")

d.group(L, T2, W, H2, "Pane and agent", 4)
col(L, T2, [("Pane|a real terminal, ID w1:p1", "coding"),
            ("Agent|a process herdr knows, e.g. reviewer", "critic"),
            ("Saved per pane|folder, label, agent session", "write")], arrows=False)

handoffs("holds", "holds", "holds")
d.save(Path(__file__).with_name("model.svg"))
