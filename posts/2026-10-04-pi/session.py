"""Pi sessions: a tree in one JSONL file, and what the model gets from it.  Drawn from the pi repo
(https://github.com/earendil-works/pi, packages/coding-agent/docs/how-pi-works.md, sessions.md and
compaction.md, commit 2003871).  Run: python3 session.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("Pi session tree",
            "1 A session is one JSONL file. Each entry has an id and its parent's id, so entries form a tree. "
            "The active branch runs from the root to the current entry; going back with /tree starts another "
            "branch in the same file and keeps the old one. A compaction entry holds a summary of older "
            "messages. 2 The model gets the system prompt with context files, tool and skill descriptions, "
            "the compaction summary instead of the older messages, and the recent messages on the active "
            "branch. Other branches are never sent. 3 Compaction runs when the context passes the model's "
            "window minus 16384 reserve tokens, or on /compact; the original entries stay. /fork starts a new "
            "session file from an earlier user message; /clone copies the active branch into a new one.")

# 1 the tree
d.group(24, 16, 1152, 436, "A session: one JSONL file, a tree", 1)
CW, GAP, X0 = 160, 26, 48
col = lambda i: X0 + i * (CW + GAP)
Y1, Y2, CH = 76, 200, 60
main = [("user", "plan"), ("assistant", "plan"), ("tool result", "plan"),
        ("compaction|summary", "write"), ("user", "plan"), ("assistant|current entry", "plan")]
for i, (lbl, k) in enumerate(main):
    d.card(col(i), Y1, lbl, k, w=CW, h=CH)
    if i:
        d.arrow(f"M{col(i - 1) + CW} {Y1 + CH / 2}H{col(i)}")
for i, lbl in [(2, "user|earlier try"), (3, "assistant")]:
    d.card(col(i), Y2, lbl, "data", w=CW, h=CH)
d.arrow(f"M{col(1) + CW / 2} {Y1 + CH}V{Y2 + CH / 2}H{col(2)}")
d.arrow(f"M{col(2) + CW} {Y2 + CH / 2}H{col(3)}")
d.note(col(4), Y2 + 26, "left with /tree: kept in the file,", "start")
d.note(col(4), Y2 + 46, "can leave a summary on the new branch", "start")
d.legend(440, 310, ["plan", "data", "write"], ["active branch", "other branch", "summary entry"])
d.note(600, 352, "each line is one entry: its id and its parent's id")
d.note(600, 376, "active branch: from the root to the current entry")
d.note(600, 400, "nothing is deleted, old branches and compacted entries stay")
d.arrow(f"M{300} {452}V{488}")

# 2 what the model gets
L, R, W, T, H = 24, 624, 552, 488, 360
d.group(L, T, W, H, "What the model gets", 2)
for i, (lbl, k) in enumerate([("System prompt|base + context files", "data"),
                              ("Tools + skill descriptions", "coding"),
                              ("Compaction summary|instead of older messages", "write"),
                              ("Recent messages on the branch|user · assistant · tool result", "plan")]):
    d.card(L + 76, T + 52 + i * 64, lbl, k, w=400, h=54)
d.note(L + W / 2, T + 330, "other branches are never sent")

# 3 when context fills up, and new files
d.group(R, T, W, H, "Compaction and new files", 3)
d.sub(R + 12, T + 46, W - 24, 150, "Compaction")
d.note(R + W / 2, T + 98, "automatic when context > window − 16384 tokens")
d.note(R + W / 2, T + 122, "or /compact, with your own instructions")
d.note(R + W / 2, T + 146, "summary of older history, recent messages kept")
d.note(R + W / 2, T + 170, "the original entries stay in the tree")
d.sub(R + 12, T + 206, W - 24, 140, "New session file")
d.card(R + 36, T + 250, "/fork|from an earlier user message", "write", w=236, h=60)
d.card(R + 292, T + 250, "/clone|copy the active branch", "write", w=236, h=60)
d.note(R + W / 2, T + 334, "sessions live in ~/.pi/agent/sessions/, by folder")

d.note(600, 884, "pi · github.com/earendil-works/pi · docs: sessions.md, compaction.md")

d.save(Path(__file__).with_name("session.svg"))
