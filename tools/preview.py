#!/usr/bin/env python3
"""Branch previews for archwall: every branch gets its own built site, kept up to date by git hooks.

    python3 tools/preview.py install   # once: hooks + always-on server (LaunchAgent) on :8765
    python3 tools/preview.py build     # build the checkout you are in (the hooks do this for you)
    python3 tools/preview.py serve     # what the LaunchAgent runs

A build copies the checkout's files (tracked and new, not ignored) to a temp dir, runs build.py
there and moves _site to $ARCHWALL_PREVIEW/<branch>/, so the checkout's own _site is untouched.
Branch post/pi is served at http://<host>:8765/post-pi/ and a post at .../post-pi/p/<slug>/.
The root page lists every branch with the diagrams of the posts it changes. Previews of deleted branches are removed.

install copies this script to $ARCHWALL_PREVIEW/.tool/ and points the hooks there, so the hooks
work in every worktree and on every branch, including ones cut before this script existed.
"""
import functools
import html
import http.server
import os
import plistlib
import shutil
import subprocess
import sys
import tempfile
import time
import tomllib
from pathlib import Path

PREVIEW = Path(os.environ.get("ARCHWALL_PREVIEW", Path.home() / "personal" / "archwall-preview"))
PORT = int(os.environ.get("ARCHWALL_PREVIEW_PORT", "8765"))
LABEL = "com.focus.archwall-preview"
HOOKS = ("post-commit", "post-checkout", "post-merge", "post-rewrite")


def git(*args, cwd=None):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=True).stdout.strip()


def slug(branch):
    return branch.replace("/", "-")


def build():
    top = Path(git("rev-parse", "--show-toplevel"))
    branch = git("branch", "--show-current", cwd=top)
    if not branch or not (top / "build.py").exists():
        return  # detached HEAD (mid-rebase) or not an archwall checkout
    PREVIEW.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=PREVIEW, prefix=".tmp-") as tmp:
        src = Path(tmp) / "src"
        for f in git("ls-files", "-co", "--exclude-standard", cwd=top).splitlines():
            if (top / f).is_file():
                (src / f).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(top / f, src / f)
        subprocess.run([sys.executable, "build.py"], cwd=src, check=True, capture_output=True)
        dest, old = PREVIEW / slug(branch), Path(tmp) / "old"
        if dest.exists():
            dest.rename(old)
        (src / "_site").rename(dest)  # swap, so a reader never sees a half-built site
    prune(top)
    index(top)
    print(f"preview: http://localhost:{PORT}/{slug(branch)}/")


def prune(top):
    live = {slug(b) for b in git("for-each-ref", "--format=%(refname:short)", "refs/heads", cwd=top).splitlines()}
    for d in PREVIEW.iterdir():
        if d.is_dir() and not d.name.startswith(".") and d.name not in live:
            shutil.rmtree(d, ignore_errors=True)


def changed_posts(top, branch):
    """Posts this branch adds or changes compared with main, newest first, with their diagram files."""
    try:
        names = git("diff", "--name-only", "main..." + branch, "--", "posts", cwd=top).splitlines()
    except subprocess.CalledProcessError:
        return []
    out = []
    for post in sorted({n.split("/")[1] for n in names if n.count("/") >= 2}, reverse=True):
        try:
            meta = tomllib.loads(git("show", f"{branch}:posts/{post}/meta.toml", cwd=top))
        except subprocess.CalledProcessError:
            continue  # post deleted on this branch
        out.append((post, meta.get("title_zh", post), [meta["figure"]] + [f["file"] for f in meta.get("figures", [])]))
    return out


def index(top):
    branches = git("for-each-ref", "--format=%(refname:short)", "refs/heads", cwd=top).splitlines()
    rows = []
    for d in sorted((d for d in PREVIEW.iterdir() if d.is_dir() and not d.name.startswith(".")),
                    key=lambda d: d.stat().st_mtime, reverse=True):
        branch = next((b for b in branches if slug(b) == d.name), d.name)
        last = git("log", "-1", "--format=%h %s", branch, cwd=top)
        when = time.strftime("%m-%d %H:%M", time.localtime(d.stat().st_mtime))
        posts = changed_posts(top, branch)
        figs = "".join(
            f'<div class="post"><a href="{d.name}/p/{post}/"><b>{html.escape(title)}</b></a><div class="figs">'
            + "".join(f'<a href="{d.name}/p/{post}/"><img src="{d.name}/p/{post}/{html.escape(f)}" loading="lazy"></a>'
                      for f in files)
            + "</div></div>" for post, title, files in posts) or '<p class="none">no post changes vs main</p>'
        rows.append(f'<section><h2><a href="{d.name}/">{html.escape(branch)}</a></h2>'
                    f'<p class="meta">built {when} · {html.escape(last)} · <a href="{d.name}/">whole site →</a></p>'
                    f'{figs}</section>')
    (PREVIEW / "index.html").write_text(
        '<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>archwall previews</title><style>'
        'body{font:16px/1.6 -apple-system,"PingFang SC",sans-serif;margin:24px 16px;max-width:1200px;background:#fbfbfa;color:#1f2a37}'
        'a{color:#2f6fd6;text-decoration:none}h2{margin:28px 0 0;font-size:20px}.meta,.none{color:#667085;font-size:14px;margin:2px 0 10px}'
        '.post{margin:0 0 16px}.figs{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px;margin-top:6px}'
        '.figs img{width:100%;aspect-ratio:4/3;background:#fff;border:1px solid #e4e7ec;border-radius:10px}'
        f'</style><h1>archwall previews</h1>{"".join(rows)}')


def install():
    top = Path(git("rev-parse", "--show-toplevel"))
    tool = PREVIEW / ".tool" / "preview.py"
    tool.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(__file__, tool)
    hooks = Path(git("rev-parse", "--git-common-dir", cwd=top)).resolve() / "hooks"
    for h in HOOKS:
        p = hooks / h
        if p.exists() and "archwall preview" not in p.read_text():
            sys.exit(f"error: {p} exists and is not ours; merge it by hand")
        p.write_text(f'#!/bin/sh\n# archwall preview: rebuild this branch\'s preview in the background\n'
                     f'"{sys.executable}" "{tool}" build >"{PREVIEW}/.build.log" 2>&1 &\n')
        p.chmod(0o755)
    plist = Path.home() / "Library" / "LaunchAgents" / f"{LABEL}.plist"
    plist.write_bytes(plistlib.dumps({
        "Label": LABEL, "ProgramArguments": [sys.executable, str(tool), "serve"],
        "RunAtLoad": True, "KeepAlive": True,
        "StandardOutPath": str(PREVIEW / ".serve.log"), "StandardErrorPath": str(PREVIEW / ".serve.log")}))
    uid = os.getuid()
    subprocess.run(["launchctl", "bootout", f"gui/{uid}/{LABEL}"], capture_output=True)
    subprocess.run(["launchctl", "bootstrap", f"gui/{uid}", str(plist)], check=True)
    print(f"hooks in {hooks}, server {LABEL} on :{PORT}, previews in {PREVIEW}")


def serve():
    PREVIEW.mkdir(parents=True, exist_ok=True)
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=PREVIEW)
    http.server.ThreadingHTTPServer(("", PORT), handler).serve_forever()


if __name__ == "__main__":
    {"build": build, "install": install, "serve": serve}[sys.argv[1] if len(sys.argv) > 1 else "build"]()
