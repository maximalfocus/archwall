"""Pi's add-ons: the four kinds, where they load from, what an extension can add, and the built-in
extensions.  Drawn from the pi repo (https://github.com/earendil-works/pi, README.md,
packages/coding-agent/docs/how-pi-works.md, extensions.md, skills.md, prompt-templates.md,
packages.md, configuration.md, mcp.md and src/extensions/index.ts, commit b2b5c42).
Run: python3 extensions.py

Snake order: 1 four kinds of add-on (top left) -> 2 where they load from (top right) ->
3 what an extension can add (bottom right) -> 4 built-in extensions (bottom left)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("Pi extensions and add-ons",
            "1 Four kinds of add-on: extensions are TypeScript code, skills are instructions read on demand, "
            "prompt templates are reusable slash commands, themes are terminal colours. "
            "2 Where they load from: your own folder ~/.pi/agent, the project's .pi folder once the project "
            "is trusted, pi packages from npm or git, or the -e flag for one run. "
            "3 What an extension can add: tools, commands, model providers, MCP servers, terminal UI and "
            "event hooks. It runs inside the pi process with the same rights. "
            "4 Built-in extensions use the same API: mcp, codemode, tool_search and llama.cpp for local "
            "models. An installed extension can replace mcp, codemode or tool_search.")

L, R, W = 24, 624, 552
T1, H1 = 16, 412
T2, H2 = 460, 400

# 1 four kinds
d.group(L, T1, W, H1, "Four kinds of add-on", 1)
for i, (lbl, k) in enumerate([("Extensions|TypeScript code", "coding"), ("Skills|instructions on demand", "data"),
                              ("Prompt templates|reusable / commands", "data"), ("Themes|terminal colours", "data")]):
    d.card(L + 18 + (i % 2) * 264, T1 + 80 + (i // 2) * 112, lbl, k, w=252, h=84)
d.note(L + W / 2, T1 + 352, "bundle them as a pi package")

# 2 where they load from
d.group(R, T1, W, H1, "Where they load from", 2)
for i, (lbl, k) in enumerate([("~/.pi/agent|your own", "data"), (".pi folder|if project trusted", "review"),
                              ("Pi packages|npm or git", "data"), ("-e flag|one run only", "data")]):
    d.card(R + 18 + (i % 2) * 264, T1 + 80 + (i // 2) * 112, lbl, k, w=252, h=84)
d.note(R + W / 2, T1 + 352, "/reload picks up changes")

# 3 what an extension can add
d.group(R, T2, W, H2, "What an extension can add", 3)
for i, lbl in enumerate(["Tools", "Commands", "Model|providers", "MCP servers", "Terminal UI", "Event hooks"]):
    d.card(R + 26 + (i % 3) * 170, T2 + 72 + (i // 3) * 96, lbl, "coding", w=160, h=76)
d.note(R + W / 2, T2 + 300, "runs inside pi, with pi's rights:")
d.note(R + W / 2, T2 + 326, "load only code you trust")

# 4 built-in extensions
d.group(L, T2, W, H2, "Built-in extensions", 4)
for i, lbl in enumerate(["mcp|MCP servers", "codemode|scripts", "tool_search|find tools", "llama.cpp|local models"]):
    d.card(L + 30 + (i % 2) * 254, T2 + 72 + (i // 2) * 100, lbl, "coding", w=238, h=80)
d.note(L + W / 2, T2 + 300, "an installed extension can replace")
d.note(L + W / 2, T2 + 326, "mcp, codemode or tool_search")

# hand-offs, drawn last so they sit on top
d.arrow(f"M{L + W} {T1 + 200}H{R}", label="found in", at=(600, T1 + 188))
d.arrow(f"M{R + W / 2} {T1 + H1}V{T2}", label="loads", at=(R + W / 2 + 40, T1 + H1 + 22))
d.arrow(f"M{R} {T2 + 160}H{L + W}", label="same API", at=(600, T2 + 148))

d.note(600, 888, "pi skips sub-agents and plan mode: add them yourself")

d.save(Path(__file__).with_name("extensions.svg"))
