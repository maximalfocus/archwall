"""Pi's packages: which library does what, and which ones the published CLI uses.  Drawn from the pi
repo (https://github.com/earendil-works/pi, README.md "Packages", every packages/*/package.json and
README.md, packages/coding-agent/src/experimental/commands.ts and src/core/experimental.ts,
commit b2b5c42).  Run: python3 packages.py

A map, not a flow, so the groups carry no numbers.  Layout: the app (top left) uses the engine
(top right) and the tool helpers (bottom right); the experimental remote-session packages sit
bottom left."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("Pi packages",
            "The app: pi-coding-agent is the pi command, with sessions, tools and the four ways in; "
            "pi-tui draws the terminal UI. It uses the engine: pi-agent-core runs the agent loop on top of "
            "pi-ai, the one API over many model providers, which reports through pi-telemetry's tracing "
            "contracts. It also uses two tool helpers through its built-in extensions: pi-codemode runs "
            "model-written JavaScript in a QuickJS sandbox, and pi-mcp is a standalone MCP client. "
            "Experimental and for development only: chord, pi-durable, pi-protocol, pi-server and pi-client "
            "serve remote sessions through the pi server and pi client commands, which only run with "
            "PI_EXPERIMENTAL=1 and are not in the published CLI.")

L, R, W = 24, 624, 552
T1, H1 = 16, 412
T2, H2 = 460, 400
CW = 492

# the app
d.group(L, T1, W, H1, "The app")
d.card(L + 30, T1 + 80, "pi-coding-agent|the pi command", "coding", w=CW, h=84)
d.card(L + 30, T1 + 196, "pi-tui|terminal UI", w=CW, h=84)
d.note(L + W / 2, T1 + 336, "sessions, tools, extensions,")
d.note(L + W / 2, T1 + 362, "the four ways in")

# the engine
d.group(R, T1, W, H1, "The engine")
d.card(R + 30, T1 + 72, "pi-agent-core|the agent loop", "plan", w=CW, h=76)
d.card(R + 30, T1 + 184, "pi-ai|one API, many models", w=CW, h=76)
d.card(R + 30, T1 + 296, "pi-telemetry|tracing contracts", "data", w=CW, h=76)
d.arrow(f"M{R + W / 2} {T1 + 148}V{T1 + 184}", label="uses", at=(R + W / 2 + 34, T1 + 172))
d.arrow(f"M{R + W / 2} {T1 + 260}V{T1 + 296}", label="uses", at=(R + W / 2 + 34, T1 + 284))

# tool helpers
d.group(R, T2, W, H2, "Tool helpers")
d.card(R + 30, T2 + 80, "pi-codemode|scripts in a sandbox", "coding", w=CW, h=84)
d.card(R + 30, T2 + 196, "pi-mcp|MCP client", "coding", w=CW, h=84)
d.note(R + W / 2, T2 + 336, "used by built-in extensions;")
d.note(R + W / 2, T2 + 362, "each works on its own too")

# experimental
d.group(L, T2, W, H2, "Experimental: remote sessions")
for i, lbl in enumerate(["chord|app runtime", "pi-durable|crash-safe runs", "pi-protocol|wire format",
                         "pi-server|routes sessions"]):
    d.card(L + 30 + (i % 2) * 254, T2 + 64 + (i // 2) * 92, lbl, "data", w=238, h=76)
d.card(L + 157, T2 + 248, "pi-client|connects", "data", w=238, h=76)
d.note(L + W / 2, T2 + 356, "dev only: PI_EXPERIMENTAL=1")
d.note(L + W / 2, T2 + 382, "not in the published CLI")

# links, drawn last so they sit on top
d.arrow(f"M{L + W} {T1 + 122}H{R}", label="uses", at=(600, T1 + 110))
d.arrow(f"M{L + W - 30} {T1 + H1}V{T2 - 16}H{600}V{T2 + 122}H{R}", label="uses", at=(600, T2 + 60))

d.note(600, 888, "pi · 13 folders under packages/, evals is private")

d.save(Path(__file__).with_name("packages.svg"))
