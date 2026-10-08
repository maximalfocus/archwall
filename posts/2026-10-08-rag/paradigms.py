"""The three RAG paradigms side by side: Naive RAG, Advanced RAG, Modular RAG.
Not steps of one run: each paradigm grew out of the one before it, so the groups are unnumbered and the
arrows between them name that relation. Module and pattern details have their own figure (modular.svg).
Drawn from Gao et al., "Retrieval-Augmented Generation for Large Language Models: A Survey",
arXiv:2312.10997v5 (Section II.A Naive RAG, II.B Advanced RAG, II.C Modular RAG, Fig. 3).
Run: python3 paradigms.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, C3, CW3  # noqa: E402

d = Diagram("Three kinds of RAG",
            "Three ways to build RAG, side by side; each grew out of the one before. "
            "Naive RAG, the earliest: index the documents, retrieve the top K chunks, and let the LLM "
            "generate the answer, also called Retrieve-Read. Its gaps: retrieval misses, picking wrong "
            "chunks or missing key facts; hallucination, an answer the chunks do not support; and "
            "redundancy, the same facts from several sources, so the answer repeats itself. "
            "Advanced RAG fixes those gaps but is still one chain. Before retrieval it improves the index "
            "with a sliding window and metadata, cuts finer chunks, and makes the question clearer by rewriting "
            "or expanding it. Retrieve and generate stay as in Naive RAG. After retrieval it reranks the "
            "chunks, moving the most relevant to the edges of the prompt, and compresses them to the key parts. "
            "Modular RAG builds on both and opens the chain into modules. You can add new modules, such as "
            "search, memory and routing, or swap existing ones. The flow need not be one pass: it can "
            "retrieve iteratively, or adaptively, deciding whether to retrieve at all. Parts such as the "
            "retriever and the generator can be fine-tuned.")

x1, x2, x3 = C3
TOP, GH = 84, 800
SW, CW = CW3 - 32, CW3 - 60  # sub-group and card widths


def sub_cards(x, y, title, cards):
    """A sub-group with a title and cards, 16 px inside the column; returns its bottom."""
    h = 52 + len(cards) * 80
    d.sub(x + 16, y, SW, h, title)
    for i, (label, kind) in enumerate(cards):
        d.card(x + 30, y + 48 + i * 80, label, kind, w=CW, h=64)
    return y + h


d.group(x1, TOP, CW3, GH, "Naive RAG")
d.column(x1, TOP, [("Index|split · embed · store", "data"),
                   ("Retrieve|top K similar chunks", "coding"),
                   ("Generate|the LLM answers", "write")], w=CW)
sub_cards(x1, TOP + 316, "Its gaps", [("Retrieval misses|wrong or missing chunks", "data"),
                                      ("Hallucination|not backed by the chunks", "data"),
                                      ("Redundancy|repeats the same facts", "data")])
d.notes(x1, TOP, GH, "Also called Retrieve-Read", "The earliest kind", w=CW3)

d.group(x2, TOP, CW3, GH, "Advanced RAG")
y = sub_cards(x2, TOP + 64, "Before retrieval", [("Better index|sliding window · metadata", "plan"),
                                                 ("Finer chunks|smaller pieces", "plan"),
                                                 ("Clearer question|rewrite · expand", "plan")])
d.card(x2 + 30, y + 24, "Retrieve · generate|as in Naive RAG", "coding", w=CW, h=64)
sub_cards(x2, y + 112, "After retrieval", [("Rerank|most relevant to the edges", "critic"),
                                           ("Compress|keep the key parts", "critic")])
d.notes(x2, TOP, GH, "Still one chain", "like Naive RAG", w=CW3)

d.group(x3, TOP, CW3, GH, "Modular RAG")
y = sub_cards(x3, TOP + 64, "Modules", [("Add new ones|search · memory · routing", "plan"),
                                        ("Swap old ones|to fit the task", "plan")])
y = sub_cards(x3, y + 24, "Flows, not one pass", [("Iterative|retrieve · read · repeat", "coding"),
                                                  ("Adaptive|retrieve only when needed", "coding")])
sub_cards(x3, y + 24, "Training", [("Fine-tune the parts|retriever · generator", "write")])
d.notes(x3, TOP, GH, "Builds on Naive and", "Advanced RAG", w=CW3)

d.arrow(f"M{x1 + CW3 - 70} {TOP}V48H{x2 + 70}V{TOP - 2}", label="fixes its gaps", at=(x1 + CW3 + 12, 36))
d.arrow(f"M{x2 + CW3 - 70} {TOP}V48H{x3 + 70}V{TOP - 2}", label="opens it up", at=(x2 + CW3 + 12, 36))

d.save(Path(__file__).with_name("paradigms.svg"))
