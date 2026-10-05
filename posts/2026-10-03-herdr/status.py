"""How herdr decides which agent needs you.  Drawn from https://github.com/herdrdev/herdr
(docs/next/website/src/content/docs/agents.mdx, integrations.mdx, add-herdr-support.mdx, concepts.mdx,
configuration.mdx; src/detect/mod.rs Agent::ALL (24) and SCREEN_MANIFEST_AGENTS (22);
src/detect/manifests/*.toml (22 files); src/config/model.rs ToastDelivery default Off; commit e35f393).
Run: python3 status.py

Snake order: 1 which agent? (top left) -> 2 read the screen (top right) -> 3 the agent's own reports
(bottom right) -> 4 result (bottom left)."""
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

d = Diagram("herdr agent status",
            "1 Which agent: herdr looks at the foreground process in each pane; it knows 24 agents such as claude, "
            "codex and pi. A wrapper that hides the agent can name it with the HERDR_AGENT variable. "
            "2 Read the screen: the live bottom of the pane and its title, not the part you scrolled to, checked "
            "against rules in a manifest per agent (22 manifests). Rule updates come from herdr.dev; a local file wins. "
            "3 The agent's own reports: 6 integrations also report state, and some agents report on their own. While "
            "they report, herdr uses that instead of the screen. A sequence number drops late reports. "
            "4 Result: working, blocked (needs a decision), done (finished, not seen yet), idle (seen, ready) or "
            "unknown. A known agent with no matching rule shows idle. Sound is on by default; popups are opt-in.")

d.group(L, T1, W, H1, "Which agent?", 1)
col(L, T1, [("Foreground process|in each pane", "data"),
            ("24 agents known|claude, codex, pi …", "data")], h=80)
d.note(L + W / 2, T1 + 300, "wrapper hides it? set HERDR_AGENT")

d.group(R, T1, W, H1, "Read the screen", 2)
col(R, T1, [("Live bottom + title|not where you scrolled", "data"),
            ("Manifest rules|22 agents, AND / OR checks", "critic")], h=80)
d.note(R + W / 2, T1 + 300, "rule updates from herdr.dev")
d.note(R + W / 2, T1 + 328, "a local override file wins")

d.group(R, T2, W, H2, "The agent's own reports", 3)
col(R, T2, [("Integrations|6 also report state", "critic"),
            ("Agents that support herdr|report by themselves", "critic")], h=80, arrows=False)
d.note(R + W / 2, T2 + 300, "while they report, the screen check waits")
d.note(R + W / 2, T2 + 328, "optional --seq drops late reports")

d.group(L, T2, W, H2, "Result", 4)
grid(L, T2, [("working", "coding"), ("blocked|needs a decision", "review"),
             ("done|finished, not seen", "write"), ("idle|seen, ready", "data"),
             ("unknown|can't tell", "data")], h=64, gap=12)
d.note(L + W / 2, T2 + 330, "known agent, no rule matched: idle")
d.note(L + W / 2, T2 + 360, "sound on by default · popups opt-in")

handoffs("agent kind", "screen state", "final state")
d.save(Path(__file__).with_name("status.svg"))
