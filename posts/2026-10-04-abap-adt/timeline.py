"""How ADT got to VS Code, year by year.  Every date is from SAP's two posts of 2025-11-04 by Thomas
Alexander Ritter (read 2026-10-05):
"Behind the Design" https://community.sap.com/t5/technology-blog-posts-by-sap/behind-the-design-how-we-transformed-the-abap-development-tools/ba-p/14258121
(2018 TypeScript language server explored; 2018 SAP BTP ABAP Environment launched, Eclipse only; 2020 number
range objects, the first server-driven type; 2023 and 2025 surveys; 88 editors as of 2025; "over the past six
years"; VS Code in 2026) and "ABAP Development Tools for VS Code: Everything You Need to Know"
https://community.sap.com/t5/technology-blog-posts-by-sap/abap-development-tools-for-vs-code-everything-you-need-to-know/ba-p/14258129
Run: python3 timeline.py

Snake order: 1 the rework, 2018 to 2020, top to bottom on the left -> 2 toward VS Code, 2023 to 2026,
top to bottom on the right."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("ADT timeline",
            "1 The rework. 2018: SAP explores a TypeScript language server and drops it, because it means two "
            "client codebases. 2018: the SAP BTP ABAP Environment launches with ADT for Eclipse only; adding many "
            "object types fast shows that editors written in two languages do not scale. 2020: number range "
            "objects are the first server-driven object type; all new types since are built that way. "
            "2 Toward VS Code. 2023 and 2025: user surveys name VS Code the most requested IDE. 2025: SAP announces "
            "work on ADT for VS Code. 2026: ADT for VS Code is due, "
            "after six years of rework.")

L, R, W = 24, 624, 552
CW, CH, STEP = 492, 96, 200


def column(x, cards):
    for i, (year, lbl, kind) in enumerate(cards):
        y = 150 + i * STEP
        d.card(x + 30, y, lbl, kind, w=CW, h=CH)
        d.pill(x + 30, y - 44, 120, 32, year, "front")
        if i:
            d.arrow(f"M{x + W / 2} {y - STEP + CH}V{y - 16}")


d.group(L, 16, W, 868, "The rework", 1)
column(L, [("2018", "TypeScript language server|tried, then dropped", None),
           ("2018", "BTP ABAP: Eclipse only|editors don't scale", None),
           ("2020", "Number range objects|first server-driven type", None)])
d.note(L + W / 2, 818, "all new object types are")
d.note(L + W / 2, 846, "server-driven since then")

d.group(R, 16, W, 868, "Toward VS Code", 2)
column(R, [("2023, 2025", "User surveys|VS Code most wanted", None),
           ("2025", "SAP announces work|on ADT for VS Code", None),
           ("2026", "ADT for VS Code|planned release", None)])
d.note(R + W / 2, 818, "six years of rework")
d.note(R + W / 2, 846, "made it possible")

d.arrow(f"M{L + W} 398H{R - 2}", label="then", at=(600, 386))

d.save(Path(__file__).with_name("timeline.svg"))
