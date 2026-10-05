"""graphify overview: from a folder to a graph your assistant asks first.  Drawn from the graphify repo
(https://github.com/Graphify-Labs/graphify, ARCHITECTURE.md, docs/how-it-works.md, README.md,
graphify/skill.md, commit 35adf43).  Run: python3 diagram.py

Snake order: 1 read the folder (top left) -> 2 pull out the facts (top right) -> 3 build the map
(bottom right) -> 4 use the map (bottom left)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("graphify overview",
            "Input: a folder of code, docs, papers, images and video. "
            "1 Read the folder: detect() skips ignored files, build output and secret files, sorts the rest by "
            "type and warns when the folder is tiny or costly. "
            "2 Pull out the facts in three passes: code is parsed on your machine with tree-sitter, no LLM; "
            "video and audio are transcribed locally with faster-whisper (video extra); docs, papers, images and "
            "transcripts go to an LLM, which costs tokens. A SHA256 cache skips unchanged files. "
            "3 Build the map: one graph with duplicates dropped, communities found with Leiden or Louvain, then "
            "god nodes, surprising links and suggested questions. "
            "4 Use the map: files in graphify-out, the assistant asks the graph through the CLI or an MCP server, "
            "and git hooks rebuild the code part for free. Side tools: PR dashboard, cross-repo graph.")

L, R, W = 24, 624, 552
T1, H1 = 84, 360
T2, H2 = 480, 372
CW, CH, GAP = 492, 64, 26


def column(x, top, cards, arrows=True):
    for i, (lbl, kind) in enumerate(cards):
        y = top + 64 + i * (CH + GAP)
        d.card(x + 30, y, lbl, kind, w=CW, h=CH)
        if arrows and i:
            d.arrow(f"M{x + W / 2} {y - GAP}V{y - 2}")


d.pill(L, 16, W, 48, "Your folder: code, docs, papers, images, video")
d.arrow(f"M{L + W / 2} 64V{T1 - 2}")

d.group(L, T1, W, H1, "Read the folder", 1)
column(L, T1, [("Skip what doesn't belong|ignore rules, build output, secrets", "review"),
               ("Sort by type|code, docs, papers, images, video", "coding"),
               ("Check the size|warn if tiny or costly", "critic")])

d.group(R, T1, W, H1, "Pull out the facts", 2)
column(R, T1, [("Code, on your machine|tree-sitter, no LLM, free", "coding"),
               ("Video, audio, on your machine|faster-whisper (video extra)", "coding"),
               ("Docs, papers, images|an LLM reads them, costs tokens", "coding")], arrows=False)
d.note(R + W / 2, T1 + H1 - 24, "SHA256 cache skips unchanged files")

d.group(R, T2, W, H2, "Build the map", 3)
column(R, T2, [("One graph|merge, drop duplicates", "write"),
               ("Find communities|Leiden or Louvain", "plan"),
               ("Find what matters|god nodes, surprises, questions", "critic")])

d.group(L, T2, W, H2, "Use the map", 4)
column(L, T2, [("graphify-out/|graph.json, graph.html, report", "write"),
               ("Assistant asks the graph|hook, CLI, MCP server", "coding"),
               ("Keep it current|git hooks rebuild code, free", "coding")], arrows=False)
d.note(L + W / 2, T2 + H2 - 22, "side tools: PR dashboard, cross-repo graph")

d.arrow(f"M{L + W} {T1 + 210}H{R - 2}", label="files by type", at=(600, T1 + 198))
d.arrow(f"M{R + W / 2} {T1 + H1}V{T2 - 2}", label="nodes + edges", at=(R + W / 2 + 86, T1 + H1 + 24))
d.arrow(f"M{R} {T2 + 200}H{L + W + 2}", label="graph", at=(600, T2 + 188))

d.note(600, 884, "Code is never sent anywhere; docs, images and transcripts go to an LLM")

d.save(Path(__file__).with_name("diagram.svg"))
