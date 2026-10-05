"""Four ways to reach a herdr server.  Drawn from https://github.com/herdrdev/herdr
(docs/next/website/src/content/docs/how-to-work.mdx, persistence-remote.mdx, connecting-machines.mdx,
socket-api.mdx "Protocol stability"; src/server/autodetect.rs; src/protocol/endpoint.rs
ENDPOINT_PROTOCOL_GENERATION = 1; commit e35f393).  Run: python3 clients.py

Snake order: 1 on this machine (top left) -> 2 remote attach (top right) -> 3 several machines
(bottom right) -> 4 one terminal (bottom left). The groups are alternatives; arrows inside each group
show what flows between your side and the server."""
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

d = Diagram("herdr clients",
            "1 On this machine: run herdr; it starts the background server if none is running and attaches. "
            "ctrl+b q detaches and herdr reattaches. You can also SSH to a host and run herdr there, like tmux. "
            "2 Remote attach: herdr --remote host. The remote server owns the panes and sends screens and session "
            "state over SSH; your local herdr draws the UI with your theme and keys. herdr asks before installing "
            "itself on the host. "
            "3 Several machines: herdr machine add saves SSH hosts so Local and the hosts share one window. Only "
            "the chosen host streams screens; the others send status. Lost links retry, up to two minutes apart. "
            "Profiles store no passwords or keys. "
            "4 One terminal: herdr agent attach or terminal attach puts one pane in your terminal, on Linux and macOS. "
            "Bridges can observe or control a pane over JSON lines. Client and server versions need not match.")

CW = 214


def pair(x, top, left, right, a, b, ka="write", kb="coding"):
    """Your side (left card) and the server side (right card), with what flows each way."""
    y = top + 70
    d.card(x + 24, y, left, ka, w=CW, h=80)
    d.card(x + W - 24 - CW, y, right, kb, w=CW, h=80)
    x1, x2 = x + 24 + CW, x + W - 24 - CW
    d.arrow(f"M{x1} {y + 24}H{x2 - 2}")
    d.text((x1 + x2) / 2, y + 14, a, "al")
    if b:
        d.arrow(f"M{x2} {y + 58}H{x1 + 2}")
        d.text((x1 + x2) / 2, y + 84, b, "al")


d.group(L, T1, W, H1, "On this machine", 1)
pair(L, T1, "herdr|your terminal", "Local server|starts if needed", "keys", "screens")
d.note(L + W / 2, T1 + 220, "ctrl+b q detaches · herdr reattaches")
d.card(L + 30, T1 + 260, "Or: ssh host, then herdr|all of it runs there, like tmux", "write", w=492, h=80)

d.group(R, T1, W, H1, "Remote attach", 2)
pair(R, T1, "Local herdr|draws the UI", "Remote server|owns the panes", "keys", "screens")
d.note(R + W / 2, T1 + 220, "herdr --remote host, over SSH")
d.card(R + 30, T1 + 260, "Your theme and keys|clipboard images pass through", "write", w=492, h=80)
d.note(R + W / 2, T1 + 380, "asks before installing herdr there")

d.group(R, T2, W, H2, "Several machines", 3)
y3 = T2 + 70
d.card(R + 24, y3, "One window|Local + saved hosts", "write", w=CW, h=80)
d.card(R + W - 24 - CW, y3, "Each host|its own server", "coding", w=CW, h=80)
d.arrow(f"M{R + W - 24 - CW} {y3 + 24}H{R + 24 + CW + 2}")
d.text(R + W / 2, y3 + 14, "screens", "al")
d.arrow(f"M{R + W - 24 - CW} {y3 + 58}H{R + 24 + CW + 2}")
d.text(R + W / 2, y3 + 84, "status", "al")
d.card(R + 30, T2 + 194, "herdr machine add host|only the chosen host streams screens", "plan", w=492, h=80)
d.note(R + W / 2, T2 + 318, "lost link: retries, up to 2 min apart")
d.note(R + W / 2, T2 + 348, "stores no passwords or keys")

d.group(L, T2, W, H2, "One terminal", 4)
pair(L, T2, "Your terminal|full screen", "One pane|an agent or shell", "keys", "screens")
d.note(L + W / 2, T2 + 220, "herdr agent attach reviewer")
d.card(L + 30, T2 + 254, "observe / control|for bridges, JSON lines", "plan", w=492, h=80)
d.note(L + W / 2, T2 + 370, "Linux and macOS only")

d.note(600, 884, "client and server versions need not match")
d.save(Path(__file__).with_name("clients.svg"))
