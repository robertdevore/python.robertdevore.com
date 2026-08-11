# Changes

- Corrected three malformed links on `/about/`.
- Changed the global brand link from the duplicate `/index.html` route to `/`.
- Generated 24 exact legacy-route fallbacks: `/blog/`, 20 `/blog/<lesson>/` routes, and `/page/2-4/` to their `/course/` equivalents.
- Added release-contract tests for canonical routes, legacy redirects, and clean home links.
- Replaced 12 truncated lesson descriptions with complete factual summaries.
- Updated Python installation/version guidance and removed global `sudo pip` advice.
- Replaced deprecated naive UTC examples with timezone-aware `datetime.now(UTC)` examples.
- Added truthful `last_updated: 2026-08-10` metadata only to the two materially refreshed lessons.
- Preserved the public crawler-training policy; no DNS, WAF, analytics, or search-platform settings were changed.
- Deployed through GitHub Pages run `31451814639` and verified 26 canonical routes, 24 legacy mappings, and five discovery assets in production.
