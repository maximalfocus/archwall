"""Building the index: the required Naive RAG chain on top, the optional extras below.
Top row, steps in order: 1 clean the files, 2 split into chunks, 3 embed and store (Naive RAG indexing).
Bottom row, a catalogue with no order and no arrows: other sources, metadata, structure, each optional.
Drawn from Gao et al., "Retrieval-Augmented Generation for Large Language Models: A Survey",
arXiv:2312.10997v5 (Section II.A Naive RAG, Indexing; II.B Advanced RAG; Section III.A Retrieval Source;
Section III.B Indexing Optimization).
Run: python3 index.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, C3, CW3, T1, H1, T2, H2  # noqa: E402

d = Diagram("Building the index",
            "Naive RAG builds the index in three steps, in order. The rest is optional. "
            "1 Clean the files: raw files such as PDF, HTML, Word and Markdown, or text such as Wikipedia "
            "dumps and medical or legal data, cleaned into plain text. "
            "2 Split into chunks: most often a fixed number of tokens, for example 100, 256 or 512; or "
            "recursive splits and a sliding window; or Small2Big, which searches on a sentence and hands "
            "the LLM the sentences before and after it. The unit can be anything from a token, phrase, "
            "sentence or proposition up to a chunk or a whole document. Bigger units hold more context but "
            "more noise; smaller ones mean more retrieval work and may lose the meaning. Splitting a PDF can "
            "break its tables. "
            "3 Embed and store: an embedding model turns each chunk into a vector, and a vector database "
            "stores it. How well the index is built decides whether retrieval finds the right context. "
            "Optional, other sources: tables in PDFs can be turned into text, or "
            "kept in a database and queried with Text-2-SQL when a question comes in; knowledge graphs, "
            "searched by entity, triplet or sub-graph, which are checked and more precise but take work to "
            "build and maintain; and content the LLM writes itself. "
            "Optional, add metadata, which Advanced RAG uses: page number, file name, author, category and "
            "timestamp from the file, which the search can filter on; plus made-up metadata, such as "
            "paragraph summaries and hypothetical questions an LLM writes that the text can answer, known "
            "as Reverse HyDE. "
            "Optional, add structure: a hierarchical index, with files in parent-child order, chunks linked "
            "to them and a summary at each node to help pick chunks; or a knowledge graph index that links "
            "concepts and entities, which KGP builds across many documents.")

x1, x2, x3 = C3
W3 = CW3 - 60

d.pill(x1, 16, CW3, 48, "In: your documents")
d.arrow(f"M{x1 + CW3 / 2} 64V{T1 - 2}")
d.pill(x2, 16, x3 + CW3 - x2, 48, "Naive RAG: steps 1 to 3 in order · the rest is optional", "front")

d.group(x1, T1, CW3, H1, "Clean the files", 1)
d.column(x1, T1, [("Raw files|PDF · HTML · Word · Markdown", "data"),
                  ("Or plain text|Wikipedia · domain data", "data"),
                  ("Clean and extract|into plain text", "coding")], w=W3)
d.notes(x1, T1, H1, "Done ahead of time", "not for each question", w=CW3)

d.group(x2, T1, CW3, H1, "Split into chunks", 2)
d.column(x2, T1, [("Fixed size|100 · 256 · 512 tokens", "coding"),
                  ("Recursive · sliding window|or Small2Big", "coding"),
                  ("Unit size|token up to whole document", "plan")], w=W3)
d.notes(x2, T1, H1, "Bigger: more context · more noise", "Splitting can break PDF tables", w=CW3)

d.group(x3, T1, CW3, H1, "Embed and store", 3)
d.column(x3, T1, [("Embedding model|each chunk → a vector", "coding"),
                  ("Vector database|stores the vectors", "write")], w=W3)
d.notes(x3, T1, H1, "Index quality decides whether", "retrieval finds the right context", w=CW3)

ya = T1 + 200
d.arrow(f"M{x1 + CW3} {ya}H{x2 - 2}", label="text", at=((x1 + CW3 + x2) / 2, ya - 12))
d.arrow(f"M{x2 + CW3} {ya}H{x3 - 2}", label="chunks", at=((x2 + CW3 + x3) / 2, ya - 12))

d.group(x1, T2, CW3, H2, "Optional: other sources")
d.column(x1, T2, [("Tables in PDFs|turned into text", "data"),
                  ("Knowledge graph|entity · triplet · sub-graph", "data"),
                  ("LLM-made content|the model's own text", "write")], w=W3)
d.notes(x1, T2, H2, "Or keep tables in a database", "and query them by Text-2-SQL", w=CW3)

d.group(x2, T2, CW3, H2, "Optional: metadata")
d.column(x2, T2, [("From the file|page · file name · author", "write"),
                  ("Made-up metadata|paragraph summaries", "write"),
                  ("Hypothetical questions|LLM-made · Reverse HyDE", "write")], w=W3)
d.notes(x2, T2, H2, "Used by Advanced RAG", "Search can filter on metadata", w=CW3)

d.group(x3, T2, CW3, H2, "Optional: structure")
d.column(x3, T2, [("Hierarchical index|parent-child · chunks linked", "plan"),
                  ("Summary at each node|helps pick chunks", "write"),
                  ("Knowledge graph index|links concepts · entities", "plan")], w=W3)
d.notes(x3, T2, H2, "KGP: one graph across documents", w=CW3)

d.save(Path(__file__).with_name("index.svg"))
