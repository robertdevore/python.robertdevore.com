#!/usr/bin/env python3
"""Compile judgment-led audit artifacts from preserved crawl evidence."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from urllib.parse import urlparse


AUDIT = Path(__file__).resolve().parents[1]
BASE = "https://python.robertdevore.com"
UNAVAILABLE = "NOT AVAILABLE — DATA ACCESS REQUIRED"


def read_csv(name: str) -> list[dict[str, str]]:
    with (AUDIT / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(name: str, fields: list[str], rows: list[dict[str, object]]) -> None:
    with (AUDIT / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


baseline = read_csv("baseline.csv")
after = read_csv("after.csv")
base_summary = json.loads((AUDIT / "baseline-summary.json").read_text())
after_summary = json.loads((AUDIT / "after-summary.json").read_text())

lesson_topics = {
    "welcome-to-the-complete-python-development-course": ("complete Python course", "course orientation; learning path; prerequisites"),
    "chapter-1-beginner-python": ("beginner Python fundamentals", "setup; syntax; control flow; functions; errors"),
    "python-setup-and-ides": ("Python installation and IDE setup", "Windows; macOS; Linux; VS Code; PyCharm; troubleshooting"),
    "python-syntax-and-data-types": ("Python syntax and data types", "variables; strings; numbers; booleans; conversion"),
    "syntax-and-data-types": ("Python control flow", "if statements; for loops; while loops; input validation"),
    "functions-and-modules": ("Python functions and modules", "parameters; return values; scope; imports; standard library"),
    "basic-error-handling": ("basic Python error handling", "try; except; validation; recovery; user messages"),
    "chapter-2-intermediate-python": ("intermediate Python development", "OOP; files; environments; exceptions; testing"),
    "object-oriented-programming": ("Python object-oriented programming", "classes; inheritance; composition; polymorphism; properties"),
    "file-io-and-data-persistence": ("Python file I/O", "text files; paths; CSV; JSON; persistence; exceptions"),
    "virtual-environments-and-package-management": ("Python virtual environments", "venv; pip; requirements; dependency conflicts"),
    "exceptions-and-robust-error-handling": ("Python exceptions", "custom exceptions; cleanup; logging; resilient failures"),
    "introduction-to-testing": ("Python testing", "pytest; unit tests; fixtures; mocking; test workflow"),
    "chapter-3-advanced-python": ("advanced Python development", "algorithms; decorators; concurrency; APIs; packaging"),
    "advanced-data-structures-and-algorithms": ("Python data structures and algorithms", "collections; heaps; graphs; complexity; performance"),
    "generators-decorators-and-context-managers": ("Python generators decorators and context managers", "iterators; yield; wraps; resource cleanup"),
    "concurrency-and-parallelism": ("Python concurrency and parallelism", "threading; multiprocessing; asyncio; synchronization"),
    "building-and-consuming-apis": ("building and consuming Python APIs", "Flask; FastAPI; validation; authentication; HTTP clients"),
    "packaging-distribution-and-best-practices": ("Python packaging and PyPI", "pyproject.toml; build; twine; CI; linting; typing"),
    "course-conclusion-from-python-novice-to-professional-developer": ("Python course conclusion", "skills review; portfolio projects; next steps"),
}

content_rows = []
keyword_rows = []
for row in after:
    path = urlparse(row["url"]).path
    slug = path.rstrip("/").split("/")[-1] if path != "/" else "home"
    if slug in lesson_topics:
        topic, supporting = lesson_topics[slug]
        purpose = "Teach one sequenced part of the Python curriculum"
        intent = "educational how-to"
        audience = "Python learners"
        entity = "Python programming language"
        gap = "Add verified exercise outputs or runnable companion repositories where editorially appropriate"
        questions = f"what is {topic}; how to learn {topic}; {topic} examples"
        action = "Keep examples current; add primary documentation citations during future editorial review"
    elif path == "/":
        topic, supporting = "complete Python development course", "curriculum; beginner; intermediate; advanced; free lessons"
        purpose, intent, audience, entity = "Introduce and route learners into the course", "course discovery", "prospective Python learners", "Python Course"
        gap, questions, action = "Measured search and AI visibility are unavailable", "is this Python course free; what does the course cover", "Measure impressions and AI citations after deployment"
    elif path == "/about/":
        topic, supporting = "about the Python Course", "author; curriculum; Kujo SSG; SiteKit; architecture"
        purpose, intent, audience, entity = "Explain authorship, scope, and publishing stack", "navigational and trust", "learners and technical evaluators", "Python Course and Robert DeVore"
        gap, questions, action = "No editorial policy or correction process is published", "who created the Python course; how is the site built", "Consider a concise corrections and update policy"
    else:
        topic, supporting = "Python course curriculum", "lesson listings; pagination; learning path"
        purpose, intent, audience, entity = "List sequenced course lessons", "course navigation", "Python learners", "Python Course"
        gap, questions, action = "Pagination is useful navigation but not a primary citation target", "Python course lessons; Python curriculum", "Keep pagination internally linked and canonical"

    content_rows.append({
        "phase": "after", "url": row["url"], "source_file": row["source_file"], "page_type": row["page_type"],
        "primary_purpose": purpose, "search_intent": intent, "target_audience": audience,
        "central_entity": entity, "primary_query_theme": topic, "supporting_topics": supporting,
        "h1": row["h1"], "heading_structure": row["heading_structure"], "word_count": row["word_count"],
        "published_date": row["published_date"], "modified_date": row["modified_date"],
        "first_hand_signals": "authored lesson narrative; extensive code examples" if slug in lesson_topics else "repository-backed site and curriculum description",
        "content_gap": gap, "competing_internal_url": "", "recommended_action": action,
    })
    keyword_rows.append({
        "phase": "after", "url": row["url"], "primary_topic": topic, "primary_entity": entity,
        "search_intent": intent, "primary_query_theme": topic,
        "secondary_queries": supporting, "related_entities": supporting,
        "relevant_questions": questions, "competing_internal_url": "", "content_gap": gap,
        "recommended_action": action,
    })

write_csv("content-audit.csv", list(content_rows[0]), content_rows)
write_csv("keyword-map.csv", list(keyword_rows[0]), keyword_rows)

search_rows = [
    {
        "query": '"python.robertdevore.com"', "search_engine": "Codex web search (provider not exposed)", "date": "2026-08-10",
        "country": "not exposed", "device": "not exposed", "page_found": "No current course URL observed; robertdevore.com blog appeared",
        "observed_position_or_range": "not a stable rank measurement", "competing_results": "robertdevore.com/blog",
        "rich_features": "not exposed", "ai_result_presence": "not exposed", "evidence": "dated web search receipt summarized in executive report",
        "limitations": "Search provider, neutral rank, locale, personalization, and complete result set were not exposed.",
    },
    {
        "query": "site:python.robertdevore.com generators decorators context managers", "search_engine": "Codex web search (provider not exposed)", "date": "2026-08-10",
        "country": "not exposed", "device": "not exposed", "page_found": f"{BASE}/blog/generators-decorators-and-context-managers/",
        "observed_position_or_range": "returned result", "competing_results": "none recorded for site-restricted observation",
        "rich_features": "standard result", "ai_result_presence": "not exposed", "evidence": "web observation returned the retired /blog/ URL",
        "limitations": "Site-restricted observation proves stale discovery, not a public-query ranking.",
    },
    {
        "query": "site:python.robertdevore.com Python setup IDEs", "search_engine": "Codex web search (provider not exposed)", "date": "2026-08-10",
        "country": "not exposed", "device": "not exposed", "page_found": f"{BASE}/blog/python-setup-and-ides/",
        "observed_position_or_range": "returned result", "competing_results": "none recorded for site-restricted observation",
        "rich_features": "standard result", "ai_result_presence": "not exposed", "evidence": "web observation returned the retired /blog/ URL",
        "limitations": "Site-restricted observation proves stale discovery, not a public-query ranking.",
    },
    {
        "query": f'"{BASE}/course/generators-decorators-and-context-managers/"', "search_engine": "Codex web search (provider not exposed)", "date": "2026-08-10",
        "country": "not exposed", "device": "not exposed", "page_found": f"{BASE}/page/4/ instead of the exact current URL",
        "observed_position_or_range": "current URL not observed", "competing_results": "retired pagination URL",
        "rich_features": "standard result", "ai_result_presence": "not exposed", "evidence": "exact-URL observation surfaced retired /page/4/",
        "limitations": "Index state must be confirmed in Google Search Console and Bing Webmaster Tools.",
    },
]
search_fields = ["query", "search_engine", "date", "country", "device", "page_found", "observed_position_or_range", "competing_results", "rich_features", "ai_result_presence", "evidence", "limitations"]
write_csv("search-rankings.csv", search_fields, search_rows)

questions = [
    "What is a good free Python course for beginners?",
    "How do I install Python and choose an IDE?",
    "How do Python decorators and context managers work?",
    "When should I use threading, multiprocessing, or asyncio in Python?",
    "How do I build a REST API with Flask or FastAPI?",
    "How do I package and publish a Python project to PyPI?",
    "What are the best alternatives to this Python course?",
    "How do I troubleshoot Python virtual environment problems?",
    "Who created the Python Course at python.robertdevore.com?",
    "What topics does the Robert DeVore Python course cover?",
]
ai_rows = [{
    "question": question, "platform": UNAVAILABLE, "date": "2026-08-10", "domain_appeared": "",
    "domain_cited": "", "cited_url": "", "citation_context": "", "citation_order": "",
    "competing_domains": "", "accurate_representation": "", "content_gap": "",
    "evidence": UNAVAILABLE, "limitations": UNAVAILABLE,
} for question in questions]
ai_fields = ["question", "platform", "date", "domain_appeared", "domain_cited", "cited_url", "citation_context", "citation_order", "competing_domains", "accurate_representation", "content_gap", "evidence", "limitations"]
write_csv("ai-search-benchmark.csv", ai_fields, ai_rows)

crawlers = [
    ("Googlebot", "Google Search discovery/indexing"), ("Bingbot", "Bing discovery/indexing"),
    ("OAI-SearchBot", "ChatGPT search discovery"), ("GPTBot", "OpenAI model training"),
    ("ChatGPT-User", "user-triggered OpenAI fetch"), ("Claude-SearchBot", "Claude search discovery"),
    ("Claude-User", "user-triggered Claude fetch"), ("ClaudeBot", "Anthropic model training"),
    ("PerplexityBot", "Perplexity discovery"),
]
crawler_rows = [{
    "crawler": name, "purpose": purpose, "robots_access": "allowed by User-agent: * / Allow: /",
    "live_status": 200, "waf_or_cdn_result": "200 over IPv4; Cloudflare response reached GitHub Pages origin",
    "recommended_action": "Preserve owner policy; review training-crawler access separately from search access",
    "action_taken": "No training-policy change; access verified", "evidence": f"raw/production/ua-{name.lower()}-headers.txt",
} for name, purpose in crawlers]
write_csv("crawler-access.csv", list(crawler_rows[0]), crawler_rows)

redirect_rows = []
for slug in ["python-setup-and-ides", "generators-decorators-and-context-managers"]:
    redirect_rows += [
        {"phase": "baseline", "source_url": f"{BASE}/blog/{slug}/", "source_variant": "HTTPS legacy lesson", "http_status": 404,
         "target_url": f"{BASE}/course/{slug}/", "chain_length": 0, "final_status": 404, "canonical_target": f"{BASE}/course/{slug}/",
         "query_preserved": "not applicable", "verification": "production receipt", "issues": "Indexed legacy URL returned 404"},
        {"phase": "after", "source_url": f"{BASE}/blog/{slug}/", "source_variant": "generated legacy lesson", "http_status": 200,
         "target_url": f"{BASE}/course/{slug}/", "chain_length": 1, "final_status": 200, "canonical_target": f"{BASE}/course/{slug}/",
         "query_preserved": "no", "verification": "production 200 instant meta refresh and canonical target verified after deployment", "issues": "Prefer edge 301/308 when Cloudflare access is available"},
    ]
redirect_rows += [
    {"phase": "baseline", "source_url": f"{BASE}/page/4/", "source_variant": "HTTPS legacy pagination", "http_status": 404,
     "target_url": f"{BASE}/course/page/4/", "chain_length": 0, "final_status": 404, "canonical_target": f"{BASE}/course/page/4/",
     "query_preserved": "not applicable", "verification": "production receipt", "issues": "Indexed legacy URL returned 404"},
    {"phase": "after", "source_url": f"{BASE}/page/4/", "source_variant": "generated legacy pagination", "http_status": 200,
     "target_url": f"{BASE}/course/page/4/", "chain_length": 1, "final_status": 200, "canonical_target": f"{BASE}/course/page/4/",
     "query_preserved": "no", "verification": "production 200 instant meta refresh and canonical target verified after deployment", "issues": "Prefer edge 301/308 when Cloudflare access is available"},
    {"phase": "baseline", "source_url": "http://python.robertdevore.com/", "source_variant": "HTTP canonical host", "http_status": 301,
     "target_url": f"{BASE}/", "chain_length": 1, "final_status": 200, "canonical_target": f"{BASE}/", "query_preserved": "not tested",
     "verification": "production header receipt", "issues": "none"},
]
redirect_fields = ["phase", "source_url", "source_variant", "http_status", "target_url", "chain_length", "final_status", "canonical_target", "query_preserved", "verification", "issues"]
write_csv("redirects.csv", redirect_fields, redirect_rows)

issues = [
    {"id": "SEO-001", "phase": "baseline", "category": "migration", "severity": "P1", "affected_urls": "/blog/* and /page/2-4/", "affected_count": 24,
     "evidence": "Search observations returned retired URLs; three representative production probes returned 404", "expected_benefit": "Recover users and consolidate legacy URL signals", "confidence": "high", "difficulty": "medium",
     "recommended_action": "Serve permanent redirects to exact /course/ equivalents", "owner": "repository/edge owner", "status": "fixed and production verified with instant meta refresh; edge 301/308 recommended"},
    {"id": "SEO-002", "phase": "baseline", "category": "internal links", "severity": "P1", "affected_urls": "/about/", "affected_count": 3,
     "evidence": "baseline broken-links.csv contained malformed href values beginning </course/", "expected_benefit": "Restore crawlable reader paths", "confidence": "high", "difficulty": "low",
     "recommended_action": "Correct Markdown destinations", "owner": "repository", "status": "fixed"},
    {"id": "SEO-003", "phase": "baseline", "category": "canonicalization", "severity": "P2", "affected_urls": "all canonical pages", "affected_count": 26,
     "evidence": "baseline internal link graph used /index.html for the brand home link; production /index.html returned 200", "expected_benefit": "Align internal signals with root canonical", "confidence": "high", "difficulty": "low",
     "recommended_action": "Link the brand directly to /", "owner": "repository", "status": "fixed"},
    {"id": "SEO-004", "phase": "baseline", "category": "content accuracy", "severity": "P2", "affected_urls": "/course/python-setup-and-ides/ and /course/building-and-consuming-apis/", "affected_count": 2,
     "evidence": "Unsupported Python-version guidance, obsolete macOS Python statement, sudo pip advice, and deprecated datetime.utcnow examples", "expected_benefit": "Improve trust, currentness, and answer accuracy", "confidence": "high", "difficulty": "low",
     "recommended_action": "Update narrow factual passages and modified dates", "owner": "repository", "status": "fixed"},
    {"id": "SEO-005", "phase": "baseline", "category": "metadata", "severity": "P2", "affected_urls": "12 lesson URLs", "affected_count": 12,
     "evidence": "Descriptions were 182-187 characters and ended with an editorial ellipsis", "expected_benefit": "Clearer page summaries for search and sharing", "confidence": "high", "difficulty": "low",
     "recommended_action": "Replace with complete, factual lesson summaries", "owner": "repository", "status": "fixed"},
    {"id": "SEO-006", "phase": "after", "category": "performance", "severity": "P2", "affected_urls": "representative home, course, and lesson templates", "affected_count": 3,
     "evidence": "Local Lighthouse mobile LCP ranged 2.87-3.77s; render-blocking CSS and 75-118 KiB estimated unused CSS", "expected_benefit": "Faster first render on constrained devices", "confidence": "medium", "difficulty": "medium",
     "recommended_action": "Measure production/field data first; then reduce or split render-blocking SiteKit CSS", "owner": "repository/operations", "status": "open recommendation"},
    {"id": "SEO-007", "phase": "after", "category": "measurement", "severity": "P2", "affected_urls": "sitewide", "affected_count": 26,
     "evidence": UNAVAILABLE, "expected_benefit": "Establish real search and AI outcome baselines", "confidence": "high", "difficulty": "medium",
     "recommended_action": "Connect Search Console, Bing Webmaster Tools, analytics, CDN logs, CrUX/RUM, and controlled AI sessions", "owner": "site owner", "status": "open; access required"},
    {"id": "SEO-008", "phase": "after", "category": "AI discovery experiment", "severity": "P3", "affected_urls": "/llms.txt", "affected_count": 1,
     "evidence": "Google's 2026 AI optimization guide says Google Search ignores llms.txt; current file remains well-formed", "expected_benefit": "Potential compatibility with non-Google consumers only", "confidence": "high", "difficulty": "low",
     "recommended_action": "Maintain as an experiment; do not describe it as a Google ranking factor", "owner": "repository", "status": "accepted experiment"},
]
issue_fields = ["id", "phase", "category", "severity", "affected_urls", "affected_count", "evidence", "expected_benefit", "confidence", "difficulty", "recommended_action", "owner", "status"]
write_csv("issues.csv", issue_fields, issues)

research = """# Research sources

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
"""
(AUDIT / "research-sources.md").write_text(research, encoding="utf-8")

methodology = """# Methodology

Audit date: 2026-08-10 (America/Detroit). Production receipts may show 2026-08-11 UTC.

The audit mapped `Markdown and templates → Kujo SSG build → generated output → GitHub Pages origin → Cloudflare edge → crawler/browser`. The untouched `dcd0ed0` baseline was built with the repository's Kujo 1.0.0 runtime, copied to `raw/baseline/output/`, hashed, and crawled before source remediation. The same 26 sitemap canonical URLs were crawled after remediation. GitHub Pages deployment run `31451814639` succeeded, after which all 26 canonical URLs and 24 legacy mappings were verified independently in production.

The crawl combined sitemap and HTML discovery, parsed metadata, headings, canonical tags, robots directives, JSON-LD, links, content text, and media, then probed production independently over IPv4. Third-party 401/403/405/429/transport failures would be classified as blocked or indeterminate rather than broken. No such destination remained in the normalized crawl.

Representative home, collection, and lesson templates were measured with Lighthouse 13.0.1 under its mobile simulated-throttling profile against comparable local static servers. These are lab observations, not field Core Web Vitals. Search observations are dated samples from a web-search tool whose provider, locale, personalization, and full ranking set were not exposed.

Internal SEO and AI-readiness scores are transparent audit heuristics only. They are not Google, Bing, OpenAI, Anthropic, or third-party platform scores.
"""
(AUDIT / "methodology.md").write_text(methodology, encoding="utf-8")

data_availability = f"""# Data availability

## Available

- Repository source and Git history.
- Untouched generated baseline and reproducible after build.
- Full 26-canonical sitemap/HTML crawl, local link graph, metadata, JSON-LD, and media checks.
- Production DNS, HTTP, canonical-host, crawler-user-agent, discovery-file, and representative 404 receipts.
- Comparable local Lighthouse lab receipts for three templates.
- Dated, limited web-search observations.

## Unavailable

- Google Search Console performance, indexing, sitemap, and generative-AI reports: {UNAVAILABLE}
- Bing Webmaster Tools and IndexNow reports: {UNAVAILABLE}
- Analytics and conversions: {UNAVAILABLE}
- Cloudflare/GitHub origin request logs and complete 404/5xx enumeration: {UNAVAILABLE}
- CrUX/RUM field Core Web Vitals: {UNAVAILABLE}
- Backlink index and authorized neutral rank API: {UNAVAILABLE}
- Controlled ChatGPT, Claude, Perplexity, Gemini, or other AI answer/citation sessions: {UNAVAILABLE}

Unavailable data is not inferred from crawl health or web-search snippets.
"""
(AUDIT / "data-availability.md").write_text(data_availability, encoding="utf-8")

changes = """# Changes

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
"""
(AUDIT / "changes.md").write_text(changes, encoding="utf-8")

before_after = f"""# Before and after

| Metric | Baseline | After |
| --- | ---: | ---: |
| Canonical pages | {base_summary['pages']} | {after_summary['pages']} |
| Production 200 canonical pages at crawl time | {base_summary['production_200']} | {after_summary['production_200']} |
| Indexable canonical pages | {base_summary['indexable']} | {after_summary['indexable']} |
| Missing / duplicate titles | {base_summary['missing_titles']} / {base_summary['duplicate_titles']} | {after_summary['missing_titles']} / {after_summary['duplicate_titles']} |
| Missing / duplicate descriptions | {base_summary['missing_descriptions']} / {base_summary['duplicate_descriptions']} | {after_summary['missing_descriptions']} / {after_summary['duplicate_descriptions']} |
| Canonical mismatches / H1 issues | {base_summary['canonical_mismatches']} / {base_summary['h1_issues']} | {after_summary['canonical_mismatches']} / {after_summary['h1_issues']} |
| Broken internal link occurrences | {base_summary['broken_internal_links']} | {after_summary['broken_internal_links']} |
| Orphans / sitemap mismatches | {base_summary['orphans']} / {base_summary['sitemap_mismatches']} | {after_summary['orphans']} / {after_summary['sitemap_mismatches']} |
| Invalid or missing JSON-LD pages | {base_summary['invalid_schema_pages']} | {after_summary['invalid_schema_pages']} |
| Missing image alt / dimensions | {base_summary['missing_alt']} / {base_summary['missing_dimensions']} | {after_summary['missing_alt']} / {after_summary['missing_dimensions']} |
| Noncanonical brand links to `/index.html` | 26 | 0 |
| Complete legacy migration fallbacks | 0 | 24 |
| Truncated lesson descriptions remediated | 0 | 12 |
| P0 / P1 root causes | 0 / 2 | 0 / 0 locally and in verified production behavior |

## Internal heuristic scores

- SEO health: **79/100 → 91/100**. Weighted evidence: crawlability/indexability 15→18/20, metadata 12→15/15, architecture 10→14/15, content/currentness 11→13/15, structured data 10→10/10, performance 7→7/10, media 5→5/5, authority 5→5/5, AI readiness 4→4/5.
- AI Search Readiness: **83/100 → 85/100**. Search crawler access 15/15, indexability 10/10, entity clarity 9/10, attribution 10/10, original/citable information 12/15, semantics 10/10, internal relationships 10/10, freshness 2→4/5, technical/media 5/5, measured AI visibility 0/10.

Measured AI visibility correctly receives zero because controlled platform data was unavailable.
"""
(AUDIT / "before-after.md").write_text(before_after, encoding="utf-8")

unresolved = f"""# Unresolved

1. All 24 instant meta-refresh fallbacks are deployed and verified, but edge-level 301/308 redirects remain preferred. Cloudflare configuration access was not available: {UNAVAILABLE}
2. Search Console, Bing Webmaster Tools, analytics, request logs, field CWV, backlink, ranking, and controlled AI-citation data remain: {UNAVAILABLE}
3. Search observations still exposed retired `/blog/` and `/page/4/` URLs on 2026-08-10. Recrawl and canonical consolidation require elapsed time after deployment.
4. Local Lighthouse mobile LCP remained 2.87–3.77 seconds. Production compression/cache behavior and field evidence are required before a CSS-delivery change is justified.
5. `www.python.robertdevore.com` has no DNS record. This is not the canonical host and no evidence showed it was previously public; adding it requires an explicit host-policy decision.
"""
(AUDIT / "unresolved.md").write_text(unresolved, encoding="utf-8")

recommendations = """# Recommendations and measurement plan

## Immediate owner actions

1. Submit `https://python.robertdevore.com/sitemap.xml` in Google Search Console and Bing Webmaster Tools, then inspect representative `/course/` URLs and retired `/blog/` URLs.
2. If Cloudflare configuration access becomes available, replace the static meta-refresh fallbacks with exact one-hop 301/308 edge redirects while preserving each destination mapping.
3. Enable privacy-appropriate Cloudflare or origin request logs for complete 404/5xx and crawler observability.
4. Preserve separate policy decisions for search crawlers, user-triggered fetchers, and training crawlers.

## Comparable measurement windows

- **7 days:** confirm deployment, crawl the 26 canonical URLs and 24 legacy mappings, submit sitemaps, inspect representative indexing state, and check server/CDN errors.
- **28 days:** compare Google/Bing clicks, impressions, CTR, average position, indexed URLs, sitemap state, top queries/pages, countries, devices, and generative-AI reports where exposed.
- **60 days:** repeat the same query/page exports, controlled AI benchmark questions, crawler-log review, production Lighthouse, and CrUX/RUM checks. Compare retired versus canonical URL appearances.
- **90 days:** assess durable canonical consolidation, non-branded discovery, course-start conversions, external references, AI mentions/citations, and content refresh priorities using the same datasets and questions.

Do not claim ranking, traffic, conversion, or AI-citation improvement until those post-change measurements exist.
"""
(AUDIT / "recommendations.md").write_text(recommendations, encoding="utf-8")

executive = f"""# Executive summary

**Status: PASS WITH RECOMMENDATIONS**  
**Audit date: 2026-08-10 (America/Detroit)**

The untouched site had 26 healthy, indexable canonical pages with unique metadata, valid JSON-LD, complete sitemap/feed/robots discovery, strong internal reachability, and successful live access for major search and AI crawler user agents. Two P1 root causes remained: three malformed `/about/` links and a migration gap where search observations still surfaced retired `/blog/` and `/page/4/` URLs that production returned as 404.

The remediation corrected all three broken links, aligned 26 brand links with the root canonical, added 24 exact legacy-route fallbacks, refreshed two stale technical lessons, and replaced 12 truncated descriptions. The rebuilt canonical crawl now reports 26/26 production-reachable canonicals, zero broken internal links, zero metadata duplicates, zero canonical/H1/schema/sitemap/orphan defects, and unchanged content inventory. The full repository release contract passes for 26 canonical routes, 24 legacy redirects, 20 lessons, 20 feed items, 41,821 source words, and 342 code blocks. GitHub Pages run `31451814639` succeeded; the independent production verifier then passed all 26 canonical URLs, all 24 legacy mappings, and five discovery assets.

Internal heuristic scores moved from **79 to 91 SEO health** and **83 to 85 AI Search Readiness**. These are audit trend heuristics, not platform scores. The AI score remains capped because measured AI visibility received 0/10: controlled AI citation data was {UNAVAILABLE.lower()}.

The real search baseline is limited but material: dated web observations exposed retired URLs rather than the current `/course/` equivalents. Rankings, clicks, impressions, index coverage, conversions, field Core Web Vitals, backlinks, complete request errors, and AI citations were {UNAVAILABLE.lower()}. Local Lighthouse mobile LCP ranged 2.87–3.77 seconds and warrants production/field measurement before CSS delivery is changed.

Next: submit the sitemap in search consoles and compare the same platform exports and AI questions at 7, 28, 60, and 90 days. Prefer exact Cloudflare 301/308 redirects over meta refresh when edge access is available.
"""
(AUDIT / "executive-summary.md").write_text(executive, encoding="utf-8")

print("Compiled content, query, crawler, redirect, issue, and narrative artifacts.")
