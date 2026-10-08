"""Building the index: gather the sources, pick the unit size, split, tag, add structure, embed and store.
Snake order in three columns: 1 sources, 2 unit size, 3 chunking (top row, left to right), then
4 metadata, 5 structure, 6 embed and store (bottom row, right to left).
Drawn from Gao et al., "Retrieval-Augmented Generation for Large Language Models: A Survey",
arXiv:2312.10997v5 (Section II.A Naive RAG, Indexing; Section III.A Retrieval Source;
Section III.B Indexing Optimization).
Run: python3 index.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, C3, CW3, T1, H1, T2, H2  # noqa: E402

d = Diagram("Building the index",
            "In: raw files such as PDF, HTML, Word and Markdown, cleaned into plain text. "
            "1 Gather the sources: unstructured text, such as Wikipedia dumps or domain data like medical "
            "or legal text; PDFs that mix text and tables, handled with Text-2-SQL on the tables or by "
            "turning the tables into text; knowledge graphs, which are checked and more precise but take "
            "work to build and maintain; and content the LLM writes itself. "
            "2 Pick the unit size: in text, from fine to coarse, token, phrase, sentence, proposition, "
            "chunk and document; in a knowledge graph, entity, triplet and sub-graph. Coarse units carry "
            "more information but also more noise; fine units mean more retrieval work and may lose the meaning. "
            "3 Split into chunks: most often a fixed number of tokens, for example 100, 256 or 512; or "
            "recursive splits and a sliding window; or Small2Big, which searches on a sentence and hands "
            "the LLM the sentences before and after it. Bigger chunks hold more context but more noise, and splitting "
            "a PDF can break its tables. "
            "4 Add metadata: page number, file name, author, category and timestamp from the file, which the "
            "search can filter on; plus made-up metadata, such as paragraph summaries and hypothetical "
            "questions an LLM writes that the text can answer, known as Reverse HyDE. "
            "5 Add structure: a hierarchical index, with files in parent-child order, chunks linked to them "
            "and a summary at each node to help pick chunks; or a knowledge graph index that links concepts "
            "and entities, which KGP builds across many documents. "
            "6 Embed and store: an embedding model turns each chunk into a vector, and a vector database "
            "stores it. How well the index is built decides whether retrieval finds the right context.")

x1, x2, x3 = C3
W3 = CW3 - 60

d.pill(24, 16, 1152, 48, "In: raw files (PDF · HTML · Word · Markdown) cleaned into plain text")
d.arrow(f"M{x1 + CW3 / 2} 64V{T1 - 2}")

d.group(x1, T1, CW3, H1, "Gather sources", 1)
d.column(x1, T1, [("Text|Wikipedia · domain data", "data"),
                  ("PDF with tables|Text-2-SQL or table → text", "data"),
                  ("Knowledge graph|precise · work to maintain", "data"),
                  ("LLM-made content|the model's own text", "write")], h=60, gap=14, first=60, w=W3)

d.group(x2, T1, CW3, H1, "Pick the unit size", 2)
d.column(x2, T1, [("Text, fine to coarse|token · phrase · sentence", "plan"),
                  ("… and on up|proposition · chunk · doc", "plan"),
                  ("Knowledge graph|entity · triplet · sub-graph", "plan")], w=W3)
d.notes(x2, T1, H1, "Coarse: more info · more noise", "Fine: more work · may lose meaning", w=CW3)

d.group(x3, T1, CW3, H1, "Split into chunks", 3)
d.column(x3, T1, [("Fixed size|100 · 256 · 512 tokens", "coding"),
                  ("Recursive splits|sliding window", "coding"),
                  ("Small2Big|small to search · big to send", "coding")], w=W3)
d.notes(x3, T1, H1, "Bigger: more context · more noise", "Splitting can break PDF tables", w=CW3)

d.group(x3, T2, CW3, H2, "Add metadata", 4)
d.column(x3, T2, [("From the file|page · file name · author", "write"),
                  ("Made-up metadata|paragraph summaries", "write"),
                  ("Hypothetical questions|LLM-made · Reverse HyDE", "write")], w=W3)
d.notes(x3, T2, H2, "Also category · timestamp", "Search can filter on metadata", w=CW3)

d.group(x2, T2, CW3, H2, "Add structure", 5)
d.column(x2, T2, [("Hierarchical index|parent-child · chunks linked", "plan"),
                  ("Summary at each node|helps pick chunks", "write"),
                  ("Knowledge graph index|links concepts · entities", "plan")], w=W3)
d.notes(x2, T2, H2, "KGP: one graph across documents", w=CW3)

d.group(x1, T2, CW3, H2, "Embed and store", 6)
d.column(x1, T2, [("Embedding model|each chunk → a vector", "coding"),
                  ("Vector database|stores the vectors", "write")], w=W3)
d.notes(x1, T2, H2, "Index quality decides whether", "retrieval finds the right context", w=CW3)

ya = T1 + 280
d.arrow(f"M{x1 + CW3} {ya}H{x2 - 2}", label="text", at=((x1 + CW3 + x2) / 2, ya - 12))
d.arrow(f"M{x2 + CW3} {ya}H{x3 - 2}", label="unit", at=((x2 + CW3 + x3) / 2, ya - 12))
d.arrow(f"M{x3 + CW3 / 2} {T1 + H1}V{T2 - 2}", label="chunks", at=(x3 + CW3 / 2 + 50, T1 + H1 + 24))
yb = T2 + 240
d.arrow(f"M{x3} {yb}H{x2 + CW3 + 2}", label="tagged", at=((x2 + CW3 + x3) / 2, yb - 12))
d.arrow(f"M{x2} {yb}H{x1 + CW3 + 2}", label="linked", at=((x1 + CW3 + x2) / 2, yb - 12))

d.save(Path(__file__).with_name("index.svg"))
