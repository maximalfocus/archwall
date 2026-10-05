"""herdr control API: who calls it, how, what it can do, and what comes back.  Drawn from
https://github.com/herdrdev/herdr (docs/next/website/src/content/docs/socket-api.mdx, agent-automation.mdx,
agent-skill.mdx, plugins.mdx; skills/herdr/SKILL.md; src/api/server.rs SOCKET_PERMISSION_MODE = 0o600;
commit e35f393).  Run: python3 api.py

Snake order: 1 who calls (top left) -> 2 how it gets there (top right) -> 3 what it can do
(bottom right) -> 4 what comes back (bottom left) -> back to 1."""
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

d = Diagram("herdr control API",
            "1 Who calls: an agent in a pane, using the herdr skill if installed; scripts; plugins. Every pane gets "
            "HERDR_PANE_ID and HERDR_SOCKET_PATH. "
            "2 How it gets there: the herdr CLI wraps every call; underneath is a local socket with one JSON "
            "request per line (a Unix socket, owner-only, or a Windows named pipe). herdr api schema prints the contract. "
            "3 What it can do: layout (workspace, tab, split), panes (run, read, wait for output), agents (start, "
            "prompt, wait until idle, done or blocked), and event subscriptions. "
            "4 What comes back: a JSON reply with IDs to capture, and an event stream of status changes. A reader "
            "that falls behind gets events_lost and re-reads a snapshot.")

d.group(L, T1, W, H1, "Who calls", 1)
col(L, T1, [("Agent in a pane|uses the herdr skill, if installed", "plan"),
            ("Scripts|shell, CI", "plan"),
            ("Plugins|actions and hooks", "plan")], arrows=False)

d.group(R, T1, W, H1, "How it gets there", 2)
col(R, T1, [("herdr CLI|wraps every call", "write"),
            ("Local socket|one JSON request per line", "data")], h=80)
d.note(R + W / 2, T1 + 300, "owner-only on Unix · pipe on Windows")
d.note(R + W / 2, T1 + 328, "herdr api schema prints the contract")

d.group(R, T2, W, H2, "What it can do", 3)
grid(R, T2, [("Layout|workspace · tab · split", "plan"), ("Panes|run · read · wait", "coding"),
             ("Agents|start · prompt · wait", "coding"), ("Events|subscribe", "data")], h=80)
d.note(R + W / 2, T2 + 290, "agent wait: until idle, done or blocked")

d.group(L, T2, W, H2, "What comes back", 4)
col(L, T2, [("JSON reply|IDs to capture, not guess", "data"),
            ("Event stream|status changes, new panes", "data")], h=80, arrows=False)
d.note(L + W / 2, T2 + 300, "falls behind? events_lost: re-read")

handoffs("commands", "requests", "replies")
d.arrow(f"M{L + 60} {T2}V{T1 + H1 + 2}", label="answers", at=(L + 120, T1 + H1 + 21))
d.note(L + W / 2, T1 + 380, "every pane gets HERDR_PANE_ID")
d.save(Path(__file__).with_name("api.svg"))
