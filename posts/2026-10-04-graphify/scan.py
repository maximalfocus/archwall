"""graphify step 1: read the folder.  Drawn from the graphify repo
(https://github.com/Graphify-Labs/graphify, graphify/detect.py: detect(), _is_sensitive(), _SKIP_DIRS,
classify_file(), extract_pdf_text(), CORPUS_WARN_THRESHOLD / CORPUS_UPPER_THRESHOLD / FILE_COUNT_UPPER;
graphify/ingest.py; README.md "Ignoring files" and "What files it handles";
pyproject.toml extras office, google, video, pdf;
commit 35adf43).  Run: python3 scan.py

Snake order: 1 what goes in (top left) -> 2 skip (top right) -> 3 convert (bottom right)
-> 4 sort and check (bottom left)."""
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


d = Diagram("graphify step 1: read the folder",
            "1 What goes in: your folder (or several, or a GitHub URL), and anything you fetch with graphify add: "
            "a paper, a web page, a tweet or a video; video URLs need the video extra. "
            "2 Skip: .gitignore is respected, .graphifyignore adds your own rules, build output such as "
            "node_modules, dist and virtual envs is pruned, and secret files such as .env, keys and credentials "
            "are skipped by name and listed, never read. "
            "3 Convert: Word and Excel files become Markdown with the office extra; Google Docs shortcuts are "
            "opt-in and need the gws command-line tool. The Markdown lands in graphify-out/converted. "
            "4 Sort and check: every file becomes code, document, paper, image or video; unknown files are "
            "listed and left out. PDF text extraction (word counts, headless runs) needs the pdf extra; "
            "under 50,000 words graphify says you may not need a graph; over 500,000 words or 500 files it "
            "warns the LLM pass will be costly.")

d.group(L, T1, W, H1, "What goes in", 1)
col(L, T1, [("Your folder|or several, or a GitHub URL", "data"),
            ("graphify add <url>|paper, web page, tweet, video", "data")], h=80, gap=32, arrows=False)
d.note(L + W / 2, T1 + 320, "fetched pages are saved as Markdown")
d.note(L + W / 2, T1 + 348, "video URLs need the video extra")

d.group(R, T1, W, H1, "Skip", 2)
grid(R, T1, [(".gitignore|respected", "review"), (".graphifyignore|your own rules", "review"),
             ("Build output|node_modules, dist", "review"), ("Secret files|.env, keys", "review")])
d.note(R + W / 2, T1 + 300, "secrets are skipped by name,")
d.note(R + W / 2, T1 + 328, "listed in the summary, never read")

d.group(R, T2, W, H2, "Convert", 3)
col(R, T2, [("Word, Excel → Markdown|office extra", "coding"),
            ("Google Docs shortcuts|opt-in, needs the gws tool", "coding")], h=80, gap=32, arrows=False)
d.note(R + W / 2, T2 + 300, "saved in graphify-out/converted/")

d.group(L, T2, W, H2, "Sort and check", 4)
grid(L, T2, [("Code", "data"), ("Document", "data"), ("Paper|PDF or reads like one", "data"),
             ("Image", "data"), ("Video, audio", "data"), ("Unknown|listed, left out", "data")],
     h=64, gap=12, y0=60)
d.note(L + W / 2, T2 + 318, "under 50,000 words: may not need a graph")
d.note(L + W / 2, T2 + 346, "over 500,000 words or 500 files: costly")

handoffs("paths", "kept files", "Markdown")
d.save(Path(__file__).with_name("scan.svg"))
