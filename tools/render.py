#!/usr/bin/env python3
"""Render a post to PNGs so you can look at it before anyone else does.  macOS, needs Google Chrome.

    python3 tools/render.py posts/<slug>     # every SVG in the post + the built page at phone width

Writes _render/<slug>/<name>.png (1200 x 900, one per SVG) and _render/<slug>/phone.png (the post
page at 390 px wide, from _site, so run build.py first). Look at every PNG: text inside its card or
group, nothing overlapping, arrows not running through words, readable on the phone shot.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def shot(url, out, w, h):
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={w},{h}",
                    f"--screenshot={out}", url], check=True, capture_output=True)


def main():
    post = (ROOT / sys.argv[1]).resolve() if len(sys.argv) > 1 else sys.exit(__doc__)
    out = ROOT / "_render" / post.name
    out.mkdir(parents=True, exist_ok=True)
    for svg in sorted(post.glob("*.svg")):
        shot(svg.as_uri(), out / f"{svg.stem}.png", 1200, 900)
        print(out / f"{svg.stem}.png")
    page = ROOT / "_site" / "p" / post.name / "index.html"
    if not page.exists():
        sys.exit(f"no {page.relative_to(ROOT)}: run python3 build.py first")
    # Headless Chrome won't make a window narrower than ~500 px, so frame the page at phone width.
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(f'<body style="margin:0"><iframe src="{page.as_uri()}" style="width:390px;height:3000px;border:0">')
    shot(Path(f.name).as_uri(), out / "phone.png", 390, 3000)
    Path(f.name).unlink()
    print(out / "phone.png")


if __name__ == "__main__":
    main()
