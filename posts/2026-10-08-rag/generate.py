"""RAG generation: from the retrieved chunks to the answer.
Three stages: 1 rerank (top left) -> 2 select and compress (top right) -> 3 build the prompt and answer
(wide bottom group), with fine-tuning the LLM as a side sub-group that feeds the LLM.
Drawn from Gao et al., "Retrieval-Augmented Generation for Large Language Models: A Survey",
arXiv:2312.10997v5 (Section II.A Naive RAG: Generation; II.B Advanced RAG: Post-Retrieval Process;
Section IV Generation: A. Context Curation, B. LLM Fine-tuning).
Run: python3 generate.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, R, GW, WIDE, T1, H1, T2, H2  # noqa: E402

d = Diagram("From chunks to answer",
            "In: the question and its top K retrieved chunks. Feeding them all straight to the LLM is not "
            "a good idea: too much context adds noise, and in long text LLMs focus on the start and the end "
            "and lose the middle. "
            "1 Rerank: put the most relevant chunks first, with rules (diversity, relevance, MRR) or with "
            "models (the BERT family, Cohere rerank, bge-reranker-large, or a general LLM like GPT), and move "
            "the best chunks to the edges of the prompt. "
            "2 Select and compress: LLMLingua uses a small language model, GPT-2 Small or LLaMA-7B, to drop "
            "unimportant tokens; PRCA and RECOMP train a compressor; fewer documents also help: in "
            "Filter-Reranker small models filter and the LLM reorders, or the LLM critiques the retrieved "
            "documents and drops weak ones, as in Chatlaw. "
            "3 Build the prompt and answer: the question and the kept chunks go into one prompt, plus the chat "
            "history in a multi-turn chat; the LLM answers from its own knowledge or only from the documents, "
            "depending on the task. "
            "Beside this, you can also adjust the LLM itself by fine-tuning it: add domain knowledge it lacks, "
            "set the format and style of its answers, align it with human or retriever preferences through "
            "reinforcement learning, or distill a stronger model such as GPT-4. RA-DIT tunes the LLM and the "
            "retriever together. It is a big plus of on-premise LLMs.")

d.pill(L, 16, GW, 48, "In: the question · its top K chunks")
d.arrow(f"M{L + GW / 2} 64V{T1 - 2}")

d.group(L, T1, GW, H1, "Rerank", 1)
d.column(L, T1, [("By rules|diversity · relevance · MRR", "critic"),
                 ("By a model|BERT · Cohere · bge · GPT", "critic"),
                 ("Best chunks to the edges|start and end of the prompt", "plan")])
d.notes(L, T1, H1, "Lost in the middle: LLMs focus", "on the start and end of long text")

d.group(R, T1, GW, H1, "Select and compress", 2)
d.column(R, T1, [("Drop unimportant tokens|LLMLingua · a small model", "critic"),
                 ("Trained compressor|PRCA · RECOMP", "critic"),
                 ("Drop weak documents|small model filters · LLM critique", "review")])
d.notes(R, T1, H1, "Too much context adds noise", "Small model: GPT-2 Small or LLaMA-7B")

d.group(L, T2, WIDE, H2, "Build the prompt and answer", 3)
d.column(L, T2, [("Prompt|question + kept chunks", "write"),
                 ("Chat history|in a multi-turn chat", "data"),
                 ("LLM answers|own knowledge or only the docs", "coding")])
d.note(L + GW / 2, T2 + H2 - 26, "Which one depends on the task")

SX, SY, SW, SH = R, T2 + 56, WIDE - (R - L) - 24, H2 - 74
d.sub(SX, SY, SW, SH, "Also: fine-tune the LLM")
cw = (SW - 60) // 2
for i, (label, kind) in enumerate([("Domain knowledge|it lacks", "write"),
                                   ("Format and style|of the answers", "plan"),
                                   ("Align by RL|human or retriever", "plan"),
                                   ("Distill a stronger LLM|such as GPT-4", "write")]):
    d.card(SX + 20 + (i % 2) * (cw + 20), SY + 48 + (i // 2) * 76, label, kind, w=cw, h=64)
d.note(SX + SW / 2, SY + SH - 44, "RA-DIT tunes LLM and retriever together")
d.note(SX + SW / 2, SY + SH - 18, "A big plus of on-premise LLMs")

d.arrow(f"M{L + GW} {T1 + 200}H{R - 2}", label="reranked", at=(600, T1 + 188))
d.arrow(f"M{R + 276} {T1 + H1}V{T1 + H1 + 18}H{L + 276}V{T2 + 62}", label="kept chunks", at=(R + 120, T1 + H1 + 24))
d.arrow(f"M{SX} {T2 + 256}H{L + GW - 28}", label="tunes", at=(SX - 25, T2 + 246))

d.save(Path(__file__).with_name("generate.svg"))
