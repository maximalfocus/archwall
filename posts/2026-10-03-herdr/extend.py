"""Extending herdr: integrations, agents that report on their own, plugins.  Drawn from
https://github.com/herdrdev/herdr (docs/next/website/src/content/docs/integrations.mdx, agents.mdx,
add-herdr-support.mdx, plugins.mdx; src/integration/; commit e35f393).  Run: python3 extend.py

Snake order: 1 install an integration (top left) -> 2 what it reports (top right) -> 3 agents that
support herdr (bottom right) -> 4 plugins (bottom left)."""
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

d = Diagram("herdr integrations and plugins",
            "1 Install an integration: herdr integration install claude writes a small hook into the agent's own "
            "config; 18 agents have one, and letta is experimental and CLI only. "
            "2 What it reports: the session ID so herdr can resume the conversation, and for 6 agents the state too. "
            "3 Agents that support herdr make the same calls themselves: report state with an optional --seq, report "
            "the resume command, and release the pane on exit. No herdr change is needed. "
            "4 Plugins: a herdr-plugin.toml declares actions, event hooks, panes and startup hooks; the whole herdr "
            "CLI is the plugin API. Plugins run as you and are not sandboxed; install shows a preview first.")

d.group(L, T1, W, H1, "Install an integration", 1)
col(L, T1, [("herdr integration install claude|opt-in, per agent", "review"),
            ("Writes a hook|into the agent's own config", "write")], h=80)
d.note(L + W / 2, T1 + 300, "18 agents have one")
d.note(L + W / 2, T1 + 328, "letta: experimental, CLI only")

d.group(R, T1, W, H1, "What it reports", 2)
col(R, T1, [("Session ID|so herdr can resume", "data"),
            ("State|6 integrations also send it", "critic")], h=80, arrows=False)

d.group(R, T2, W, H2, "Agents that support herdr", 3)
col(R, T2, [("report-agent|state, optional --seq", "critic"),
            ("Resume command|re-run after a restart", "plan"),
            ("release-agent|when the user quits", "data")], arrows=False)
d.note(R + W / 2, T2 + 370, "no change to herdr needed")

d.group(L, T2, W, H2, "Plugins", 4)
col(L, T2, [("herdr-plugin.toml|actions, event hooks, panes", "plan"),
            ("Startup hooks|run after the session is restored", "coding"),
            ("Runs as you, not sandboxed|install shows a preview first", "review")], arrows=False)
d.note(L + W / 2, T2 + 370, "the whole herdr CLI is the plugin API")

handoffs("hook runs", "same calls", "same CLI")
d.save(Path(__file__).with_name("extend.svg"))
