"""What keeps the PEER in its lane, per CLI.
Drawn from maximalfocus/peerreview-skills at commit 2f8d61e (scripts/claude-round.sh, scripts/codex-round.sh,
scripts/pi-round.sh, scripts/dsh-round.sh, scripts/git-guard.sh, scripts/round-support.sh).
Run: python3 rails.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("peerreview guard rails",
            "1 Claude Code as peer runs in safe mode, without the host user's CLAUDE.md, skills, hooks or MCP "
            "servers; in the verdict round Edit, Write and Bash are switched off. "
            "2 The Codex CLI as peer edits inside a workspace-write sandbox; its verdict runs in a fresh "
            "read-only sandbox. "
            "3 Pi has no sandbox; its verdict only gets read, grep, find and ls. dsh has no tool allowlist, so "
            "its verdict fails if the repo changed. "
            "4 For every peer: a git guard on the PATH lets only read-only git commands run in the repo, which "
            "guards against mistakes but is not a sandbox; each round has a deadline of 1800 seconds by "
            "default; and only the host commits.")

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

d.pill(L, 16, W, 48, "Each driver script wraps its PEER CLI like this")

d.group(L, T1, W, H1, "Claude Code as PEER", 1)
column(L, T1, [("Safe mode|no HOST CLAUDE.md, hooks, MCP", "review"),
               ("Edit rounds|all tools, git guarded", "coding"),
               ("Verdict round|Edit, Write, Bash switched off", "critic")])

d.group(R, T1, W, H1, "Codex CLI as PEER", 2)
column(R, T1, [("Edit rounds|workspace-write sandbox", "coding"),
               ("Verdict round|fresh read-only sandbox", "critic")])
notes(R, T1, H1, "Both rounds also", "behind the git guard")

d.group(R, T2, W, H2, "Pi and dsh as PEER", 3)
column(R, T2, [("Pi: no sandbox|verdict gets read, grep, find, ls", "coding"),
               ("dsh: no tool allowlist|verdict fails if the repo moved", "coding")])
notes(R, T2, H2, "A moved repo is not reverted:", "the HOST looks at it first")

d.group(L, T2, W, H2, "For every PEER", 4)
column(L, T2, [("Git guard on PATH|only read-only git in the repo", "review"),
               ("Round deadline|1800 s by default", "review"),
               ("Only the HOST commits|and pushes", "review")])

d.note(600, 888, "The git guard catches mistakes; it is not a sandbox against a PEER set on getting around it")

d.save(Path(__file__).with_name("rails.svg"))
