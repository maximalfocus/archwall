"""graphify: what leaves your machine, and the safety checks.  Drawn from the graphify repo
(https://github.com/Graphify-Labs/graphify, README.md "Privacy"; ARCHITECTURE.md "Security";
graphify/security.py (validate_url: http/https only, private and metadata IPs blocked; 50 MB / 10 MB
fetch caps; validate_graph_path inside graphify-out; sanitize_label, 256 chars); graphify/querylog.py
(_log_path: off unless GRAPHIFY_QUERY_LOG or GRAPHIFY_QUERY_LOG_ENABLE is set; this settles README's
"Privacy" section, which still says on by default); graphify/serve.py serve_http (127.0.0.1 default,
API-key middleware); graphify/llm.py detect_backend; commit 35adf43).  Run: python3 privacy.py

Snake order: 1 stays on your machine (top left) -> 2 goes to an LLM (top right) -> 3 safety checks
(bottom right) -> 4 off unless you ask (bottom left)."""
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


def grid(x, top, cards, h=80, gap=16, y0=64):
    """Two columns of cards, filled row by row."""
    for i, (lbl, kind) in enumerate(cards):
        d.card(x + 30 + (i % 2) * 254, top + y0 + (i // 2) * (h + gap), lbl, kind, w=238, h=h)


def handoffs(a, b, c, ya=T1 + 206, yc=T2 + 200):
    """Arrows between the four groups in snake order, with what each one carries."""
    if a:
        d.arrow(f"M{L + W} {ya}H{R - 2}", label=a, at=(600, ya - 12))
    if b:
        d.arrow(f"M{R + W / 2} {T1 + H1}V{T2 - 2}", label=b, at=(R + W / 2 + 14 + len(b) * 4.6, T1 + H1 + 21))
    if c:
        d.arrow(f"M{R} {yc}H{L + W + 2}", label=c, at=(600, yc - 12))


d = Diagram("graphify: what leaves your machine",
            "1 Stays on your machine: code, parsed with tree-sitter, and video and audio, transcribed with "
            "faster-whisper. No telemetry. "
            "2 Goes to an LLM: docs, papers, images and transcripts, to the assistant's own model, or in "
            "headless runs to the API whose key you set, or to a local Ollama. "
            "3 Safety checks: fetched URLs must be http or https and may not point at private or cloud metadata "
            "addresses; downloads are capped at 50 MB with a timeout; graph paths must sit inside graphify-out; "
            "node labels are cleaned and capped at 256 characters. "
            "4 Off unless you ask: the query log is opt-in through an environment variable; the HTTP server "
            "listens on localhost unless you pass --host, and should get --api-key when you do.")

d.group(L, T1, W, H1, "Stays on your machine", 1)
col(L, T1, [("Code|tree-sitter", "coding"),
            ("Video, audio|faster-whisper", "coding")], h=80, gap=32, arrows=False)
d.note(L + W / 2, T1 + 320, "no telemetry")

d.group(R, T1, W, H1, "Goes to an LLM", 2)
col(R, T1, [("Docs, papers, images|the assistant's own model", "coding"),
            ("Headless runs|your API key, or local Ollama", "coding")], h=80, gap=32, arrows=False)
d.note(R + W / 2, T1 + 320, "Ollama keeps it all on your machine")

d.group(R, T2, W, H2, "Safety checks", 3)
grid(R, T2, [("URLs http(s)|no private IPs", "review"), ("Downloads|50 MB cap, timeout", "review"),
             ("Graph paths|inside graphify-out/", "review"), ("Labels|cleaned, 256 chars", "review")])

d.group(L, T2, W, H2, "Off unless you ask", 4)
col(L, T2, [("Query log|opt-in, env variable", "data"),
            ("HTTP server|localhost unless --host", "data")], h=80, gap=32, arrows=False)
d.note(L + W / 2, T2 + 300, "opening it up? set --api-key too")

handoffs("transcripts", None, None)
d.save(Path(__file__).with_name("privacy.svg"))
