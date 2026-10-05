"""herdr server main loop: wait, apply, run scheduled jobs, draw and send.  Drawn from
https://github.com/herdrdev/herdr (src/server/headless.rs HeadlessServer::run, src/app/session.rs and
src/app/mod.rs SESSION_SAVE_DEBOUNCE = 5 s, AGENTS.md "Multiplicative performance paths", Cargo.toml zbus
note for logind; commit e35f393).  Run: python3 loop.py

Snake order: 1 wait for something (top left) -> 2 apply it (top right) -> 3 scheduled jobs
(bottom right) -> 4 draw and send (bottom left) -> back to 1."""
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

d = Diagram("herdr server loop",
            "1 Wait for something: output from a pane, keys or clicks from a client, a request on the API socket, "
            "or a timer. "
            "2 Apply it: update the shared state (panes, agents, layout) and re-check agent status from the screen "
            "and the agents' reports. "
            "3 Scheduled jobs: save session.json 5 seconds after the last change, and drop short-lived labels whose "
            "time is up. "
            "4 Draw and send: render only what some client can see; hidden panes still read their output so status "
            "stays current. Stream screens and session state to clients, then wait again. "
            "When the server stops it saves once more; on Linux with logind it asks for a short delay at shutdown to save.")

d.group(L, T1, W, H1, "Wait for something", 1)
grid(L, T1, [("Pane output|from each terminal", "data"), ("Keys, clicks|from clients", "write"),
             ("API requests|CLI, agents, plugins", "plan"), ("Timers|saves, expiries", "data")], h=88, gap=20)

d.group(R, T1, W, H1, "Apply it", 2)
col(R, T1, [("Update shared state|panes, agents, layout", "coding"),
            ("Re-check agent status|screen + reports", "critic")], h=80)

d.group(R, T2, W, H2, "Scheduled jobs", 3)
col(R, T2, [("Save session.json|5 s after the last change", "write"),
            ("Drop expired labels|short-lived metadata", "data")], h=80, arrows=False)
d.note(R + W / 2, T2 + 300, "on stop: one last save")
d.note(R + W / 2, T2 + 328, "Linux + logind: delays shutdown to save")

d.group(L, T2, W, H2, "Draw and send", 4)
col(L, T2, [("Render what someone sees|hidden panes still update", "coding"),
            ("Stream to clients|screens + session state", "write")], h=80)

handoffs("event", "changes", "due")
d.arrow(f"M{L + 60} {T2}V{T1 + H1 + 2}", label="wait again", at=(L + 130, T1 + H1 + 21))
d.save(Path(__file__).with_name("loop.svg"))
