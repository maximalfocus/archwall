"""Why a new IDE for ABAP was hard: the two problems SAP names in "Behind the Design"
(Thomas Alexander Ritter, 2025-11-04, read 2026-10-05), sections "Introduction" and
"How Do We Transform the ABAP Development Tools Architecture to Offer More Choice?":
https://community.sap.com/t5/technology-blog-posts-by-sap/behind-the-design-how-we-transformed-the-abap-development-tools/ba-p/14258121
Run: python3 problem.py

Snake order: 1 what users ask for (top left) -> 2 problem one, the client layer (top right) ->
3 problem two, the editors (bottom right) -> 4 the two fixes (bottom left)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("Why a new IDE was hard",
            "1 Users want more choice: in SAP's 2023 and 2025 surveys VS Code was the most requested IDE; "
            "others asked for JetBrains IDEs, Neovim or Zed. Official ABAP tools existed only for SAP GUI and Eclipse. "
            "2 Problem one: every IDE needs a client layer that talks to the ABAP server, wraps the REST APIs, "
            "keeps old releases working and holds the debugger, test runner, ATC and tracing: 2.9 million lines "
            "with no UI. "
            "3 Problem two: ABAP has many object type editors, 88 on the SAP BTP ABAP environment alone in 2025, "
            "against one for CAP (CDS) and three for Java (class, interface, enumeration). "
            "4 The fixes: reuse the client layer as a language server, and make editors server-driven.")

L, R, W = 24, 624, 552
T1, H1 = 16, 404
T2, H2 = 452, 432

# 1 users
d.group(L, T1, W, H1, "Users want more IDEs", 1)
d.card(L + 30, 80, "Surveys 2023, 2025|VS Code most requested", None, w=492, h=72)
d.card(L + 30, 182, "Also asked for|JetBrains, Neovim, Zed", w=492, h=72, cls="human")
d.note(L + W / 2, 354, "Official ABAP tools: only SAP GUI")
d.note(L + W / 2, 382, "and Eclipse")

# 2 client layer
d.group(R, T1, W, H1, "Problem 1: the client layer", 2)
d.card(R + 30, 80, "Talks to the ABAP server|wraps the REST APIs", "coding", w=492, h=72)
d.card(R + 30, 182, "Debugger, test runner|ATC, tracing", "coding", w=492, h=72)
d.note(R + W / 2, 354, "2.9 million lines with no UI")
d.note(R + W / 2, 382, "every new IDE needs one")

d.arrow(f"M{L + W} 218H{R - 2}", label="blocked by", at=(600, 206))

# 3 editors
d.group(R, T2, W, H2, "Problem 2: the editors", 3)
d.card(R + 30, T2 + 70, "ABAP on SAP BTP|88 editors (2025)", None, w=492, h=72)
d.card(R + 30, T2 + 172, "CAP|1 editor (CDS)", None, w=236, h=72)
d.card(R + 286, T2 + 172, "Java|class, interface, enum", None, w=236, h=72)
d.note(R + W / 2, T2 + 364, "every new IDE would need them all")

d.arrow(f"M{R + W / 2} {T1 + H1}V{T2 - 2}", label="and", at=(R + W / 2 + 34, T1 + H1 + 22))

# 4 fixes
d.group(L, T2, W, H2, "The two fixes", 4)
d.card(L + 30, T2 + 70, "Reuse the client layer|as a language server", "plan", w=492, h=72)
d.card(L + 30, T2 + 172, "Server-driven editors|two renderers", "plan", w=492, h=72)
d.note(L + W / 2, T2 + 364, "six years of rework, VS Code in 2026")

d.arrow(f"M{R} {T2 + 208}H{L + W + 2}", label="solved by", at=(600, T2 + 196))

d.save(Path(__file__).with_name("problem.svg"))
