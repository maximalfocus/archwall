"""herdr overview: who draws, who runs the agents, who tells you which one is stuck, and what comes
back after a restart.  Drawn from https://github.com/herdrdev/herdr (README.md, AGENTS.md,
docs/next/website/src/content/docs: concepts, agents, session-state, socket-api; src/server/headless.rs;
commit e35f393).  Run: python3 diagram.py

Snake order: 1 clients (top left) -> 2 server, one per session (top right) -> 3 control API
(bottom right) -> 4 if the server stops (bottom left)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("herdr overview",
            "1 Clients: a local window, a client over SSH to one or more machines, or a direct attach "
            "to one terminal. Clients draw the screen and send keys; ctrl+b q detaches and the agents keep running. "
            "2 Server, one per session: each pane is a real terminal running an agent, read into screen "
            "state by libghostty-vt. A screen check against 22 agent manifests and the agents' own reports "
            "decide working, blocked, done or idle. "
            "3 Control API: agents in panes, scripts and plugins call the server through the herdr CLI or a "
            "local socket to spawn panes, prompt agents and wait on them. "
            "4 If the server stops, the processes are gone; herdr brings back what it can: live handoff during "
            "updates (experimental, --handoff), the agent's own resume (needs its integration), pane history "
            "(opt-in) and the saved layout in session.json.")
A, B, GW = 24, 632, 544
TOP, TH = 16, 420
BOT, BH = 468, 384

# 1 clients (top left)
d.group(A, TOP, GW, TH, "Clients", 1)
d.sub(A + 12, 66, GW - 24, 150, "Draw the screen, send keys")
for i, t in enumerate(["Local|window", "Over SSH|1 or more hosts", "One terminal|direct attach"]):
    d.card(A + 24 + i * 172, 108, t, "write", w=160, h=72)
d.sub(A + 12, 230, GW - 24, 190, "Detach")
d.card(A + 30, 276, "ctrl+b q", "plan", w=180, h=72)
d.card(A + 342, 276, "Agents keep|running", "coding", w=180, h=72)
d.arrow(f"M{A + 210} 312H{A + 336}")
d.note(A + GW / 2, 392, "close the laptop or lose SSH: work goes on")

d.arrow(f"M{A + GW} 128H{B}", label="keys", at=(600, 118))
d.arrow(f"M{B} 170H{A + GW}", label="screens", at=(600, 194))

# 2 server (top right)
d.group(B, TOP, GW, TH, "Server, one per session", 2)
d.sub(B + 12, 66, GW - 24, 130, "Each pane")
d.card(B + 24, 108, "Real terminal|claude, codex …", "coding", w=210, h=72)
d.card(B + 318, 108, "Screen state|libghostty-vt", "data", w=210, h=72)
d.arrow(f"M{B + 234} 144H{B + 312}", label="output", at=(B + 276, 134))
d.sub(B + 12, 212, GW - 24, 208, "Who needs you?")
d.card(B + 298, 254, "Screen check|22 agent manifests", "critic", w=230, h=64)
d.card(B + 298, 334, "Agent's own report|via integrations", "critic", w=230, h=64)
d.card(B + 24, 280, "working · blocked|done · idle", "data", w=206, h=76)
d.arrow(f"M{B + 423} 180V248")
d.arrow(f"M{B + 298} 290H{B + 236}")
d.arrow(f"M{B + 298} 366H{B + 264}V336H{B + 236}")
d.note(B + 127, 392, "rolls up to tab, workspace")

# 3 control API (bottom right)
d.group(B, BOT, GW, BH, "Control API", 3)
d.sub(B + 12, BOT + 46, GW - 24, 150, "Who calls it")
d.card(B + 24, BOT + 92, "Agents in panes|spawn · prompt · wait", "plan", w=250, h=72)
d.card(B + 308, BOT + 92, "Scripts|and plugins", "plan", w=220, h=72)
d.sub(B + 12, BOT + 210, GW - 24, 162, "How")
d.card(B + 24, BOT + 256, "herdr CLI|wraps every call", "write", w=230, h=72)
d.card(B + 298, BOT + 256, "Local socket|JSON lines", "data", w=230, h=72)

d.arrow(f"M{B + 470} {TOP + TH}V{BOT}", label="events", at=(B + 512, 458))
d.arrow(f"M{B + 400} {BOT}V{TOP + TH}", label="commands", at=(B + 348, 458))

# 4 restart and restore (bottom left)
d.group(A, BOT, GW, BH, "If the server stops", 4)
d.sub(A + 12, BOT + 46, GW - 24, 326, "Bring back what it can")
rows = [("Live handoff|keeps the processes", "coding", "updates, experimental"),
        ("Agent resume|claude --resume <id>", "plan", "needs its integration"),
        ("Pane history", "data", "opt-in, may hold secrets"),
        ("Saved layout|session.json", "write", "fresh shell, same dir")]
for i, (t, k, n) in enumerate(rows):
    y = BOT + 90 + i * 68
    d.card(A + 30, y, t, k, w=270, h=60)
    d.note(A + 316, y + 36, n, "start")

d.arrow(f"M{B + 60} {TOP + TH}V452H{A + GW / 2}V{BOT}", label="save", at=(A + GW / 2 + 70, 458))

d.note(600, 884, "one Rust binary · the server owns shared facts; each client draws its own look")

d.save(Path(__file__).with_name("diagram.svg"))
