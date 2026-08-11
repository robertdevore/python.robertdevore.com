# Changes

- Corrected three malformed links on `/about/`.
- Changed the global brand link from the duplicate `/index.html` route to `/`.
- Initially generated 24 exact legacy-route fallbacks, then replaced them with an active Cloudflare Bulk Redirect Rule containing 24 exact 301 mappings with query-string preservation.
- Removed the static meta-refresh artifacts after all 24 edge redirects passed production verification.
- Added release-contract tests for canonical routes, absence of retired generated routes, edge redirects, query preservation, and clean home links.
- Replaced 12 truncated lesson descriptions with complete factual summaries.
- Updated Python installation/version guidance and removed global `sudo pip` advice.
- Replaced deprecated naive UTC examples with timezone-aware `datetime.now(UTC)` examples.
- Added truthful `last_updated: 2026-08-10` metadata only to the two materially refreshed lessons.
- Preserved the public crawler-training policy; no DNS, WAF, analytics, or search-platform settings were changed.
- Deployed the content remediation through GitHub Pages runs `31451814639` and `31452140745`.
- Deployed Cloudflare Bulk Redirect List `4ecb2aecd75a48aeb27a4bd575b0198b` through active rule `1a0ee52fa1654bd7ae652f5987e89cea`, then verified 26 canonical routes, 24 exact 301 mappings, query preservation, and five discovery assets in production.
