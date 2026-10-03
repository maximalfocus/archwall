#!/usr/bin/env python3
"""Build the static site into _site/.  Stdlib only (Python 3.11+).

    python3 build.py            # build
    python3 build.py --serve    # build, then serve on http://localhost:8000

Each post is a folder posts/<YYYY-MM-DD-slug>/ with:
    meta.toml   title_zh, title_en, date, tags, figure, alt_zh, alt_en, [source]
    zh.md       Chinese body (small Markdown subset)
    en.md       English body
    <figure>    the vector diagram shown on the home page and in the article
All URLs are relative, so the site works under any GitHub Pages path.
"""
import html
import json
import math
import re
import shutil
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "_site"
PER_PAGE = 50
SITE = tomllib.loads((ROOT / "site.toml").read_text())
MAX_WORDS_EN, MAX_HANZI_ZH = 300, 300

esc = html.escape


def inline(s):
    s = esc(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", s)
    return re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', s)


def markdown(text):
    """Paragraphs, ## headings, - / 1. lists, **bold**, *italic*, `code`, [links](url)."""
    out = []
    for block in re.split(r"\n\s*\n", text.strip()):
        lines = block.splitlines()
        if m := re.match(r"(#{2,4})\s+(.*)", lines[0]):
            out.append(f"<h{len(m[1])}>{inline(m[2])}</h{len(m[1])}>")
        elif all(re.match(r"\s*[-*]\s", ln) for ln in lines):
            out.append("<ul>" + "".join(f"<li>{inline(re.sub(r'^\s*[-*]\s', '', ln))}</li>" for ln in lines) + "</ul>")
        elif all(re.match(r"\s*\d+\.\s", ln) for ln in lines):
            out.append("<ol>" + "".join(f"<li>{inline(re.sub(r'^\s*\d+\.\s', '', ln))}</li>" for ln in lines) + "</ol>")
        else:
            out.append(f"<p>{inline(' '.join(ln.strip() for ln in lines))}</p>")
    return "\n".join(out)


def bi(zh, en, tag="span"):
    return (f'<{tag} class="i18n-zh" lang="zh-CN">{zh}</{tag}>'
            f'<{tag} class="i18n-en" lang="en">{en}</{tag}>')


def page(title_zh, title_en, body, root, desc=""):
    return f"""<!doctype html>
<html lang="zh-CN" data-lang="zh" data-title-zh="{esc(title_zh)}" data-title-en="{esc(title_en)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title_zh)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="icon" href="{root}static/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{root}static/style.css">
<script>try{{var q=new URLSearchParams(location.search).get('lang'),l=q==='en'||q==='zh'?q:localStorage.getItem('dl-lang');if(l==='en')document.documentElement.setAttribute('data-lang','en')}}catch(e){{}}</script>
</head>
<body>
<header class="top"><a class="brand" href="{root}">{esc(SITE['title'])}</a>
<span class="tag">{bi(esc(SITE['tagline_zh']), esc(SITE['tagline_en']))}</span></header>
<main>
{body}
</main>
<button id="lang-toggle" type="button" aria-label="中文 / English">EN</button>
<script src="{root}static/site.js" defer></script>
</body>
</html>
"""


def load_posts():
    posts = []
    for d in sorted((ROOT / "posts").glob("*/"), reverse=True):
        if not (d / "meta.toml").exists():
            continue
        meta = tomllib.loads((d / "meta.toml").read_text())
        zh, en = (d / "zh.md").read_text(), (d / "en.md").read_text()
        words = len(re.findall(r"[A-Za-z0-9][\w'’.-]*", en))
        hanzi = len(re.findall(r"[一-鿿]", zh))
        if words > MAX_WORDS_EN or hanzi > MAX_HANZI_ZH:
            print(f"warning: {d.name} is long (en {words} words, zh {hanzi} hanzi; limit {MAX_WORDS_EN}/{MAX_HANZI_ZH})")
        if not (d / meta["figure"]).exists():
            sys.exit(f"error: {d.name}: figure {meta['figure']} missing")
        posts.append({**meta, "slug": d.name, "dir": d, "zh": zh, "en": en})
    posts.sort(key=lambda p: (p["date"], p["slug"]), reverse=True)
    return posts


def card(p, root):
    href = f"{root}p/{p['slug']}/"
    img = f"{root}p/{p['slug']}/{p['figure']}"
    return (f'<a class="card" href="{href}"><figure><img src="{img}" alt="{esc(p["alt_en"])}" '
            f'data-alt-zh="{esc(p["alt_zh"])}" data-alt-en="{esc(p["alt_en"])}" loading="lazy" decoding="async"></figure>'
            f'<div class="cap">{bi(esc(p["title_zh"]), esc(p["title_en"]))}<time>{p["date"]}</time></div></a>')


def pager(n, total, root):
    if total <= 1:
        return ""
    link = lambda i: root if i == 1 else f"{root}page/{i}/"
    prev = f'<a href="{link(n - 1)}">{bi("← 上一页", "← Newer")}</a>' if n > 1 else "<span></span>"
    nxt = f'<a href="{link(n + 1)}">{bi("下一页 →", "Older →")}</a>' if n < total else "<span></span>"
    return f'<nav class="pager">{prev}<span>{n} / {total}</span>{nxt}</nav>'


def build_index(posts):
    pages = max(1, math.ceil(len(posts) / PER_PAGE))
    for n in range(1, pages + 1):
        root = "./" if n == 1 else "../../"
        chunk = posts[(n - 1) * PER_PAGE:n * PER_PAGE]
        search = (f'<div class="search"><input id="q" type="search" autocomplete="off" '
                  f'data-ph-zh="搜索架构…" data-ph-en="Search architectures…" placeholder="搜索架构…" '
                  f'data-index="{root}search.json" data-root="{root}"></div>')
        body = (f'{search}<p id="hits" class="hits" hidden></p>'
                f'<section id="grid" class="grid">{"".join(card(p, root) for p in chunk)}</section>'
                f'{pager(n, pages, root)}')
        dest = OUT / ("index.html" if n == 1 else f"page/{n}/index.html")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(page(SITE["title"], SITE["title"], body, root, SITE["tagline_en"]))


def build_post(p):
    root = "../../"
    dest = OUT / "p" / p["slug"]
    shutil.copytree(p["dir"], dest, ignore=shutil.ignore_patterns("*.md", "*.toml", "*.py", "__pycache__"))
    fig = (f'<figure class="hero"><a href="{p["figure"]}" title="Open full size">'
           f'<img src="{p["figure"]}" alt="{esc(p["alt_en"])}" data-alt-zh="{esc(p["alt_zh"])}" '
           f'data-alt-en="{esc(p["alt_en"])}"></a></figure>')
    tags = "".join(f'<a class="chip" href="{root}?q={esc(t)}">{esc(t)}</a>' for t in p.get("tags", []))
    src = (f'<p class="src">{bi("来源", "Source")}: <a href="{esc(p["source"])}">{esc(p["source"].split("/")[2])}</a></p>'
           if p.get("source") else "")
    body = (f'<article><h1>{bi(esc(p["title_zh"]), esc(p["title_en"]))}</h1>'
            f'<p class="meta"><time>{p["date"]}</time>{tags}</p>{fig}'
            f'<div class="i18n-zh" lang="zh-CN">{markdown(p["zh"])}</div>'
            f'<div class="i18n-en" lang="en">{markdown(p["en"])}</div>{src}'
            f'<p class="back"><a href="{root}">{bi("← 全部架构", "← All architectures")}</a></p></article>')
    desc = re.sub(r"[*`#\[\]]", "", p["en"]).split("\n")[0][:160]
    (dest / "index.html").write_text(page(p["title_zh"], p["title_en"], body, root, desc))


def plain(md):
    return re.sub(r"\s+", " ", re.sub(r"[*`#]|\]\([^)]*\)|\[", "", md)).strip()


def main():
    shutil.rmtree(OUT, ignore_errors=True)
    OUT.mkdir()
    shutil.copytree(ROOT / "static", OUT / "static")
    (OUT / ".nojekyll").write_text("")
    posts = load_posts()
    for p in posts:
        build_post(p)
    build_index(posts)
    index = [{"s": p["slug"], "f": p["figure"], "d": p["date"], "tz": p["title_zh"], "te": p["title_en"],
              "az": p["alt_zh"], "ae": p["alt_en"], "t": p.get("tags", []),
              "x": (plain(p["zh"]) + " " + plain(p["en"])).lower()} for p in posts]
    (OUT / "search.json").write_text(json.dumps(index, ensure_ascii=False, separators=(",", ":")))
    print(f"built {len(posts)} posts, {max(1, math.ceil(len(posts) / PER_PAGE))} index page(s) -> {OUT}")
    if "--serve" in sys.argv:
        import functools, http.server
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=OUT)
        print("serving http://localhost:8000")
        http.server.ThreadingHTTPServer(("", 8000), handler).serve_forever()


if __name__ == "__main__":
    main()
