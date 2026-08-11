# Methodology

Audit date: 2026-08-10 (America/Detroit). Production receipts may show 2026-08-11 UTC.

The audit mapped `Markdown and templates → Kujo SSG build → generated output → GitHub Pages origin → Cloudflare edge → crawler/browser`. The untouched `dcd0ed0` baseline was built with the repository's Kujo 1.0.0 runtime, copied to `raw/baseline/output/`, hashed, and crawled before source remediation. The same 26 sitemap canonical URLs were crawled after remediation. GitHub Pages runs `31451814639`, `31452140745`, and final fallback-removal run `31464566449` succeeded. Cloudflare Bulk Redirect List `4ecb2aecd75a48aeb27a4bd575b0198b` and active rule `1a0ee52fa1654bd7ae652f5987e89cea` replaced the temporary static fallbacks; all 26 canonical URLs, 24 exact 301 mappings, query preservation, and five discovery assets were verified independently in production.

The crawl combined sitemap and HTML discovery, parsed metadata, headings, canonical tags, robots directives, JSON-LD, links, content text, and media, then probed production independently over IPv4. Third-party 401/403/405/429/transport failures would be classified as blocked or indeterminate rather than broken. No such destination remained in the normalized crawl.

Representative home, collection, and lesson templates were measured with Lighthouse 13.0.1 under its mobile simulated-throttling profile against comparable local static servers. These are lab observations, not field Core Web Vitals. Search observations are dated samples from a web-search tool whose provider, locale, personalization, and full ranking set were not exposed.

Internal SEO and AI-readiness scores are transparent audit heuristics only. They are not Google, Bing, OpenAI, Anthropic, or third-party platform scores.
