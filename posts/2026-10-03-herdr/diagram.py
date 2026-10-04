"""herdr architecture, drawn from the repo docs (concepts, session state, socket API) at
https://github.com/herdrdev/herdr (commit 5da0a01).  Run: python3 diagram.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("herdr architecture",
            "1 Clients (local TUI, remote over SSH, direct attach) only draw and send keys; detaching leaves work running. "
            "2 One server per session owns every pane: a real PTY running the agent, parsed into terminal state by "
            "libghostty-vt. A screen detector and the agents' own reports decide working, blocked or idle; "
            "a finished pane you have not looked at shows done. "
            "3 A socket API lets agents and scripts spawn panes, prompt each other and wait on state. "
            "4 If the server stops, herdr restores what it can: live handoff, the agent's resume command, "
            "opt-in pane history, and the saved layout.")
A, B, GW = 24, 632, 544   # 64px gutter so arrow labels fit between columns
TOP, TH = 16, 420    # top row
BOT, BH = 468, 384   # bottom row

# 1 clients (top left)
d.group(A, TOP, GW, TH, "Clients", 1)
d.sub(A + 12, 66, GW - 24, 150, "Draw the screen, send keys")
for i, t in enumerate(["Local|TUI", "Remote|over SSH", "Direct attach|one terminal"]):
    d.card(A + 24 + i * 172, 108, t, w=160, h=72)
d.sub(A + 12, 230, GW - 24, 190, "Detach")
d.card(A + 30, 276, "ctrl+b q", "plan", w=180, h=72)
d.card(A + 342, 276, "Agents keep|running", "coding", w=180, h=72)
d.arrow(f"M{A + 210} 312H{A + 336}")
d.note(A + GW / 2, 392, "close the laptop or lose SSH: work goes on")

# clients <-> server
d.arrow(f"M{A + GW} 128H{B}", label="keys", at=(600, 118))
d.arrow(f"M{B} 170H{A + GW}", label="screen", at=(600, 194))

# 2 server (top right)
d.group(B, TOP, GW, TH, "Server, one per session", 2)
d.sub(B + 12, 66, GW - 24, 130, "Each pane")
d.card(B + 24, 108, "PTY + process|claude, codex …", "coding", w=210, h=72)
d.card(B + 318, 108, "Terminal state|libghostty-vt", "data", w=210, h=72)
d.arrow(f"M{B + 234} 144H{B + 312}", label="output", at=(B + 276, 134))
d.sub(B + 12, 212, GW - 24, 208, "Who is stuck?")
d.card(B + 298, 254, "Screen detector|22 agent manifests", "critic", w=230, h=64)
d.card(B + 298, 334, "Agent's own report|newest seq wins", "write", w=230, h=64)
d.card(B + 24, 280, "working · blocked|done · idle", "review", w=206, h=76)
d.arrow(f"M{B + 423} 180V248")
d.arrow(f"M{B + 298} 290H{B + 236}")
d.arrow(f"M{B + 298} 366H{B + 264}V336H{B + 236}")
d.note(B + 127, 392, "per pane and per workspace")

# 3 control API (bottom right)
d.group(B, BOT, GW, BH, "Control API", 3)
d.sub(B + 12, BOT + 46, GW - 24, 150, "Socket API for agents and scripts")
d.card(B + 24, BOT + 92, "Agents in panes|spawn · prompt · wait", "plan", w=250, h=72)
d.card(B + 308, BOT + 92, "Scripts|and plugins", "write", w=220, h=72)
d.sub(B + 12, BOT + 210, GW - 24, 162, "Every pane gets")
d.card(B + 24, BOT + 256, "HERDR_PANE_ID|HERDR_SOCKET_PATH", "data", w=260, h=72)
d.note(B + 302, BOT + 286, "agent wait: returns when", "start")
d.note(B + 302, BOT + 310, "another agent is blocked", "start")

# server <-> control API
d.arrow(f"M{B + 470} {TOP + TH}V{BOT}", label="events", at=(B + 512, 458))
d.arrow(f"M{B + 400} {BOT}V{TOP + TH}", label="commands", at=(B + 348, 458))

# 4 restart and restore (bottom left)
d.group(A, BOT, GW, BH, "If the server stops", 4)
d.sub(A + 12, BOT + 46, GW - 24, 326, "Bring back what it can")
rows = [("Live handoff|best effort", "coding", "during updates, opt-in"),
        ("Resume command|claude --resume <id>", "plan", "same conversation"),
        ("Pane history", "data", "opt-in, may hold secrets"),
        ("Saved layout|session.json", "data", "fresh shell, same dir")]
for i, (t, k, n) in enumerate(rows):
    y = BOT + 90 + i * 68
    d.card(A + 30, y, t, k, w=270, h=60)
    d.note(A + 318, y + 36, n, "start")

d.arrow(f"M{B + 60} {TOP + TH}V452H{A + GW / 2}V{BOT}", label="save", at=(A + GW / 2 + 70, 458))

d.note(600, 884, "one Rust binary · shared facts live in the server and go out through the API; looks stay in the client")

d.save(Path(__file__).with_name("diagram.svg"))
