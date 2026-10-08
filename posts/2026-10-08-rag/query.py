"""Fixing the question before the search: why, then three families of query optimization.
A catalogue, not stages: expand, transform and route are separate options with no order between them.
Drawn from Gao et al., "Retrieval-Augmented Generation for Large Language Models: A Survey",
arXiv:2312.10997v5 (Section III.C Query Optimization: 1 Query Expansion, 2 Query Transformation, 3 Query Routing).
Run: python3 query.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, R, GW, T1, H1, T2, H2  # noqa: E402

d = Diagram("Fix the question first",
            "In: the user's question, as typed. Naive RAG searches with it directly, and a poor question "
            "finds poor chunks. "
            "Why fix it: words can be ambiguous, for example \"LLM\" can mean a large language model or a "
            "Master of Laws; and a question can be complex and not well organized. "
            "Three ways to fix it, with no order between them. "
            "Expand, one question becomes many: multi-query has an LLM write several queries and runs them "
            "in parallel; sub-query breaks a complex question into simpler sub-questions with least-to-most "
            "prompting; Chain-of-Verification has an LLM check the expanded queries to cut hallucinations. "
            "Transform, search with a changed question: rewrite it with an LLM or a smaller model such as "
            "RRR; HyDE writes a hypothetical answer and searches with that; step-back prompting writes a "
            "more general question and searches with it and the original. Taobao's rewrite, BEQUE, raised "
            "recall for long-tail queries. "
            "Route, send each question to a fitting RAG pipeline: a metadata router pulls keywords from the "
            "question and filters chunks on them; a semantic router goes by what the question means; or mix "
            "both.")

d.pill(L, 16, 1152, 48, "In: the user's question, as typed · three ways to fix it before the search")

d.group(L, T1, GW, H1, "Why fix it")
d.column(L, T1, [("Ambiguous words|\"LLM\": language model or law degree?", "data"),
                 ("Messy questions|complex · not well organized", "data"),
                 ("Naive RAG searches as is|poor question · poor chunks", "data")])

d.group(R, T1, GW, H1, "Expand: one becomes many")
d.column(R, T1, [("Multi-query|LLM writes several · run in parallel", "coding"),
                 ("Sub-query|split into simpler questions", "coding"),
                 ("Chain-of-Verification|LLM checks the new queries", "critic")])
d.notes(R, T1, H1, "Sub-query uses least-to-most prompting", "Checked queries: fewer hallucinations")

d.group(L, T2, GW, H2, "Transform: search with a new question")
d.column(L, T2, [("Rewrite|by an LLM or a small model (RRR)", "coding"),
                 ("HyDE|search with a made-up answer", "coding"),
                 ("Step-back question|searched along with the original", "coding")])
d.notes(L, T2, H2, "Taobao's BEQUE rewrite: better recall", "for long-tail queries")

d.group(R, T2, GW, H2, "Route: pick the right pipeline")
d.column(R, T2, [("Metadata router|keywords filter the chunks", "plan"),
                 ("Semantic router|by what the question means", "plan"),
                 ("Hybrid routing|semantic + metadata", "plan")])

d.save(Path(__file__).with_name("query.svg"))
