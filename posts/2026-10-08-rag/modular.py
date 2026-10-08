"""Modular RAG's building blocks: the new modules and the new patterns, grouped by job.
A catalogue, not a flow: the four groups have no order between them. Loops and adaptive flows
get their own figure (flows.svg), so here they are one card each.
Drawn from Gao et al., "Retrieval-Augmented Generation for Large Language Models: A Survey",
arXiv:2312.10997v5 (Section II.C Modular RAG: 1) New Modules, 2) New Patterns).
Run: python3 modular.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, R, GW, T1, H1, T2, H2  # noqa: E402

d = Diagram("Modular RAG building blocks",
            "Modular RAG builds on Naive and Advanced RAG, but lets you swap parts, add new ones, or change "
            "the order they run in. The parts are grouped here by job, not by order. "
            "Modules that find: Search lets the LLM write code or query languages to search engines, databases "
            "and knowledge graphs; RAG-Fusion turns one query into several, searches them in parallel and "
            "reranks the results; Memory uses the LLM's own memory to guide retrieval. "
            "Modules that pick or fit: Routing picks the right path for a query, such as a summary, a "
            "specific database, or merging several streams; Predict has the LLM write the context itself, to "
            "cut noise and repetition; Task Adapter fits RAG to a downstream task, retrieving prompts for "
            "zero-shot inputs and building task-specific retrievers from few-shot query generation. "
            "Patterns that change the chain: Rewrite-Retrieve-Read has the LLM rewrite the query first; "
            "Generate-Read uses text the LLM writes instead of retrieval, and Recite-Read recalls from the "
            "model's weights; hybrid retrieval mixes keyword, semantic and vector search; sub-queries and "
            "HyDE match a drafted answer against real documents. "
            "Patterns that loop or adapt: Demonstrate-Search-Predict feeds one module's output into "
            "another; ITER-RETGEN runs Retrieve-Read-Retrieve-Read; FLARE and Self-RAG decide whether "
            "retrieval is needed at all; and the flexible setup makes it easier to fine-tune the retriever, "
            "the generator, or both together.")

d.pill(L, 16, 1152, 48, "Modular RAG: swap parts · add new ones · change the order · grouped by job")

d.group(L, T1, GW, H1, "Modules that find")
d.column(L, T1, [("Search|LLM writes code or queries", "coding"),
                 ("RAG-Fusion|many queries · parallel search · rerank", "coding"),
                 ("Memory|the LLM's own memory guides retrieval", "data")])
d.notes(L, T1, H1, "Search reaches engines · databases · graphs", "")

d.group(R, T1, GW, H1, "Modules that pick or fit")
d.column(R, T1, [("Routing|summary · a database · merge streams", "plan"),
                 ("Predict|the LLM writes the context itself", "write"),
                 ("Task Adapter|fit RAG to a downstream task", "plan")])
d.notes(R, T1, H1, "Predict: less noise and repetition", "Task Adapter: zero-shot · few-shot")

d.group(L, T2, GW, H2, "Patterns that change the chain")
d.column(L, T2, [("Rewrite-Retrieve-Read|LLM rewrites the query first", "plan"),
                 ("Generate-Read · Recite-Read|from the LLM's output or its weights", "write"),
                 ("Hybrid retrieval|keyword + semantic + vector", "coding"),
                 ("Sub-queries · HyDE|match a drafted answer to real docs", "coding")],
         h=60, gap=14, first=60)

d.group(R, T2, GW, H2, "Patterns that loop or adapt")
d.column(R, T2, [("Demonstrate-Search-Predict|one module's output helps another", "coding"),
                 ("ITER-RETGEN|Retrieve-Read-Retrieve-Read", "coding"),
                 ("FLARE · Self-RAG|decide if retrieval is needed", "plan"),
                 ("Easier fine-tuning|retriever · generator · or both", "critic")],
         h=60, gap=14, first=60)

d.save(Path(__file__).with_name("modular.svg"))
