"""herdr architecture, drawn from the repo docs (concepts, session state, socket API) at
https://github.com/herdrdev/herdr (commit 5da0a01).  Run: python3 diagram.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("herdr architecture",
            "1 Clients (local TUI, remote over SSH, direct attach) only draw and send keys; detaching leaves work running. "
            "2 One server per session owns every pane: a real PTY running the agent, parsed into terminal state by "
            "libghostty-vt. A screen detector and the agents' own reports decide working, blocked, done or idle. "
            "3 A socket API lets agents and scripts spawn panes, prompt each other and wait on state. "
            "4 If the server stops, herdr restores what it can: live handoff, the agent's resume command, "
            "opt-in pane history, and the saved layout.")
A, B, GW, CW = 24, 624, 552, 180

# 1 clients (top left)
d.group(A, 16, GW, 400, "Clients", 1)
d.sub(A + 12, 60, GW - 24, 150, "Draw the screen, send keys")
for i, t in enumerate(["Local|TUI", "Remote|over SSH", "Direct attach|one terminal"]):
    d.card(A + 30 + i * 170, 112, t, w=152, h=64)
d.sub(A + 12, 226, GW - 24, 178, "Detach")
d.card(A + 30, 270, "ctrl+b q", "plan", w=CW)
d.card(A + 342, 270, "Agents keep|running", "coding", w=CW)
d.arrow(f"M{A+210} 300H{A+336}")
d.note(A + GW / 2, 368, "close the laptop or lose SSH: the server keeps going")

# clients <-> server
d.arrow(f"M{A+GW} 130H{B}"); d.note(A + GW + 24, 120, "keys")
d.arrow(f"M{B} 176H{A+GW}"); d.note(A + GW + 24, 196, "screen")

# 2 server (top right)
d.group(B, 16, GW, 400, "Server, one per session", 2)
d.sub(B + 12, 60, GW - 24, 130, "Each pane")
d.card(B + 30, 104, "PTY + process|claude, codex …", "coding", w=CW)
d.card(B + 342, 104, "Terminal state|libghostty-vt", "data", w=CW)
d.arrow(f"M{B+210} 134H{B+336}"); d.note(B + 273, 124, "output")
d.sub(B + 12, 206, GW - 24, 198, "Who is stuck?")
d.card(B + 342, 246, "Screen detector|22 agent manifests", "critic", w=CW)
d.card(B + 342, 326, "Agent's own report|seq: newest wins", "write", w=CW)
d.card(B + 30, 270, "working · blocked|done · idle", "review", w=CW, h=76)
d.arrow(f"M{B+432} 164V240")
d.arrow(f"M{B+342} 276H{B+216}")
d.arrow(f"M{B+342} 356H{B+300}V330H{B+216}")
d.note(B + 120, 374, "shown per pane,")
d.note(B + 120, 392, "rolled up per workspace")

# 3 control API (bottom right)
CY = 446
d.group(B, CY, GW, 370, "Control API", 3)
d.sub(B + 12, CY + 44, GW - 24, 150, "Socket API for agents and scripts")
d.card(B + 30, CY + 92, "Agents in panes|spawn · prompt · wait", "plan", w=230, h=64)
d.card(B + 312, CY + 92, "Scripts|and plugins", "write", w=200, h=64)
d.sub(B + 12, CY + 206, GW - 24, 152, "Every pane gets")
d.card(B + 30, CY + 250, "HERDR_PANE_ID|HERDR_SOCKET_PATH", "data", w=230, h=64)
d.note(B + 412, CY + 276, "agent wait: return when")
d.note(B + 412, CY + 294, "another agent is blocked")

# server <-> control API
d.arrow(f"M{B+470} 416V{CY}"); d.note(B + 482, 436, "events", "start")
d.arrow(f"M{B+400} {CY}V416"); d.note(B + 388, 436, "commands", "end")

# 4 restart and restore (bottom left)
d.group(A, CY, GW, 370, "If the server stops", 4)
d.sub(A + 12, CY + 44, GW - 24, 314, "Bring back what it can")
rows = [("Live handoff|processes survive", "coding", "updates, opt-in"),
        ("Agent resume command|claude --resume <id>", "plan", "same conversation"),
        ("Pane history", "data", "opt-in, may hold secrets"),
        ("Saved layout|session.json", "data", "fresh shell, same dir")]
for i, (t, k, n) in enumerate(rows):
    y = CY + 88 + i * 66
    d.card(A + 30, y, t, k, w=260, h=56)
    d.note(A + 310, y + 33, n, "start")

d.arrow(f"M{B+60} 416V431H{A+GW/2}V{CY}"); d.note(A + GW / 2 + 12, 426, "save", "start")

d.note(600, 868, "one Rust binary · shared facts live in the server and go out through the API; looks stay in the client")

d.save(Path(__file__).with_name("diagram.svg"))
