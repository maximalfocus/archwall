"""How many times to search: once, iterative, recursive, adaptive (four options, no order between them).
Drawn from Gao et al., "Retrieval-Augmented Generation for Large Language Models: A Survey",
arXiv:2312.10997v5 (Section V Augmentation Process in RAG, A-C, and Fig. 5).
Run: python3 flows.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, R, GW, T1, H1, T2, H2  # noqa: E402

d = Diagram("How many times to search",
            "In: a question. RAG can search its knowledge base in four ways, shown side by side. "
            "Once: search one time, then generate the answer. This is the most common way, but it is often "
            "not enough for hard problems that need several reasoning steps. "
            "Iterative: search, generate, and repeat; each search uses the question plus the text generated "
            "so far. ITER-RETGEN works this way. The risk is gaps in meaning and irrelevant information "
            "piling up. "
            "Recursive: refine the query and split the problem into sub-problems, then search and generate, "
            "and refine again. IRCoT guides this with chain-of-thought; ToC builds a clarification tree. "
            "With a structured index it searches a summary first, then inside the document. "
            "Adaptive: the LLM itself decides whether to search and when to stop, often with special tokens. "
            "FLARE searches when the probability of the words it generates falls below a threshold; "
            "Self-RAG uses retrieve and critic tokens.")

d.pill(L, 16, 1152, 48, "In: a question · how many times should RAG search?")

CW = 360           # card width; the right side of each group holds the loop arrow


def flow(x, top, cards, h, gap, first=72):
    """Cards in a column with a down arrow between each; returns the card tops."""
    ys = [top + first + i * (h + gap) for i in range(len(cards))]
    for y, (label, kind) in zip(ys, cards):
        d.card(x + 30, y, label, kind, w=CW, h=h)
    for y in ys[1:]:
        d.arrow(f"M{x + 30 + CW / 2} {y - gap}V{y - 2}")
    return ys


def loop(x, ys, h, label):
    """Dashed arrow from the last card back up to the first, on the right of the cards."""
    a, b, e = x + 30 + CW, x + 30 + CW + 70, ys[-1] + h / 2
    d.arrow(f"M{a} {e}H{b}V{ys[0] + h / 2}H{a + 2}", back=True,
            label=label, at=(b, (ys[0] + e) / 2 + 6))


d.group(L, T1, GW, H1, "Once")
flow(L, T1, [("Retrieve|one search", "coding"),
             ("Generate|the answer", "write")], 64, 60)
d.notes(L, T1, H1, "The most common way", "Often not enough for multi-step reasoning")

d.group(R, T1, GW, H1, "Iterative")
ys = flow(R, T1, [("Retrieve|question + text so far", "coding"),
                  ("Generate|more text", "write")], 64, 60)
loop(R, ys, 64, "repeat")
d.notes(R, T1, H1, "e.g. ITER-RETGEN", "Risk: irrelevant info piles up")

d.group(L, T2, GW, H2, "Recursive")
ys = flow(L, T2, [("Refine the query|split into sub-problems", "plan"),
                  ("Retrieve", "coding"),
                  ("Generate", "write")], 56, 24, first=60)
loop(L, ys, 56, "refine")
d.notes(L, T2, H2, "IRCoT: chain-of-thought · ToC: clarification tree", "Or: search a summary, then inside the document")

d.group(R, T2, GW, H2, "Adaptive")
ys = flow(R, T2, [("LLM decides|search now? stop?", "plan"),
                  ("Retrieve|only when needed", "coding"),
                  ("Generate", "write")], 56, 24, first=60)
loop(R, ys, 56, "until it stops")
d.notes(R, T2, H2, "Often steered by special tokens", "FLARE: search when word probability drops")

d.save(Path(__file__).with_name("flows.svg"))
