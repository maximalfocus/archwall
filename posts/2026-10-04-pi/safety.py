"""Pi and safety: what pi does and does not protect, and the ways to fence it in.  Drawn from the pi
repo (https://github.com/earendil-works/pi, README.md "Permissions & Containerization",
packages/coding-agent/docs/security.md, containerization.md, extensions.md "Tool exposure" and
mcp.md "Permissions", commit b2b5c42).  Run: python3 safety.py

Snake order: 1 by default (top left) -> 2 project trust (top right) -> 3 opt-in permission
extension (bottom right) -> 4 isolation (bottom left).  Layers of defence, not a flow, so no arrows
between the groups."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("Pi safety",
            "1 By default pi has no built-in permission system and does not ask before each tool call. "
            "Tools, extensions and child processes run with the rights of the account that started pi. "
            "2 Project trust decides whether a folder's .pi settings, extensions, skills and MCP servers "
            "load. It is not a sandbox: once pi runs, tools can reach anything the account can. "
            "3 Opt in: a permission extension can hook every tool call, MCP calls included, and ask before "
            "risky ones, using the hints tools declare. "
            "4 Isolation: run all of pi in plain Docker, Docker Sandboxes or OpenShell, or keep pi on the "
            "host and send only the built-in tools into a micro-VM with the Gondolin extension.")

L, R, W = 24, 624, 552
T1, H1 = 16, 412
T2, H2 = 460, 400
CW = 492

# 1 by default
d.group(L, T1, W, H1, "By default", 1)
d.card(L + 30, T1 + 72, "No permission system|no ask before each call", "review", w=CW, h=76)
d.card(L + 30, T1 + 184, "Your account's rights|for tools and extensions", "coding", w=CW, h=76)
d.note(L + W / 2, T1 + 318, "files, comments and tool output")
d.note(L + W / 2, T1 + 344, "can steer the model (prompt injection)")

# 2 project trust
d.group(R, T1, W, H1, "Project trust", 2)
d.card(R + 30, T1 + 72, "Trust this folder?|you decide, can be saved", "review", w=CW, h=76)
d.card(R + 30, T1 + 184, ".pi folder loads|settings, extensions, MCP", "data", w=CW, h=76)
d.arrow(f"M{R + W / 2} {T1 + 148}V{T1 + 184}", label="yes", at=(R + W / 2 + 28, T1 + 172))
d.note(R + W / 2, T1 + 318, "not a sandbox: it only decides")
d.note(R + W / 2, T1 + 344, "what loads at startup")

# 3 opt-in permission extension
d.group(R, T2, W, H2, "Opt in: permission extension", 3)
d.card(R + 30, T2 + 72, "Hook every tool call|MCP calls too", "review", w=CW, h=76)
d.card(R + 30, T2 + 184, "Ask before risky ones|using the tools' hints", "review", w=CW, h=76)
d.arrow(f"M{R + W / 2} {T2 + 148}V{T2 + 184}")
d.note(R + W / 2, T2 + 318, "you install or write one;")
d.note(R + W / 2, T2 + 344, "none is built in")

# 4 isolation
d.group(L, T2, W, H2, "Isolation (strongest)", 4)
for i, (lbl, k) in enumerate([("Plain Docker|all of pi", None), ("Docker Sandboxes|all of pi", None),
                              ("OpenShell|all of pi, policies", None), ("Gondolin|only built-in tools", None)]):
    d.card(L + 30 + (i % 2) * 254, T2 + 72 + (i // 2) * 100, lbl, k, w=238, h=80)
d.note(L + W / 2, T2 + 300, "expose only the files, keys and")
d.note(L + W / 2, T2 + 326, "network the task needs")

d.note(600, 888, "pi's docs: watching the transcript is not a security boundary")

d.save(Path(__file__).with_name("safety.svg"))
