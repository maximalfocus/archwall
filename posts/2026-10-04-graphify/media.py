"""graphify step 2b: docs, papers, images and video.  Drawn from the graphify repo
(https://github.com/Graphify-Labs/graphify, docs/how-it-works.md "Pass 2" and "Pass 3"; graphify/skill.md
Step 3 Part B (cache check B0, chunks of 20-25 files with each image alone B1, general-purpose subagents
B2, Gemini only when GEMINI_API_KEY / GOOGLE_API_KEY is set); graphify/skills/*/references/transcribe.md;
graphify/transcribe.py build_whisper_prompt; graphify/llm.py extract_corpus_parallel, detect_backend,
GRAPHIFY_MAX_RETRY_DEPTH bisection; graphify/validate.py; pyproject.toml extras video, anthropic, openai,
gemini, kimi, ollama, bedrock; commit 35adf43).  Run: python3 media.py

Snake order: 1 video and audio (top left) -> 2 batch (top right) -> 3 read with an LLM (bottom right)
-> 4 check and save (bottom left)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

L, R, W = 24, 624, 552
T1, H1 = 16, 412
T2, H2 = 460, 400


def col(x, top, cards, h=72, gap=24, arrows=True):
    """One column of wide cards, top to bottom, optionally joined by arrows."""
    for i, (lbl, kind) in enumerate(cards):
        y = top + 64 + i * (h + gap)
        d.card(x + 30, y, lbl, kind, w=492, h=h)
        if arrows and i:
            d.arrow(f"M{x + W / 2} {y - gap}V{y - 2}")


def handoffs(a, b, c, ya=T1 + 206, yc=T2 + 200):
    """Arrows between the four groups in snake order, with what each one carries."""
    if a:
        d.arrow(f"M{L + W} {ya}H{R - 2}", label=a, at=(600, ya - 12))
    if b:
        d.arrow(f"M{R + W / 2} {T1 + H1}V{T2 - 2}", label=b, at=(R + W / 2 + 14 + len(b) * 4.6, T1 + H1 + 21))
    if c:
        d.arrow(f"M{R} {yc}H{L + W + 2}", label=c, at=(600, yc - 12))


d = Diagram("graphify step 2b: docs, papers, images and video",
            "1 Video and audio, with the video extra: a one-line topic hint is written from the key concepts "
            "found so far, then faster-whisper transcribes on your machine. Transcripts are treated as docs. "
            "2 Batch the rest: files already in the SHA256 cache are skipped; the rest go into chunks of 20 to "
            "25 files, same folder together, each image on its own. "
            "3 Read with an LLM, the only pass that costs tokens: inside the assistant, parallel subagents on "
            "the assistant's own model, or Gemini if a Gemini key is set. Headless graphify extract uses an API "
            "backend such as Claude, OpenAI, Gemini or a local Ollama; their client libraries are extras. "
            "4 Check and save: each chunk returns JSON with nodes, edges and group links; a schema check warns "
            "about a bad chunk, and a chunk whose JSON will not parse is skipped; a reply cut off mid-way is "
            "split and retried; results go into the cache.")

d.group(L, T1, W, H1, "Video, audio (video extra)", 1)
col(L, T1, [("Topic hint|from key concepts so far", "plan"),
            ("faster-whisper|transcribes on your machine", "coding")], h=80, gap=40)
d.note(L + W / 2, T1 + 330, "transcripts are treated as docs")

d.group(R, T1, W, H1, "Batch the rest", 2)
col(R, T1, [("Check the cache|skip files already done", "review"),
            ("Chunks of 20–25 files|same folder together, images alone", "plan")], h=80, gap=40)

d.group(R, T2, W, H2, "Read with an LLM", 3)
col(R, T2, [("Parallel subagents|the assistant's own model", "coding"),
            ("Headless: graphify extract|Claude, OpenAI, Gemini, Ollama…", "coding")], h=80, gap=32,
    arrows=False)
d.note(R + W / 2, T2 + 300, "the only pass that costs tokens")
d.note(R + W / 2, T2 + 328, "API client libraries are extras")

d.group(L, T2, W, H2, "Check and save", 4)
col(L, T2, [("JSON per chunk|nodes, edges, group links", "write"),
            ("Schema check|warns; bad JSON: skipped", "review")], h=80, gap=32)
d.note(L + W / 2, T2 + 300, "a cut-off reply is split and retried")
d.note(L + W / 2, T2 + 328, "results go into the cache")

handoffs("transcripts", "chunks", "JSON")
d.save(Path(__file__).with_name("media.svg"))
