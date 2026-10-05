"""Picking the PEER: always another vendor, tier 1 first.
Drawn from maximalfocus/peerreview-skills at commit 2f8d61e (scripts/select-peer.sh, scripts/peer-auth.sh,
skills/peerreview/SKILL.md Step 0.0, README.md Install).
Run: python3 peer.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("peerreview peer choice",
            "1 Who is the host: Claude Code, the Codex CLI, Pi on DeepSeek, or the DeepSeek Harness dsh, read "
            "from environment markers and the model in use. "
            "2 Tier 1 is the other subscription CLI: Claude Code on a Claude subscription, or the Codex CLI on a "
            "ChatGPT subscription. A Claude Code host gets Codex, a Codex host gets Claude Code. "
            "3 Tier 2, only if no tier-1 peer is reachable: dsh with deepseek-v4-pro for CDD repos, Pi with "
            "deepseek-flash for every other repo. The report names it as the weaker tier. A DeepSeek host has "
            "tier 1 only. "
            "4 Every candidate is checked first: the CLI is installed and signed in, without printing keys; for the "
            "subscription peers a tiny prompt probes quota, and an out-of-quota peer is skipped; if nobody is left, "
            "the review stops. "
            "The peer is never from the host's own vendor.")

L, R, W = 24, 624, 552
T1, H1 = 84, 380
T2, H2 = 500, 364
CW, CH, GAP = 492, 64, 16


def column(x, top, cards, gap=GAP):
    for i, (lbl, kind) in enumerate(cards):
        d.card(x + 30, top + 64 + i * (CH + gap), lbl, kind, w=CW, h=CH)


def notes(x, top, h, a, b):
    d.note(x + W / 2, top + h - 52, a)
    d.note(x + W / 2, top + h - 26, b)

d.pill(L, 16, W, 48, "select-peer.sh picks the PEER before the loop")
d.arrow(f"M{L + W / 2} 64V{T1 - 2}")

d.group(L, T1, W, H1, "Who is the HOST?", 1)
column(L, T1, [("Claude Code|Anthropic", None),
               ("Codex CLI|OpenAI", None),
               ("Pi, or DeepSeek Harness (dsh)|DeepSeek", None)])
notes(L, T1, H1, "Read from the environment", "and the model in use")

d.group(R, T1, W, H1, "Tier 1: the other subscription", 2)
column(R, T1, [("Claude Code|Claude subscription", "coding"),
               ("Codex CLI|ChatGPT subscription", "coding")])
notes(R, T1, H1, "Claude Code HOST gets Codex;", "Codex HOST gets Claude Code")

d.group(R, T2, W, H2, "Tier 2: only if tier 1 is out", 3)
column(R, T2, [("dsh, deepseek-v4-pro|for CDD repos", "coding"),
               ("Pi, deepseek-flash|for every other repo", "coding")])
notes(R, T2, H2, "Named as the weaker tier in the report;", "a DeepSeek HOST has tier 1 only")

d.group(L, T2, W, H2, "Each candidate is checked", 4)
column(L, T2, [("CLI installed, signed in|no keys printed", "review"),
               ("Quota probe (subscription)|one tiny prompt; used up → next", "review"),
               ("Nobody left → stop|no same-vendor stand-in", "review")])

d.arrow(f"M{L + W} {T1 + 200}H{R - 2}", label="ladder", at=(600, T1 + 188))
d.arrow(f"M{R + W / 2} {T1 + H1}V{T2 - 2}", label="none reachable", at=(R + W / 2 + 80, T1 + H1 + 24))

d.note(600, 888, "The PEER is never from the HOST's own vendor")

d.save(Path(__file__).with_name("peer.svg"))
