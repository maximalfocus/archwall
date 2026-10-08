"""RAG next to the other ways to improve an LLM: prompt engineering, RAG, fine-tuning, side by side,
then what the survey found when it compared them (and RAG vs long context).
Options, not steps: three unnumbered columns, no arrows; one wide group of findings below.
Drawn from Gao et al., "Retrieval-Augmented Generation for Large Language Models: A Survey",
arXiv:2312.10997v5 (Section II.D RAG vs Fine-tuning, Fig. 4 caption, Section VII.A RAG vs Long Context).
Run: python3 compare.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, C3, CW3, WIDE  # noqa: E402

d = Diagram("RAG next to the other options",
            "Three ways to improve an LLM, side by side. "
            "Prompt engineering uses what the model can already do: it needs little outside knowledge "
            "and little change to the model, the least of the three on both. "
            "RAG is like giving the model a tailored textbook to look facts up in. Good: knowledge can be "
            "updated in real time from outside sources, and answers are easy to trace. Bad: answers are "
            "slower, and fetching data raises ethical questions. Early, naive RAG needs little change to "
            "the model; modular RAG leans more on fine-tuning. "
            "Fine-tuning is like a student learning the material over time, by training the model further. "
            "Good: it can copy a specific structure, style or format. Bad: it is static, so updates mean "
            "retraining, and it needs a lot of computing for data preparation and training. It can cut "
            "hallucinations but may struggle with unfamiliar data. "
            "What the survey reports: RAG beat unsupervised fine-tuning on knowledge-heavy tasks, for both "
            "known and new knowledge; LLMs struggle to learn new facts through unsupervised fine-tuning; "
            "and a long context of over 200,000 tokens does not replace RAG, because it is slower and a "
            "black box, while RAG shows the original sources so users can check the answer. "
            "RAG and fine-tuning are not either-or: used together they may work best.")

d.pill(L, 16, WIDE, 48, "Three ways to improve an LLM · side by side")

TOP, GH = 84, 456
CARD_W = CW3 - 60


def mark(col, i, good):
    """ok/bad mark at the right end of card i in column col."""
    x = C3[col] + 30 + CARD_W - 20
    y = TOP + 64 + i * 80 + 32
    (d.ok if good else d.bad)(x, y)


d.group(C3[0], TOP, CW3, GH, "Prompt engineering")
d.column(C3[0], TOP, [("Uses what the model|can already do", "plan"),
                      ("Outside knowledge|little needed", "data"),
                      ("Change to the model|little needed", "data")], w=CARD_W)
d.notes(C3[0], TOP, GH, "Needs the least of both", "", w=CW3)

d.group(C3[1], TOP, CW3, GH, "RAG")
d.column(C3[1], TOP, [("A tailored textbook|look the facts up", "coding"),
                      ("Real-time updates|from outside sources", "coding"),
                      ("Easy to trace|high interpretability", "critic"),
                      ("Slower answers|ethics of fetching data", "data")], w=CARD_W)
mark(1, 1, True)
mark(1, 2, True)
mark(1, 3, False)
d.notes(C3[1], TOP, GH, "Naive RAG: little model change", "Modular RAG: leans on fine-tuning", w=CW3)

d.group(C3[2], TOP, CW3, GH, "Fine-tuning (FT)")
d.column(C3[2], TOP, [("A student learns it|train the model more", "coding"),
                      ("Fits a structure|style or format", "write"),
                      ("Static|retrain to update", "data"),
                      ("Heavy compute|data prep and training", "data")], w=CARD_W)
mark(2, 1, True)
mark(2, 2, False)
mark(2, 3, False)
d.notes(C3[2], TOP, GH, "Can cut hallucinations", "may struggle with unfamiliar data", w=CW3)

BT, BH = 560, 304
d.group(L, BT, WIDE, BH, "What the survey reports")
BW, GAP = 352, 28
for i, (label, kind) in enumerate([("RAG beat unsupervised FT|on known and new facts", "critic"),
                                   ("Unsupervised FT|struggles with new facts", "critic"),
                                   ("200,000+ token context|does not replace RAG", "critic")]):
    d.card(L + 30 + i * (BW + GAP), BT + 64, label, kind, w=BW, h=64)
d.note(L + WIDE / 2, BT + 186, "Long context is slower and a black box; RAG shows its sources")
d.pill(L + 226, BT + 222, 700, 48, "Not either-or: RAG + fine-tuning together may work best")

d.save(Path(__file__).with_name("compare.svg"))
