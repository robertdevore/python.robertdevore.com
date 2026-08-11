# Recommendations and measurement plan

## Immediate owner actions

1. Submit `https://python.robertdevore.com/sitemap.xml` in Google Search Console and Bing Webmaster Tools, then inspect representative `/course/` URLs and retired `/blog/` URLs.
2. Keep Cloudflare rule `1a0ee52fa1654bd7ae652f5987e89cea` enabled and retain all 24 exact mappings during the migration measurement window.
3. Enable privacy-appropriate Cloudflare or origin request logs for complete 404/5xx and crawler observability.
4. Preserve separate policy decisions for search crawlers, user-triggered fetchers, and training crawlers.

## Comparable measurement windows

- **7 days:** confirm deployment, crawl the 26 canonical URLs and 24 legacy mappings, submit sitemaps, inspect representative indexing state, and check server/CDN errors.
- **28 days:** compare Google/Bing clicks, impressions, CTR, average position, indexed URLs, sitemap state, top queries/pages, countries, devices, and generative-AI reports where exposed.
- **60 days:** repeat the same query/page exports, controlled AI benchmark questions, crawler-log review, production Lighthouse, and CrUX/RUM checks. Compare retired versus canonical URL appearances.
- **90 days:** assess durable canonical consolidation, non-branded discovery, course-start conversions, external references, AI mentions/citations, and content refresh priorities using the same datasets and questions.

Do not claim ranking, traffic, conversion, or AI-citation improvement until those post-change measurements exist.
