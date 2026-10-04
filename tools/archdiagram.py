"""archwall house style for architecture diagrams.

Every post's diagram.svg is drawn with these primitives so the home page reads as one wall:
grey rounded groups, lighter sub-groups, white cards with a coloured left bar, slate arrows,
system sans-serif text, white background. No icons or clip-art.

Every diagram is W x H = 1200 x 900 (4:3), so cards on the home page line up and a phone
screen gets a tall enough picture. Lay stages out in two columns and wrap (snake) instead of
stretching them into one long row.

Phones show the 1200-wide frame at about a third of its size, so type is big and words are few:
- Card labels 20px, notes 17px, nothing smaller. A card label fits in two short lines.
- At most two note lines per group. Anything longer belongs in the post text, not the picture.
- Name what an arrow carries with arrow(..., label=..., at=(x, y)) instead of a note beside it.
- KIND colours mean the card's role (below). If colour encodes anything else in a diagram,
  for example "active branch", add a legend() for it.

    from archdiagram import Diagram
    d = Diagram("Title", "One-paragraph description for screen readers.")
    d.group(24, 16, 552, 300, "Group")
    d.card(48, 96, "Coding|Agent", "coding")    # "|" breaks lines
    d.arrow("M212 126H236", label="calls", at=(224, 116))
    d.save("diagram.svg")
"""

# Card accent colours, by role.  Keep the meaning stable across posts.
KIND = {
    "coding": "#2f6fd6",  # does the work: coding / execution agents
    "critic": "#e8973a",  # judges: critics, evaluators, scorers
    "plan": "#2f9e6e",    # plans or decides: policies, planners
    "write": "#8a5cc7",   # produces artefacts: writers, data stores
    "review": "#d64545",  # reviews / gates
    "data": "#5b6675",    # passive data: logs, trees, histories
}

CSS = """
text{font-family:-apple-system,"Helvetica Neue",Arial,"PingFang SC",sans-serif;fill:#1f2a37}
.gt{font-size:26px;font-weight:700}
.st{font-size:20px;font-weight:700}
.ag{font-size:20px}
.q{font-size:18px;fill:#3d4a5c}
.lb{font-size:17px;fill:#4a5565}
.al{font-size:16px;font-weight:600;fill:#3d4a5c;paint-order:stroke;stroke:#ffffff;stroke-width:6px;stroke-linejoin:round}
.grp{fill:#f2f5f9;stroke:#9aa4b2;stroke-width:1.6}
.sub{fill:#e8edf3;stroke:#b8c1cc;stroke-width:1.2}
.agent{fill:#ffffff;stroke:#b8c1cc;stroke-width:1.2}
.human{fill:#d6e6fb;stroke:#9cbbe6;stroke-width:1.2}
.front{fill:#dcf0e0;stroke:#9ccfa8;stroke-width:1.2}
.flow{stroke:#5b6675;stroke-width:2;fill:none;marker-end:url(#arr)}
.back{stroke-dasharray:7 5}
.cyc{stroke:#5b6675;stroke-width:2;fill:none;marker-end:url(#ca)}
.num{fill:#1f2a37}
.numt{font-size:16px;font-weight:700;fill:#ffffff}
"""


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


W, H = 1200, 900


class Diagram:
    def __init__(self, title, desc):
        self.w, self.h, self.title, self.desc, self.o = W, H, title, desc, []

    def raw(self, s):
        self.o.append(s)

    def text(self, x, y, s, cls="", anchor="middle", extra=""):
        self.raw(f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}" {extra}>{esc(s)}</text>')

    def rect(self, x, y, w, h, cls, rx=10):
        self.raw(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" class="{cls}"/>')

    def arrow(self, d, back=False, label=None, at=None):
        """Path d with an arrowhead; back dashes it. label is drawn at `at` with a white halo."""
        self.raw(f'<path d="{d}" class="flow{" back" if back else ""}"/>')
        if label:
            self.text(at[0], at[1], label, "al")

    def group(self, x, y, w, h, title, n=None):
        """Top-level stage. n puts a numbered dot before the title."""
        self.rect(x, y, w, h, "grp", 12)
        if n is None:
            self.text(x + w / 2, y + 36, title, "gt")
        else:
            tw = len(title) * 13.5
            cx = x + w / 2 - tw / 2 - 10
            self.number(cx, y + 27, n)
            self.text(cx + 20, y + 36, title, "gt", "start")

    def sub(self, x, y, w, h, title):
        self.rect(x, y, w, h, "sub", 9)
        self.text(x + w / 2, y + 28, title, "st")

    def card(self, x, y, label, kind=None, w=180, h=64, cls="agent"):
        """White card; '|' splits lines. kind picks the coloured left bar (see KIND)."""
        self.rect(x, y, w, h, cls, 8)
        if kind:
            self.raw(f'<rect x="{x}" y="{y + 10}" width="5" height="{h - 20}" rx="2" fill="{KIND[kind]}"/>')
        lines = label.split("|")
        y0 = y + h / 2 - (len(lines) - 1) * 12 + 7
        for i, ln in enumerate(lines):
            self.text(x + w / 2 + 3, y0 + i * 24, ln, "ag")

    def note(self, x, y, s, anchor="middle"):
        self.text(x, y, s, "lb", anchor)

    def legend(self, x, y, kinds, labels=None):
        """Row of role colours, e.g. legend(x, y, ["coding", "critic"]). labels overrides the names."""
        cx = x
        for k, lbl in zip(kinds, labels or kinds):
            self.raw(f'<rect x="{cx}" y="{y - 14}" width="6" height="20" rx="2" fill="{KIND[k]}"/>')
            self.text(cx + 14, y + 2, lbl, "lb", "start")
            cx += 14 + len(lbl) * 9 + 28

    def pill(self, x, y, w, h, label, cls="human"):
        """Rounded input/output box outside the main flow (the human ask, the final output)."""
        self.rect(x, y, w, h, cls, h / 2)
        self.text(x + w / 2, y + h / 2 + 6, label, "q")

    def number(self, x, y, n):
        self.raw(f'<circle cx="{x}" cy="{y}" r="14" class="num"/>')
        self.text(x, y + 6, str(n), "numt")

    def cycle(self, x, y, r=8):
        self.raw(f'<path d="M{x - r} {y} A{r} {r} 0 0 1 {x + r * 0.7} {y - r * 0.7}" class="cyc"/>')
        self.raw(f'<path d="M{x + r} {y} A{r} {r} 0 0 1 {x - r * 0.7} {y + r * 0.7}" class="cyc"/>')

    def ok(self, x, y):
        self.raw(f'<g transform="translate({x} {y})"><rect x="-9" y="-9" width="18" height="18" rx="4" fill="#2f9e6e"/>'
                 '<path d="M-5 0l3.5 4 6.5-8" stroke="#fff" stroke-width="2.4" fill="none"/></g>')

    def bad(self, x, y):
        self.raw(f'<g transform="translate({x} {y})"><rect x="-9" y="-9" width="18" height="18" rx="4" fill="#d64545"/>'
                 '<path d="M-4.5-4.5l9 9M4.5-4.5l-9 9" stroke="#fff" stroke-width="2.4"/></g>')

    def bulb(self, x, y):
        self.raw(f'<g transform="translate({x} {y})"><circle r="8" fill="#ffd54a" stroke="#b8860b" stroke-width="1.5"/>'
                 '<rect x="-4" y="7" width="8" height="5" rx="1" fill="#8c96a3"/></g>')

    def svg(self):
        w, h = self.w, self.h
        return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-labelledby="t d">
<title id="t">{esc(self.title)}</title>
<desc id="d">{esc(self.desc)}</desc>
<defs>
<marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="#5b6675"/></marker>
<marker id="ca" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="#5b6675"/></marker>
</defs>
<style>{CSS}</style>
<rect width="{w}" height="{h}" rx="18" fill="#ffffff"/>
{chr(10).join(self.o)}
</svg>
'''

    def save(self, path):
        with open(path, "w") as f:
            f.write(self.svg())
