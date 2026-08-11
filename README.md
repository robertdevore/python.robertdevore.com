# Python Course

The source for [python.robertdevore.com](https://python.robertdevore.com): a complete Python development course that progresses from first setup to professional packaging and distribution.

The site is built with [Kujo SSG](https://github.com/kujolang/ssg) and styled with the vendored [SiteKit](https://github.com/kujolang/site-kit) distribution. Course content lives in Markdown, the site is fully static, and all search assets are generated locally.

## Build locally

Install the `kujo` CLI, then run:

```bash
./scripts/build.sh
kujo serve output --port 4178
```

Open <http://127.0.0.1:4178>.

## Edit the site

| Change | Location |
| --- | --- |
| Course lessons | `content/posts/` |
| About and utility pages | `content/pages/` |
| Site title, URL, sorting | `kujo-ssg.yml` |
| Page structure | `templates/` |
| Python color theme | `assets/css/style.css` |
| Search and menu behavior | `assets/js/docs.js` |

Generated files go under `output/`; do not edit them by hand.

## Social images

Every public route has a page-specific 1200×630 social card in `assets/images/social/`. The card source of truth is `howl.json`; SVGs are rendered by [Howl](https://github.com/kujolang/howl), then converted to PNG for Open Graph and Twitter metadata.

```bash
HOWL_BIN=/path/to/howl/bin/howl ./scripts/render-social-images.sh
```

Set `KUJO` as well when the Howl launcher cannot find the Kujo interpreter. Cards intentionally omit the lower-left URL so social platforms can use that overlay area.

## Verify

```bash
bash scripts/test-site.sh
```

The test builds the production site, validates generated HTML, checks representative routes and assets, and verifies the complete curriculum manifest.

The build script uses Kujo SSG's deterministic parallel build phases automatically, keeping the full 40,000-word course quick to regenerate while producing the same static output contract.
