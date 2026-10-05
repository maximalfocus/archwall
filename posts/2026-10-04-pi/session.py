"""Pi sessions: a tree in one JSONL file, and what the model gets from it.  Drawn from the pi repo
(https://github.com/earendil-works/pi, packages/coding-agent/docs/how-pi-works.md, sessions.md,
session-format.md, compaction.md and settings.md "Compaction", commit b2b5c42).  Run: python3 session.py

Layout: 1 the tree spans the top row; then 2 what the model gets (bottom left) and 3 compaction
and new files (bottom right)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("Pi session tree",
            "1 A session is one JSONL file. Each entry has an id and its parent's id, so entries form a tree. "
            "The active branch runs from the root to the current entry. Going back with /tree starts another "
            "branch in the same file and keeps the old one. A compaction entry holds a summary of older "
            "messages. 2 The model gets the system prompt with context files, tool and skill descriptions, "
            "the compaction summary instead of the older messages, and the recent messages on the active "
            "branch. Other branches are never sent. 3 Compaction runs when the context passes the model's "
            "window minus 16384 reserve tokens, or on /compact; the original entries stay. /fork starts a new "
            "session file from an earlier user message; /clone copies the active branch into a new one.")

# 1 the tree
d.group(24, 16, 1152, 440, "A session: one JSONL file, a tree", 1)
CW, GAP, X0 = 170, 16, 50
col = lambda i: X0 + i * (CW + GAP)
Y1, Y2, CH = 80, 212, 72
main = [("user", "plan"), ("assistant", "plan"), ("tool result", "plan"),
        ("compaction|summary", "write"), ("user", "plan"), ("assistant|current", "plan")]
for i, (lbl, k) in enumerate(main):
    d.card(col(i), Y1, lbl, k, w=CW, h=CH)
    if i:
        d.arrow(f"M{col(i - 1) + CW} {Y1 + CH / 2}H{col(i)}")
for i, lbl in [(2, "user|earlier try"), (3, "assistant")]:
    d.card(col(i), Y2, lbl, "data", w=CW, h=CH)
d.arrow(f"M{col(1) + CW / 2} {Y1 + CH}V{Y2 + CH / 2}H{col(2)}")
d.arrow(f"M{col(2) + CW} {Y2 + CH / 2}H{col(3)}")
d.note(col(4), Y2 + CH / 2 + 6, "left via /tree, still in the file", "start")
d.legend(330, 340, ["plan", "data", "write"], ["active branch", "other branch", "summary entry"])
d.note(600, 400, "each line is one entry with its parent's id")
d.note(600, 426, "active branch: root to the current entry")

# 2 what the model gets
L, R, W, T, H = 24, 624, 552, 492, 368
d.group(L, T, W, H, "What the model gets", 2)
for i, (lbl, k) in enumerate([("System prompt + context files", "data"),
                              ("Tool + skill descriptions", "coding"),
                              ("Compaction summary", "write"),
                              ("Recent messages on the branch", "plan")]):
    d.card(L + 46, T + 62 + i * 64, lbl, k, w=460, h=52)
d.note(L + W / 2, T + 346, "other branches are never sent")
d.arrow(f"M{L + W / 2} {456}V{T}", label="active branch", at=(L + W / 2 + 76, 480))

# 3 compaction and new files
d.group(R, T, W, H, "Compaction and new files", 3)
d.sub(R + 12, T + 58, W - 24, 126, "Compaction")
d.note(R + W / 2, T + 120, "near the limit (window − 16384), or /compact")
d.note(R + W / 2, T + 148, "summary in, old entries stay")
d.sub(R + 12, T + 198, W - 24, 156, "New session file")
d.card(R + 30, T + 252, "/fork|from a user message", w=236, h=76)
d.card(R + 286, T + 252, "/clone|the active branch", w=236, h=76)

d.note(600, 888, "pi · docs: how-pi-works.md, sessions.md, compaction.md")

d.save(Path(__file__).with_name("session.svg"))
