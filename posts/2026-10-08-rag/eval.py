"""Checking a RAG system: what it is tested on, the two targets (retrieval and generation quality)
with their metrics, quality scores and abilities, and the benchmarks and tools that check them.
A catalogue: unnumbered groups, one labelled relation arrow ("check"), no steps.
Drawn from Gao et al., "Retrieval-Augmented Generation for Large Language Models: A Survey",
arXiv:2312.10997v5 (Section VI Task and Evaluation, Tables II-IV; task and dataset count in Section I).
Run: python3 eval.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, R, GW, T1, H1, T2, H2  # noqa: E402

d = Diagram("Checking a RAG system",
            "In: a RAG system to check, on two targets, retrieval and generation, either by hand or "
            "automatically. "
            "What it is tested on: question answering is the core task, single-hop, multi-hop and long-form, "
            "plus domain questions and multiple choice; other tasks include information extraction, dialogue "
            "and code search. The survey counts 26 tasks and nearly 50 datasets. "
            "Benchmarks and tools check both targets: the benchmarks RGB, RECALL and CRUD test the four "
            "abilities; the tools RAGAS, ARES and TruLens use an LLM to grade the three quality scores. "
            "Classic metrics such as EM, F1, BLEU and ROUGE are traditional and not yet a standard for RAG. "
            "Retrieval quality: search metrics Hit Rate, MRR and NDCG; the score context relevance, meaning "
            "the retrieved text is on point with no extras; and the ability noise robustness, meaning the "
            "system copes with documents that are related to the question but hold nothing useful. "
            "Generation quality: without labels, the answer should be faithful, relevant and not harmful; "
            "with labels, it should be accurate. The scores answer faithfulness and answer relevance. "
            "Three abilities: negative rejection, saying no when the documents lack the answer; information "
            "integration, combining several documents; and counterfactual robustness, ignoring known "
            "false facts in the documents.")

d.pill(L, 16, 1152, 48, "In: a RAG system · two targets: retrieval and generation · checked by hand or automatically")

d.group(L, T1, GW, H1, "What it is tested on")
d.column(L, T1, [("Question answering|single-hop · multi-hop · long-form", "data"),
                 ("More question answering|domain · multiple choice", "data"),
                 ("Other tasks|extraction · dialogue · code search", "data")])
d.notes(L, T1, H1, "Question answering is the core task", "26 tasks · nearly 50 datasets")

d.group(R, T1, GW, H1, "Benchmarks and tools")
d.column(R, T1, [("Benchmarks: RGB · RECALL · CRUD|test the four abilities", "critic"),
                 ("Tools: RAGAS · ARES · TruLens|an LLM grades the three scores", "critic"),
                 ("Classic: EM · F1 · BLEU · ROUGE|not yet a standard for RAG", "data")])

d.group(L, T2, GW, H2, "Retrieval quality")
d.column(L, T2, [("Search metrics|Hit Rate · MRR · NDCG", "critic"),
                 ("Score: context relevance|on point · no extras", "critic"),
                 ("Ability: noise robustness|cope with related but empty docs", "critic")])

d.group(R, T2, GW, H2, "Generation quality")
d.column(R, T2, [("Without labels|faithful · relevant · not harmful", "critic"),
                 ("With labels|accurate", "critic"),
                 ("Scores|answer faithfulness · answer relevance", "critic"),
                 ("Abilities|say no · combine docs · ignore false facts", "critic")],
         h=60, gap=14, first=60)

# Benchmarks and tools check both targets.
d.arrow(f"M{R + 276} {T1 + H1}V{T2 - 2}", label="check", at=(R + 276, T1 + H1 + 24))
d.arrow(f"M{R + 100} {T1 + H1}V{T1 + H1 + 18}H{L + GW / 2}V{T2 - 2}", label="check", at=(450, T1 + H1 + 24))

d.save(Path(__file__).with_name("eval.svg"))
