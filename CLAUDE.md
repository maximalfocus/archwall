# archwall

Architecture-diagram site; see README.md for layout and build.
Writing or landing a post: use the `archwall` skill (`.claude/skills/archwall/`); it has the steps, this file has the rules.

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
- The figure is an SVG, redrawn (no raster screenshots), and appears both on the home page and in the post.
- Show the whole architecture, so a non-technical manager can follow it from the diagrams alone. There is no cap on
  how many diagrams a post has: start with an overview (the home-page card), then add one for each phase, part or
  concern that a diagram (the overview or any other) only names (data flow, safety rails, models, operations, ...),
  as many as it takes.
  List the extra ones under `[[figures]]` in `meta.toml` (file, alt, a caption saying in plain words what the
  diagram shows) and place each with a line `![](name.svg)` in both zh.md and en.md. The first diagram stays the home-page card.
  Each extra one follows the same rules below, with its source `<name>.py` next to `<name>.svg`.
- One look for every diagram, whatever the source figure looks like: draw it with `tools/archdiagram.py`
  (grey groups, lighter sub-groups, white cards with a coloured role bar, slate arrows, no icons).
  Keep the source as `posts/<slug>/diagram.py` next to the generated `diagram.svg`.
- Every diagram is 1200 x 900 (4:3), the same frame as the home-page cards. Wrap stages into two columns
  (snake order) rather than one long flat row, so it stays readable on a phone.
- Few words in the picture: card labels of two short lines, at most two note lines per group, labelled arrows
  for what flows. Details go in the post text. The tool's docstring has the type sizes; don't go below them.
- Numbers and claims must match the source; cite it in `source`.
- A feature that needs an extra, a flag or a config setting is labelled as such, in the text and the picture.
- Where docs disagree with each other or with the code about what the code does, settle it from the
  code when the code can answer; otherwise leave the claim out.
