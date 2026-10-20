"""The retriever: how the search itself works, which embedding model does it, and three ways to make it better.
A map, not a snake: search (top left) uses an embedding model (top right); the bottom group is a catalogue
of improvements (hybrid retrieval, fine-tuning, adapters) with no order between them.
Drawn from Gao et al., "Retrieval-Augmented Generation for Large Language Models: A Survey",
arXiv:2312.10997v5 (Section II.A Naive RAG, Retrieval; III.D Embedding, incl. 1) Mix/hybrid Retrieval and
2) Fine-tuning Embedding Model; III.E Adapter).
Run: python3 search.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, R, GW, WIDE, T1, H1, T2, H2  # noqa: E402

d = Diagram("How the search works",
            "In: a user's question, and the chunk vectors already in the index. "
            "The search: embed the question with the same model used for the index, score each chunk "
            "by how similar its vector is to the question's, for example with cosine similarity, and keep "
            "the top K chunks for the prompt. "
            "The search uses an embedding model. There are two kinds: a sparse encoder such as BM25, and a "
            "dense retriever built on a BERT-style pre-trained model. Newer models include AngIE, Voyage and "
            "BGE. Leaderboards compare them: MTEB covers 8 tasks and 58 datasets; C-MTEB, for Chinese, covers "
            "6 tasks and 35 datasets. No one model fits every use. "
            "Three ways to make it better, in no order. "
            "Mix sparse and dense: sparse retrieval helps dense retrieval with rare entities and zero-shot "
            "questions, its results can help train dense models, and a pre-trained language model can learn "
            "term weights to boost sparse retrieval. "
            "Fine-tune the model: on your own domain data, for fields full of jargon such as healthcare and "
            "legal; or to align the retriever with the LLM, using the LLM's output as the training signal "
            "(LSR). REPLUG trains with KL divergence; LLM-Embedder uses rewards from the LLM. "
            "Add an adapter, when you cannot fine-tune because the model is only behind an API or compute is "
            "limited: BGM keeps the retriever and the LLM fixed and trains a bridge model between them; "
            "UPRISE, AAR and PRCA are other add-on adapters.")

d.pill(L, 16, WIDE, 48, "In: a user's question · chunk vectors already in the index")
d.arrow(f"M{L + GW / 2} 64V{T1 - 2}")

d.group(L, T1, GW, H1, "The search")
d.column(L, T1, [("Embed the question|same model as the index", "coding"),
                 ("Score each chunk|e.g. cosine similarity", "critic"),
                 ("Keep the top K|most similar chunks", "coding")])
d.notes(L, T1, H1, "Out: top K chunks for the prompt", "")

d.group(R, T1, GW, H1, "The embedding model")
d.column(R, T1, [("Sparse encoder|BM25", "data"),
                 ("Dense retriever|BERT-style model", "data"),
                 ("Newer models|AngIE · Voyage · BGE", "data")])
d.notes(R, T1, H1, "MTEB: 8 tasks · 58 datasets", "C-MTEB (Chinese): 6 tasks · 35 datasets")

d.arrow(f"M{L + GW} {T1 + 200}H{R - 2}", label="uses", at=(600, T1 + 188))

d.group(L, T2, WIDE, H2, "Ways to make it better")
SW, SY, SH = 352, T2 + 56, 284
for x, title, cards in [
    (48, "Mix sparse and dense",
     [("Sparse helps dense|rare entities · zero-shot", "plan"),
      ("Sparse results|help train dense models", "plan"),
      ("Learned term weights|a PLM boosts sparse", "plan")]),
    (424, "Fine-tune the model",
     [("Your own domain data|healthcare · legal jargon", "write"),
      ("Align with the LLM|LLM output as signal (LSR)", "write"),
      ("REPLUG: KL divergence|LLM-Embedder: LLM rewards", "write")]),
    (800, "Add an adapter",
     [("Can't fine-tune?|API only · little compute", "data"),
      ("BGM bridge model|fixed retriever ↔ fixed LLM", "coding"),
      ("Other adapters|UPRISE · AAR · PRCA", "coding")]),
]:
    d.sub(x, SY, SW, SH, title)
    for i, (label, kind) in enumerate(cards):
        d.card(x + 16, SY + 48 + i * 76, label, kind, w=SW - 32, h=64)

d.arrow(f"M{L + 200} {T2}V{T1 + H1 + 2}", label="improves", at=(L + 200, T1 + H1 + 24))
d.arrow(f"M{R + 352} {T2}V{T1 + H1 + 2}", label="improves", at=(R + 352, T1 + H1 + 24))

d.save(Path(__file__).with_name("search.svg"))
