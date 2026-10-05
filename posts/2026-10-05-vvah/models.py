"""VVAH models: every AI step is a setting.  Drawn from the community fork
maximalfocus/visa-vulnerability-agentic-harness (README.md "Multi-model by design", docs/features.md
sections 3-5, docs/architecture.md "LLM transport layer", vvaharness/config/profiles/default.yaml,
commit 1c292e3).  Run: python3 models.py

Snake order: 1 steps (top left) -> 2 routes (top right) -> 3 providers (bottom right)
-> 4 what each AI may touch (bottom left)."""
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

d = Diagram("VVAH models",
            "1 Every AI step is a setting: detection S0 to S9, the fix step S10, the grading panel S11 and the "
            "four live-check roles each name their own model in the config, with no code change. "
            "2 Four routes, chosen per step with via: cli runs the claude program, sdk the Anthropic SDK, openai "
            "any OpenAI-style API, and deepagents a LangGraph harness, which the default profile uses everywhere. "
            "3 Providers: Anthropic Claude, OpenAI or any compatible gateway, and open-weight models on "
            "compatible endpoints. The default profile needs one Anthropic key. "
            "4 What each AI may touch: one-shot steps get no tools, explorers and verifiers get read-only tools, "
            "the fixer may edit inside the repo, and no shipped profile grants a shell.")

d.group(L, T1, W, H1, "Every AI step is a setting", 1)
grid(L, T1, [("Detection|S0–S9", "coding"), ("Fix|S10", "coding"),
             ("Grading panel|S11", "critic"), ("Live check|4 roles", "critic")])
d.note(L + W / 2, T1 + 300, "swap a model in config,")
d.note(L + W / 2, T1 + 328, "no code change")

d.group(R, T1, W, H1, "Four routes (via:)", 2)
grid(R, T1, [("cli|claude program", "data"), ("sdk|Anthropic SDK", "data"),
             ("openai|OpenAI-style API", "data"), ("deepagents|LangGraph harness", "data")])
d.note(R + W / 2, T1 + 300, "default profile: deepagents")
d.note(R + W / 2, T1 + 328, "on every step")

d.group(R, T2, W, H2, "Providers", 3)
col(R, T2, [("Anthropic Claude|native", "data"),
            ("OpenAI|or any compatible gateway", "data"),
            ("Open-weight models|on compatible endpoints", "data")], arrows=False)
d.note(R + W / 2, T2 + 370, "default profile: one Anthropic key")

d.group(L, T2, W, H2, "What each AI may touch", 4)
col(L, T2, [("One-shot steps · no tools", "review"), ("Explorers, verifiers · read-only", "review"),
            ("Fixer · edits inside the repo", "review"), ("Shell · in no shipped profile", "review")],
    h=60, gap=14, arrows=False)

handoffs("config", "API calls", None)
d.note(600, 888, "Prompts carry your code to the chosen provider: use approved endpoints only")
d.save(Path(__file__).with_name("models.svg"))
