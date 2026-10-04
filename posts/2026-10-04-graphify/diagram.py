"""graphify: how a folder becomes a knowledge graph.  Drawn from the graphify repo
(https://github.com/Graphify-Labs/graphify, ARCHITECTURE.md, docs/how-it-works.md and README.md,
commit 48d7c0e).  Run: python3 diagram.py

Snake order: 1 scan the folder (top left) -> 2 extract in three passes (top right) -> 3 build,
cluster, analyze (bottom right) -> 4 files in graphify-out/ (bottom left)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("graphify architecture",
            "1 Scan the folder: detect() sorts files into code, docs and papers, images, and video or audio. "
            "A SHA256 cache skips files that have not changed. "
            "2 Extract in three passes. Pass 1 parses code with tree-sitter, locally, with no LLM. "
            "Pass 2 transcribes video and audio with faster-whisper, locally (video extra). Pass 3 sends docs, papers, "
            "images and transcripts to parallel LLM subagents, which costs tokens. Passes 1 and 3 return nodes "
            "and edges, and each edge is tagged EXTRACTED, INFERRED or AMBIGUOUS. "
            "3 Build and cluster: build() makes one NetworkX graph, cluster() finds communities with the "
            "Leiden algorithm (leiden extra; otherwise Louvain), and the analyze helpers find god nodes and surprising connections. "
            "4 Output in graphify-out: graph.json, graph.html and GRAPH_REPORT.md, plus optional exports "
            "such as an Obsidian vault, a wiki, SVG, GraphML and Cypher.")

L, R, W = 24, 624, 552
T1, H1 = 16, 412
T2, H2 = 460, 400

# 1 scan the folder
d.group(L, T1, W, H1, "Scan the folder", 1)
d.sub(L + 12, T1 + 58, W - 24, 246, "detect(): sort by type")
for i, lbl in enumerate(["Code", "Docs, papers", "Images", "Video, audio"]):
    d.card(L + 30 + (i % 2) * 254, T1 + 112 + (i // 2) * 96, lbl, "data", w=238, h=74)
d.note(L + W / 2, T1 + 346, "SHA256 cache:")
d.note(L + W / 2, T1 + 372, "unchanged files are skipped")

# 2 extract
d.group(R, T1, W, H1, "Extract: three passes", 2)
PW, PH = W - 60, 80
for i, lbl in enumerate(["Pass 1: code|tree-sitter, local, no LLM",
                         "Pass 2: video, audio|faster-whisper (video extra)",
                         "Pass 3: docs, papers, images|LLM subagents, costs tokens"]):
    d.card(R + 30, T1 + 64 + i * 96, lbl, "coding", w=PW, h=PH)
d.note(R + W / 2, T1 + 380, "edges: EXTRACTED, INFERRED, AMBIGUOUS")

# 3 build and cluster
d.group(R, T2, W, H2, "Build and cluster", 3)
CW, CH = 238, 80
A = (R + 30, T2 + 76)    # build
B = (R + 284, T2 + 76)   # leiden
C = (R + 284, T2 + 224)  # analyze
d.card(*A, "build()|one NetworkX graph", "write", w=CW, h=CH)
d.card(*B, "cluster()|Leiden or Louvain", "plan", w=CW, h=CH)
d.card(*C, "Analyze|god nodes, surprises", "critic", w=CW, h=CH)
d.arrow(f"M{A[0] + CW} {A[1] + CH / 2}H{B[0]}")
d.arrow(f"M{B[0] + CW / 2} {B[1] + CH}V{C[1]}")
d.note(R + W / 2, T2 + 350, "no embeddings, no vector store")

# 4 outputs
d.group(L, T2, W, H2, "Output: graphify-out/", 4)
for i, (lbl, k) in enumerate([("graph.json|full graph", "data"), ("graph.html|click and search", "write"),
                              ("GRAPH_REPORT.md|the highlights", "write")]):
    d.card(L + 30 + (i % 2) * 254, T2 + 72 + (i // 2) * 100, lbl, k, w=238, h=80)
d.card(L + 284, T2 + 172, "Exports|Obsidian, wiki, …", "write", w=238, h=80)
d.note(L + W / 2, T2 + 318, "also SVG, GraphML, Cypher")

# hand-offs between stages, drawn last so they sit on top
d.arrow(f"M{L + W - 12} {T1 + 200}H{R + 30}", label="files", at=(L + W + 24, T1 + 188))
d.arrow(f"M{R + 64} {T1 + 352}V{A[1]}", label="nodes + edges", at=(R + 140, T1 + H1 + 22))
d.arrow(f"M{C[0]} {C[1] + CH / 2}H{L + W - 12}", label="graph", at=(L + W + 24, C[1] + CH / 2 - 12))

d.note(600, 888, "detect → extract → build → cluster → analyze → report → export")

d.save(Path(__file__).with_name("diagram.svg"))
