"""ADT object type editors before and after server-driven development (2020), redrawn from the
"server_driven_before_after" figure in SAP's post:
https://community.sap.com/t5/technology-blog-posts-by-sap/behind-the-design-how-we-transformed-the-abap-development-tools/ba-p/14258121
Run: python3 editors.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("ADT editors before and after 2020",
            "Before 2020 every object type had its own editor: the UI in Java on the client, the persistence "
            "in ABAP on the server; the SAP BTP ABAP environment alone needs 88 editors as of 2025. "
            "Today all new object types are server-driven: number range objects were the first, in 2020. "
            "The server describes the UI in ABAP and the client has two renderers, one for form-based and "
            "one for source-based objects. A new IDE needs two editors, not 88.")

LINE = 400


def split(x, w):
    d.raw(f'<path d="M{x + 16} {LINE}H{x + w - 16}" stroke="#5b6675" stroke-width="2" stroke-dasharray="9 7"/>')
    d.text(x + 24, LINE - 14, "Client", "lb", "start")
    d.text(x + 24, LINE + 30, "Server", "lb", "start")


def stack(x, y, label, w, h):
    for k in (2, 1):
        d.rect(x + k * 10, y + k * 10, w, h, "agent", 8)
    d.card(x, y, label, "write", w=w, h=h)


# before
d.group(24, 16, 564, 868, "Before 2020: one editor each")
split(24, 564)
for i, n in enumerate(["1", "2", "n"]):
    x = 52 + i * 180
    d.card(x, 180, f"Editor {n}|Java UI", "coding", w=150, h=80)
    d.card(x, 540, f"Object|type {n}", "write", w=150, h=80)
    d.arrow(f"M{x + 77} 260V536")
d.note(306, 740, "88 editors on BTP ABAP (2025)")
d.note(306, 768, "doesn't scale")

# after
d.group(612, 16, 564, 868, "Today: server-driven")
split(612, 564)
for i, (r, o) in enumerate([("Form-based|renderer", "All form-based|object types"),
                            ("Source-based|renderer", "All source-based|object types")]):
    x = 652 + i * 256
    d.card(x, 180, r, "coding", w=220, h=80)
    stack(x, 540, o, 220, 80)
    d.arrow(f"M{x + 113} 260V536")
d.note(894, 740, "first one: number range objects")
d.note(894, 768, "a new IDE needs 2 editors, not 88")

d.save(Path(__file__).with_name("editors.svg"))
