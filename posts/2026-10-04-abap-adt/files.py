"""Where the code lives in ADT for VS Code.  From "ABAP Development Tools for VS Code: Everything You Need
to Know", sections "File-based development first", "SAP Joule for Developers Features Coming to VS Code" and
"ABAP Development Tools for VS Code Unlock Access to Cutting-Edge AI Tools" (Thomas Alexander Ritter,
2025-11-04, read 2026-10-05), linked from the "Behind the Design" post:
https://community.sap.com/t5/technology-blog-posts-by-sap/abap-development-tools-for-vs-code-everything-you-need-to-know/ba-p/14258129
Run: python3 files.py

Snake order: 1 you edit files (top left) -> 2 the virtual workspace (top right) -> 3 the ABAP server keeps
the objects (bottom right) -> 4 AI tools work on the files (bottom left), back up to the files."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("Files in VS Code, objects on the server",
            "1 In VS Code every object type is edited as a file, in the ABAP file formats, because VS Code is "
            "built for source files and AI tools work best on files. "
            "2 SAP implemented that file system with the virtual workspace technology. "
            "3 The ABAP objects themselves stay on the server. "
            "4 Any AI extension for VS Code can work on those files, though not every AI tool supports the "
            "virtual workspace yet. SAP plans to bring its Joule for developers features, such as predictive "
            "code completion, to VS Code.")

L, R, W = 24, 624, 552
T1, H1 = 16, 404
T2, H2 = 452, 432

# 1 files
d.group(L, T1, W, H1, "You edit files", 1)
d.card(L + 30, 80, "Every object type|as a file", "write", w=492, h=72)
d.card(L + 30, 182, "ABAP file|formats", "data", w=492, h=72)
d.note(L + W / 2, 354, "VS Code is built for files")
d.note(L + W / 2, 382, "AI tools work best on files")

# 2 virtual workspace
d.group(R, T1, W, H1, "Virtual workspace", 2)
d.card(R + 30, 130, "Virtual|file system", "coding", w=492, h=72)
d.note(R + W / 2, 354, "SAP built it with the")
d.note(R + W / 2, 382, "virtual workspace technology")

d.arrow(f"M{L + W} 166H{R + 28}", label="lives in", at=(600, 154))

# 3 server
d.group(R, T2, W, H2, "ABAP server", 3)
d.card(R + 30, T2 + 130, "ABAP objects|stay on the server", "data", w=492, h=72)

d.arrow(f"M{R + W - 70} 202V{T2 + 126}", label="backed by", at=(R + W - 70, T1 + H1 + 22))

# 4 AI
d.group(L, T2, W, H2, "AI tools", 4)
d.card(L + 30, T2 + 70, "AI extensions|for VS Code", "coding", w=492, h=72)
d.card(L + 30, T2 + 172, "Joule for developers|planned", "coding", w=492, h=72)
d.note(L + W / 2, T2 + 364, "Not every AI tool supports the")
d.note(L + W / 2, T2 + 392, "virtual workspace yet")

d.arrow(f"M{L + W / 2} {T2}V{T1 + H1 + 2}", label="work on the files", at=(L + W / 2 + 90, T1 + H1 + 22))

d.save(Path(__file__).with_name("files.svg"))
