"""RAG overview: index your documents, find the chunks that match a question, trim them, let the LLM answer.
Snake order: 1 index (top left) -> 2 retrieve (top right) -> 3 curate (bottom right) -> 4 generate (bottom left).
Drawn from Gao et al., "Retrieval-Augmented Generation for Large Language Models: A Survey",
arXiv:2312.10997v5 (Section II.A Naive RAG, II.B Advanced RAG, Fig. 2 and Fig. 3).
Run: python3 diagram.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, R, GW, T1, H1, T2, H2  # noqa: E402

d = Diagram("RAG overview",
            "In: your documents, and a user's question. "
            "1 Index, done ahead of time: clean the raw files (PDF, HTML, Word, Markdown) into plain text, "
            "split the text into chunks, turn each chunk into a vector with an embedding model, and store "
            "the vectors in a vector database. "
            "2 Retrieve, for each question: Advanced RAG first rewrites or expands the question; the same "
            "embedding model turns the question into a vector, and the system takes the top K chunks most "
            "similar to it. "
            "3 Curate, added by Advanced RAG: rerank the chunks so the most relevant come first, and compress "
            "them so the LLM is not flooded with noise. "
            "4 Generate: the question and the chosen chunks, plus any chat history, go into one prompt, and "
            "the LLM writes the answer from it. Naive RAG is steps 1, 2 and 4 only.")

d.pill(L, 16, GW, 48, "In: your documents")
d.arrow(f"M{L + GW / 2} 64V{T1 - 2}")
d.pill(R, 16, GW, 48, "In: a user's question")
d.arrow(f"M{R + GW / 2} 64V{T1 - 2}")

d.group(L, T1, GW, H1, "Index, ahead of time", 1)
d.column(L, T1, [("Clean the files|PDF · HTML · Word → plain text", "coding"),
                 ("Split into chunks|small enough for the LLM", "coding"),
                 ("Embed each chunk|an embedding model → a vector", "coding"),
                 ("Store the vectors|in a vector database", "data")], h=60, gap=14, first=60)

d.group(R, T1, GW, H1, "Retrieve, per question", 2)
d.column(R, T1, [("Rewrite the question|Advanced RAG", "plan"),
                 ("Embed the question|same model as the index", "coding"),
                 ("Take the top K chunks|most similar vectors", "coding")])

d.group(R, T2, GW, H2, "Curate the chunks", 3)
d.column(R, T2, [("Rerank|most relevant first", "critic"),
                 ("Compress|cut the noise", "critic")])
d.notes(R, T2, H2, "Added by Advanced RAG", "Naive RAG skips this step")

d.group(L, T2, GW, H2, "Generate", 4)
d.column(L, T2, [("Build the prompt|question + chunks + history", "write"),
                 ("LLM|answers from the prompt", "coding"),
                 ("Answer|back to the user", "write")])

d.arrow(f"M{L + GW} {T1 + 200}H{R - 2}", label="vector index", at=(600, T1 + 188))
d.arrow(f"M{R + 276} {T1 + H1}V{T2 - 2}", label="top K chunks", at=(R + 276, T1 + H1 + 24))
d.arrow(f"M{R} {T2 + 136}H{L + GW + 2}", label="best chunks", at=(600, T2 + 124))

d.save(Path(__file__).with_name("diagram.svg"))
