# Research sources

Retrieved 2026-08-10 (America/Detroit). Technical conclusions use current first-party documentation.

| Source | Evidence class | Audit conclusion |
| --- | --- | --- |
| [Google crawling and indexing](https://developers.google.com/search/docs/crawling-indexing) | Official requirement/recommendation | Crawlable links, robots controls, sitemaps, canonicals, and accessible content remain the foundation. |
| [Google robots meta specification](https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag) | Official requirement | Indexing directives must remain crawlable to be observed. |
| [Google sitemap guidance](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap) | Official recommendation | Include canonical URLs that should appear in Search; sitemaps are discovery hints, not indexing guarantees. |
| [Google structured data guidelines](https://developers.google.com/search/docs/appearance/structured-data/sd-policies) | Official requirement/recommendation | JSON-LD must be valid, visible-content-aligned, current, relevant, and non-misleading; rich results are not guaranteed. |
| [Google generative AI optimization guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) | Official recommendation | Foundational SEO, unique people-first content, crawlability, page experience, and Search Console measurement apply; Google ignores `llms.txt` for Search and needs no special AI schema. |
| [Google redirects](https://developers.google.com/search/docs/crawling-indexing/301-redirects) | Official recommendation | 301/308 is preferred; an instant meta refresh is a viable permanent-redirect fallback when server redirects are unavailable. |
| [Google site moves](https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes) | Official recommendation | Map old URLs to relevant new URLs, keep redirects long-term, update links, and submit the current sitemap. |
| [Bing IndexNow](https://www.bing.com/webmasters/help/indexnow-0z209wby) | Official recommendation | IndexNow can notify Bing of added, changed, or deleted URLs; implementation remains optional and requires operational ownership. |
| [Schema.org Course](https://schema.org/Course) | Official vocabulary | `Course`, provider, and educational properties are valid vocabulary; vocabulary validity is separate from Google rich-result eligibility. |
| [OpenAI crawlers](https://developers.openai.com/api/docs/bots) | Official crawler policy | OAI-SearchBot controls ChatGPT search discovery, GPTBot controls training use, and ChatGPT-User is user-triggered; policies are independent. |
| [Anthropic crawlers](https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler) | Official crawler policy | Claude-SearchBot, ClaudeBot, and Claude-User serve separate search, training, and user-fetch purposes. |
| [Python 3.14.6 release](https://www.python.org/downloads/release/python-3146/) and [version documentation](https://www.python.org/doc/versions/) | Official technical source | Python 3.14 is the current stable series observed at audit time; course setup advice should avoid unsupported fixed minimums. |

`llms.txt` is retained as an experimental discovery artifact, not a documented Google Search requirement or ranking mechanism.
