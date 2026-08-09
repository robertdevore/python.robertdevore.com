# Python Course contributor guide

This repository is the source for `python.robertdevore.com`. It is built with Kujo SSG and the vendored SiteKit distribution.

## Canonical surfaces

- `content/`: course lessons and site pages in Markdown.
- `templates/`: semantic Kujo SSG templates.
- `assets/css/style.css`: Python Course theme built on SiteKit tokens.
- `assets/sitekit/`: vendored, unmodified SiteKit consumer distribution.
- `assets/js/docs.js`: mobile navigation, local search, and code-copy behavior.
- `build.kujo`: vendored Kujo SSG entrypoint.

## Rules

- Preserve the existing public lesson URLs under `/course/`.
- Keep the curriculum order, previous/next links, and course navigation synchronized.
- Keep SiteKit's `fonts/` directory beside `sitekit.css`; Departure Mono is served locally.
- Use semantic HTML, visible focus, accessible controls, and reduced-motion-safe behavior.
- Do not hand-edit `output/` or `assets/js/docs-search-index.json`.

## Validation

```bash
bash scripts/test-site.sh
```

