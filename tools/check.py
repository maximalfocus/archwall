#!/usr/bin/env python3
"""Check a post for everything that can be checked without eyes.  macOS, needs Google Chrome.

    python3 tools/check.py posts/<slug>      # prints each failure; exit 0 = clean

- Length: the counts build.py enforces (en <= 300 words, zh <= 300 hanzi).
- Figures: meta figure is diagram.svg; every other SVG is listed under [[figures]] with alt_zh,
  caption_zh and caption_en; every SVG has its .py and a non-empty <title> and <desc>; each listed figure
  sits on its own line, once, in both bodies, in the same order. A post not in OLD must leave out alt_en
  (top level and figures): build.py derives it from the SVG, so the .py holds the only copy.
- Fresh: each committed SVG equals a new run of its .py (run outside the repo, so nothing here changes).
- Look: 1200 x 900, no raster, no type of its own, role bars in KIND colours; no em dash in the
  bodies, titles, captions or alt texts (derived ones included).
- Build: the whole site builds (build.main into a temp dir) with no error or warning. This one command
  is the /peerreview gate for a post.
- Layout, measured by Chrome with real fonts: text inside its card, pill, group or the frame; cards
  inside a group; no overlaps (a stack of offset copies of one card is fine); at most two lines per
  card and two notes per group or sub-group (legend labels, a note beside a card and the labels of a
  dashed boundary line do not count);
  no arrow crosses a card or runs through text (an arrow's own label may sit on it).
- Size: the skill (.claude/skills/archwall/SKILL.md) stays within 80 lines of at most 110 characters,
  CLAUDE.md within 40 lines of at most 130; over a cap, merge or delete before adding.

It does not judge whether a picture is right or readable: render it and look (tools/render.py).
"""
import contextlib
import html
import io
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import tomllib
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))
import archdiagram  # noqa: E402
import build  # noqa: E402

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
# Posts from before alt_en was derived (650dcb5); they keep their hand-written alt_en.
OLD = {"2026-10-03-dream-rsi", "2026-10-03-herdr", "2026-10-03-scientisttwo-pipeline", "2026-10-04-abap-adt",
       "2026-10-04-graphify", "2026-10-04-mcp", "2026-10-04-pi", "2026-10-05-grafana", "2026-10-05-idd-skills",
       "2026-10-05-peerreview-skills", "2026-10-05-vvah", "2026-10-06-open-connector", "2026-10-07-automic-vault"}
FIG = re.compile(r"(?m)^!\[[^\]]*\]\(([^)\s]+)\)$")

# Runs in the page Chrome renders: measures every text box and checks the boxes against each other.
LAYOUT_JS = r"""
(function () {
  const out = [], svg = document.querySelector('svg');
  const num = v => parseFloat(v || '0');
  const R = [...svg.querySelectorAll('rect')].filter(r => !r.closest('defs') && !r.closest('g')).map(r => ({
    cls: r.getAttribute('class') || '', x: num(r.getAttribute('x')), y: num(r.getAttribute('y')),
    w: num(r.getAttribute('width')), h: num(r.getAttribute('height')), rx: num(r.getAttribute('rx'))}));
  const cards = R.filter(r => ['agent', 'human', 'front'].includes(r.cls));
  const groups = R.filter(r => r.cls === 'grp'), subs = R.filter(r => r.cls === 'sub');
  const frame = {x: 0, y: 0, w: 1200, h: 900};
  const inside = (a, c) => a.x >= c.x - 0.5 && a.y >= c.y - 0.5 && a.x + a.w <= c.x + c.w + 0.5 && a.y + a.h <= c.y + c.h + 0.5;
  const pad = (c, px, py) => ({x: c.x + px, y: c.y + py, w: c.w - 2 * px, h: c.h - 2 * py});
  const hit = (a, b) => a.x < b.x + b.w && b.x < a.x + a.w && a.y < b.y + b.h && b.y < a.y + a.h;
  const holds = (c, x, y) => x >= c.x && x <= c.x + c.w && y >= c.y && y <= c.y + c.h;
  const smallest = (list, x, y) => list.filter(c => holds(c, x, y)).sort((a, b) => a.w * a.h - b.w * b.h)[0];
  const front = (x, y) => cards.filter(c => holds(c, x, y)).pop();  // drawn last = on top
  const stacked = (a, b) => a.w === b.w && a.h === b.h && Math.abs(a.x - b.x) <= 24 && a.x - b.x === a.y - b.y;
  const swatches = R.filter(r => !r.cls && r.w === 6 && r.h === 20);  // legend() colour keys
  const dividers = [...svg.querySelectorAll('path[stroke-dasharray]')].filter(p => !p.closest('g')).map(p => {
    const m = (p.getAttribute('d') || '').match(/^M\s*([\d.]+)[ ,]+([\d.]+)\s*H\s*([\d.]+)$/);
    return m && {x1: Math.min(+m[1], +m[3]), x2: Math.max(+m[1], +m[3]), y: +m[2]};
  }).filter(Boolean);  // dashed boundary lines; their labels are not notes
  const at = r => `${Math.round(r.x)},${Math.round(r.y)}`;
  const tight = b => ({x: b.x, y: b.y + 2, w: b.w, h: b.h - 4});
  const texts = [...svg.querySelectorAll('text')].filter(el => !el.closest('g')).map(el => {
    const b = el.getBBox();
    return {s: JSON.stringify(el.textContent), cls: el.getAttribute('class') || '', b: {x: b.x, y: b.y, w: b.width, h: b.height}};
  });
  for (const r of R.filter(r => r.cls)) if (!inside(r, frame)) out.push(`box at ${at(r)} leaves the frame`);
  for (const t of texts) if (!inside(t.b, frame)) out.push(`text leaves the frame: ${t.s}`);
  for (let i = 0; i < groups.length; i++) for (let j = i + 1; j < groups.length; j++)
    if (hit(groups[i], groups[j])) out.push(`groups at ${at(groups[i])} and ${at(groups[j])} overlap`);
  // A rounded pill (rx = h/2) sits outside the flow on purpose; every other card belongs in a group.
  for (const c of cards.filter(c => c.cls === 'agent' || c.rx < c.h / 2 - 0.5))
    if (!groups.some(g => inside(c, pad(g, 4, 4)))) out.push(`card at ${at(c)} is not inside a group`);
  for (let i = 0; i < cards.length; i++) for (let j = i + 1; j < cards.length; j++)
    if (hit(cards[i], cards[j]) && !stacked(cards[i], cards[j])) out.push(`cards at ${at(cards[i])} and ${at(cards[j])} overlap`);
  const lines = new Map();
  for (const t of texts) {
    const cx = t.b.x + t.b.w / 2, cy = t.b.y + t.b.h / 2;
    if (t.cls === 'ag') {
      const c = front(cx, cy);
      if (!c) { out.push(`card label outside any card: ${t.s}`); continue; }
      if (!inside(t.b, {x: c.x + 8, y: c.y + 2, w: c.w - 14, h: c.h - 4})) out.push(`card label overflows its card: ${t.s}`);
      lines.set(c, (lines.get(c) || 0) + 1);
    } else if (t.cls === 'q') {
      const c = front(cx, cy);
      if (!c || !inside(t.b, pad(c, 8, 2))) out.push(`pill text overflows: ${t.s}`);
    } else if (t.cls === 'gt' || t.cls === 'st') {
      const c = smallest(t.cls === 'gt' ? groups : subs, cx, cy);
      if (!c || !inside(t.b, pad(c, 8, 0))) out.push(`title overflows its box: ${t.s}`);
      for (const k of cards) if (hit(t.b, k)) out.push(`title covers a card: ${t.s}`);
    } else if (t.cls === 'lb') {
      const g = smallest(groups.concat(subs), cx, cy);
      if (!inside(t.b, g ? pad(g, 8, 0) : frame)) out.push(`note overflows: ${t.s}`);
      for (const k of cards) if (hit(t.b, k)) out.push(`note covers a card: ${t.s}`);
      const legend = g && swatches.some(w => t.b.x - (w.x + w.w) >= 0 && t.b.x - (w.x + w.w) <= 12 && cy >= w.y && cy <= w.y + w.h &&
        smallest(groups.concat(subs), w.x + w.w / 2, w.y + w.h / 2) === g);
      // A note beside a card is exempt only if that card is in the note's own group or sub-group
      // and the note is left or right of it, not under it.
      const beside = g && cards.some(k => cy >= k.y && cy <= k.y + k.h &&
        (t.b.x + t.b.w <= k.x || t.b.x >= k.x + k.w) &&
        smallest(groups.concat(subs), k.x + k.w / 2, k.y + k.h / 2) === g);
      // A dashed boundary's labels sit just above and below the line, in that line's own group.
      const boundary = g && dividers.some(v => cx >= v.x1 && cx <= v.x2 && Math.abs(cy - v.y) <= 30 &&
        smallest(groups.concat(subs), (v.x1 + v.x2) / 2, v.y) === g);
      if (g && !legend && !beside && !boundary) lines.set(g, (lines.get(g) || 0) + 1);
    } else if (t.cls === 'al') {
      for (const k of cards) if (hit(t.b, k)) out.push(`arrow label covers a card: ${t.s}`);
    }
  }
  for (const [c, n] of lines) if (n > 2) out.push(`${c.cls === 'grp' || c.cls === 'sub' ? 'group' : 'card'} at ${at(c)} has ${n} ${c.cls === 'grp' || c.cls === 'sub' ? 'notes' : 'lines'}, at most 2`);
  for (let i = 0; i < texts.length; i++) for (let j = i + 1; j < texts.length; j++) {
    const a = texts[i], b = texts[j];
    if (a.cls !== 'numt' && b.cls !== 'numt' && hit(tight(a.b), tight(b.b))) out.push(`texts overlap: ${a.s} / ${b.s}`);
  }
  const paths = [...svg.querySelectorAll('path')].filter(p => !p.closest('defs') && !p.closest('g') &&
    (/(^| )flow( |$)/.test(p.getAttribute('class') || '') || (!p.getAttribute('class') && p.getAttribute('stroke'))));
  for (const p of paths) {
    const d = p.getAttribute('d'), toks = d.match(/[A-Za-z]|-?\d*\.?\d+(?:e-?\d+)?/g) || [];
    let cmd = null, x = 0, y = 0;
    const pts = [];
    for (let i = 0; i < toks.length;) {
      if (/^[A-Za-z]$/.test(toks[i])) { cmd = toks[i++]; continue; }
      if (cmd === 'M' || cmd === 'L') { x = +toks[i++]; y = +toks[i++]; pts.push([x, y]); }
      else if (cmd === 'H') { x = +toks[i++]; pts.push([x, y]); }
      else if (cmd === 'V') { y = +toks[i++]; pts.push([x, y]); }
      else if (cmd === 'C') {
        const [x1, y1, x2, y2, x3, y3] = toks.slice(i, i + 6).map(Number); i += 6;
        for (let k = 1; k <= 16; k++) {
          const t = k / 16, u = 1 - t;
          pts.push([u*u*u*x + 3*u*u*t*x1 + 3*u*t*t*x2 + t*t*t*x3, u*u*u*y + 3*u*u*t*y1 + 3*u*t*t*y2 + t*t*t*y3]);
        }
        x = x3; y = y3;
      } else { out.push(`arrow ${d}: path command ${cmd} is not checked; use M, L, H, V or C`); break; }
    }
    for (let i = 1; i < pts.length; i++) {
      const [x1, y1] = pts[i - 1], [x2, y2] = pts[i];
      const seg = {x: Math.min(x1, x2) - 1, y: Math.min(y1, y2) - 1, w: Math.abs(x2 - x1) + 2, h: Math.abs(y2 - y1) + 2};
      for (const k of cards) if (hit(seg, pad(k, 1, 1))) out.push(`arrow ${d} crosses the card at ${at(k)}`);
      for (const t of texts) if (!['al', 'numt'].includes(t.cls) && hit(seg, tight(t.b))) out.push(`arrow ${d} runs through ${t.s}`);
    }
  }
  document.getElementById('out').textContent = JSON.stringify([...new Set(out)]);
})();
"""


def measure(svg, tmp):
    """Run LAYOUT_JS on one SVG in headless Chrome; returns its list of layout failures."""
    page = tmp / f"{svg.stem}.html"
    page.write_text("<!doctype html><meta charset=utf-8><body style='margin:0'>" + svg.read_text()
                    + "<pre id=out>PENDING</pre><script>" + LAYOUT_JS + "</script></body>")
    # A fresh profile keeps headless Chrome alive (its updater wakes up), so read the dumped DOM as
    # soon as it is complete, then end Chrome's whole process group.
    proc = subprocess.Popen([CHROME, "--headless=new", "--disable-gpu", "--no-first-run",
                             "--disable-component-update", f"--user-data-dir={tempfile.mkdtemp(dir=tmp)}",
                             "--dump-dom", page.as_uri()], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                            text=True, start_new_session=True)
    dom, deadline = "", time.monotonic() + 120
    try:
        while "</html>" not in dom and time.monotonic() < deadline:
            line = proc.stdout.readline()
            if not line:
                break
            dom += line
    finally:
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        proc.wait()
    m = re.search(r'<pre id="out">(.*?)</pre>', dom, re.S)
    if not m or m[1] == "PENDING":
        return ["Chrome returned no layout result"]
    return json.loads(html.unescape(m[1]))


def check(post):
    fails = []
    for name, max_lines, max_w in ((".claude/skills/archwall/SKILL.md", 80, 110), ("CLAUDE.md", 40, 130)):
        lines = (ROOT / name).read_text().splitlines()
        if len(lines) > max_lines:
            fails.append(f"{name} is {len(lines)} lines, over the cap {max_lines}: merge or delete before adding")
        for i, line in enumerate(lines, 1):
            if len(line) > max_w:
                fails.append(f"{name} line {i} is {len(line)} characters, over {max_w}")
    meta = tomllib.loads((post / "meta.toml").read_text())
    zh, en = (post / "zh.md").read_text(), (post / "en.md").read_text()

    words, hanzi = build.counts(en, zh)
    print(f"{post.name}: en {words} words, zh {hanzi} hanzi")
    if words > build.MAX_WORDS_EN or hanzi > build.MAX_HANZI_ZH:
        fails.append(f"too long: limit {build.MAX_WORDS_EN} words / {build.MAX_HANZI_ZH} hanzi")

    figs = meta.get("figures", [])
    listed = [f.get("file") for f in figs]
    svgs = sorted(p.name for p in post.glob("*.svg"))
    if meta.get("figure") != "diagram.svg":
        fails.append("meta figure must be diagram.svg, the home-page card")
    old = post.name in OLD
    for f in figs:
        for k in ("file", "alt_zh", "caption_zh", "caption_en") + (("alt_en",) if old else ()):
            if not str(f.get(k, "")).strip():
                fails.append(f"[[figures]] {f.get('file')}: no {k}")
    if not old:
        stray = (["meta"] if "alt_en" in meta else []) + [f"[[figures]] {f.get('file')}" for f in figs if "alt_en" in f]
        fails += [f"{w}: leave out alt_en, build.py takes it from the SVG <title> and <desc>" for w in stray]
    alt = {s: build.svg_alt(post / s) if (post / s).exists() else "" for s in svgs}
    for s, a in alt.items():
        if not a:
            fails.append(f"{s}: empty <title> or <desc>")
    if sorted(listed + ["diagram.svg"]) != svgs or len(set(listed)) != len(listed):
        fails.append(f"SVGs on disk {svgs} differ from diagram.svg plus [[figures]] {listed}")
    for s in svgs:
        if not (post / s).with_suffix(".py").exists():
            fails.append(f"{s}: no {Path(s).stem}.py next to it")
    placed = {n: FIG.findall(t) for n, t in (("en.md", en), ("zh.md", zh))}
    if placed["en.md"] != placed["zh.md"]:
        fails.append("en.md and zh.md place their figures differently")
    for n, got in placed.items():
        if sorted(got) != sorted(listed):
            fails.append(f"{n} places {got}, want each of {listed} once")

    for where, text in ([("en.md", en), ("zh.md", zh)]
                        + [(f"meta {k}", meta.get(k, "")) for k in ("title_zh", "title_en", "alt_zh", "alt_en")]
                        + [(f"{f.get('file')} {k}", f.get(k, "")) for f in figs
                           for k in ("alt_zh", "alt_en", "caption_zh", "caption_en")]
                        + [(f"{s} title/desc", a) for s, a in alt.items()]):
        if "—" in str(text):
            fails.append(f"{where}: em dash")

    kinds = set(archdiagram.KIND.values())
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        (tmp / "tools").mkdir()
        shutil.copy(ROOT / "tools" / "archdiagram.py", tmp / "tools")
        fresh = tmp / "posts" / post.name
        fresh.mkdir(parents=True)
        for py in post.glob("*.py"):
            shutil.copy(py, fresh / py.name)
        for py in sorted(fresh.glob("*.py")):
            r = subprocess.run([sys.executable, str(py)], cwd=fresh, capture_output=True, text=True)
            if r.returncode:
                fails.append(f"{py.name} fails: {r.stderr.strip().splitlines()[-1:]}")
        for s in svgs:
            raw = (post / s).read_text()
            new = fresh / s
            if new.exists() and new.read_text() != raw:
                fails.append(f"{s} is stale: run python3 {post.relative_to(ROOT)}/{Path(s).stem}.py")
            try:
                root = ET.fromstring(raw)
            except ET.ParseError as e:
                fails.append(f"{s}: not valid SVG ({e})")
                continue
            if (root.get("width"), root.get("height"), root.get("viewBox")) != ("1200", "900", "0 0 1200 900"):
                fails.append(f"{s}: not 1200 x 900")
            if "<image" in raw or "<foreignObject" in raw:
                fails.append(f"{s}: raster or embedded content")
            outside = re.sub(r"<style>.*?</style>", "", raw, flags=re.S)
            if re.search(r"font-size|font-family| style=", outside):
                fails.append(f"{s}: type of its own outside the house CSS")
            for fill in re.findall(r'<rect [^>]*width="[56]" [^>]*fill="(#[0-9a-fA-F]{6})"', raw):
                if fill not in kinds:
                    fails.append(f"{s}: role colour {fill} is not one of KIND")
            fails += [f"{s}: {v}" for v in measure(post / s, tmp)]
    fails += site_builds()
    return fails


def site_builds():
    """Run build.main into a temp dir, as GitHub Pages will; any error or warning, in any post, fails."""
    out, saved = io.StringIO(), build.OUT
    with tempfile.TemporaryDirectory() as t:
        build.OUT = Path(t) / "_site"
        try:
            with contextlib.redirect_stdout(out):
                build.main()
        except (Exception, SystemExit) as e:
            return [f"build fails: {e!r}"]
        finally:
            build.OUT = saved
    return [f"build: {line}" for line in out.getvalue().splitlines() if line.startswith(("warning", "error"))]


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    post = (Path.cwd() / sys.argv[1]).resolve()
    if not (post / "meta.toml").exists():
        sys.exit(f"no meta.toml in {post}")
    if not Path(CHROME).exists():
        sys.exit(f"Google Chrome not found at {CHROME}: the layout check needs it")
    fails = check(post)
    for f in fails:
        print("FAIL:", f)
    print("clean" if not fails else f"{len(fails)} failure(s)")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
