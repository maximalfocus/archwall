# archwall

Architecture-diagram site; see README.md for layout and build.

## Post workflow (always)

- Every new post (or substantive rewrite) goes on its own branch `post/<slug>` cut from `main`; commit freely there.
- Push the branch and open a PR; the owner reviews and asks for revisions. Never merge without the owner's explicit go-ahead.
- On approval: squash merge (`gh pr merge --squash --delete-branch`), so each post is one commit on `main`, then pull `main`.
- Site/tooling changes that are not a post follow the same branch → PR → squash flow (branch `site/<topic>`).

## Post rules

- Body ≤ 300 words (en) / 300 hanzi (zh), both languages, same content.
- Voice, everywhere from the home page to the post: short, plain, down-to-earth. Say it the way you'd explain it to a colleague.
  No AI filler: no "it's worth noting", no stacked adjectives, no em-dash asides, no summary that repeats the body.
  Short sentences, everyday words; keep only jargon the diagram itself uses.
- The figure is an SVG, hand-made or redrawn (no raster screenshots), and appears both on the home page and in the post.
- Numbers and claims must match the source; cite it in `source`.
