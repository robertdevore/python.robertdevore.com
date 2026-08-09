#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

fail() {
	printf 'FAIL: %s\n' "$1"
	exit 1
}

assert_path() {
	[[ -e "$1" ]] || fail "missing path: $1"
}

assert_contains() {
	grep -Fq "$2" "$1" || fail "expected '$2' in $1"
}

assert_not_contains() {
	grep -Fq "$2" "$1" && fail "did not expect '$2' in $1"
	return 0
}

bash -n scripts/build.sh scripts/build-parallel.sh scripts/test-site.sh scripts/validate-generated-output.sh
node --check assets/js/syntax-highlight.js
node --check assets/js/docs.js
node scripts/test-syntax-highlight.js

assert_path assets/sitekit/sitekit.css
assert_path assets/sitekit/sitekit.js
assert_path assets/sitekit/fonts/DepartureMono-Regular.woff2
assert_path assets/sitekit/fonts/DepartureMono-LICENSE.txt
assert_path assets/fonts/inter-latin-400.woff2
assert_path assets/fonts/inter-latin-700.woff2
assert_path assets/fonts/Inter-LICENSE.txt
assert_path assets/js/syntax-highlight.js
assert_path assets/images/python-course-social.svg
assert_path assets/images/python-course-social.png

post_count="$(find content/posts -maxdepth 1 -name '*.md' -type f | wc -l | tr -d ' ')"
[[ "$post_count" == "20" ]] || fail "expected 20 course lessons, found $post_count"

course_word_count="$(wc -w content/posts/*.md | tail -1 | awk '{print $1}')"
[[ "$course_word_count" -ge 40000 ]] || fail "course content looks incomplete: $course_word_count words"

SITE_URL=https://python.robertdevore.com bash scripts/build.sh

assert_path output/index.html
assert_path output/about/index.html
assert_path output/course/index.html
assert_path output/course/python-setup-and-ides/index.html
assert_path output/course/python-syntax-and-data-types/index.html
assert_path output/course/syntax-and-data-types/index.html
assert_path output/course/course-conclusion-from-python-novice-to-professional-developer/index.html
[[ ! -e output/blog ]] || fail "legacy /blog/ output should not be generated"
[[ ! -e output/page ]] || fail "duplicate homepage pagination should not be generated"
[[ ! -e output/sample-page ]] || fail "stale Stattic sample page should not be generated"
assert_path output/feed/index.xml
assert_path output/sitemap.xml
assert_path output/robots.txt
assert_path output/llms.txt
assert_path output/CNAME
assert_path output/assets/sitekit/fonts/DepartureMono-Regular.woff2
assert_path output/assets/fonts/inter-latin-400.woff2
assert_path output/assets/fonts/inter-latin-700.woff2
assert_path output/assets/js/docs-search-index.json
assert_path output/assets/js/syntax-highlight.js
assert_path output/assets/images/python-course-social.png

assert_contains output/index.html 'Learn Python. Build real things.'
assert_contains output/index.html 'class="course-stats"'
assert_contains output/index.html '<code class="language-python">def start_journey(name):'
assert_contains output/index.html 'assets/js/syntax-highlight.js'
assert_contains output/index.html 'assets/css/style.css?v=20260809-1'
assert_contains output/index.html 'assets/js/docs.js?v=20260809-1'
assert_contains output/index.html 'href="/course/" class="text-primary hover:underline">Course</a>'
assert_contains output/index.html 'property="og:image" content="https://python.robertdevore.com/assets/images/python-course-social.png"'
assert_contains output/index.html '"@type":"Course"'
assert_contains output/index.html 'name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"'
assert_contains output/course/python-syntax-and-data-types/index.html '1.2. Syntax &amp; Data Types'
assert_contains output/course/syntax-and-data-types/index.html '1.3. Control Flow (If, For, While)'
assert_contains output/course/python-setup-and-ides/index.html 'class="docs-shell"'
assert_contains output/course/python-setup-and-ides/index.html 'href="#installing-python"'
assert_contains output/course/chapter-1-beginner-python/index.html 'class="language-java"'
assert_contains output/course/chapter-1-beginner-python/index.html 'class="language-python"'
assert_contains output/course/chapter-1-beginner-python/index.html '"@type":"Article"'
assert_contains output/course/chapter-1-beginner-python/index.html '"learningResourceType":"Lesson"'
assert_not_contains output/course/chapter-1-beginner-python/index.html '"@type":"BlogPosting"'
assert_not_contains output/course/chapter-1-beginner-python/index.html '<p>public class Hello {</p>'
assert_contains output/course/virtual-environments-and-package-management/index.html 'class="language-text">README.md'
assert_not_contains output/course/virtual-environments-and-package-management/index.html 'class="language-text"><h2>Setup</h2>'
assert_not_contains output/course/virtual-environments-and-package-management/index.html '<h1>pip</h1>'
assert_contains output/about/index.html 'Kujo SSG and SiteKit'
assert_contains output/assets/css/style.css 'Departure Mono'
assert_contains output/assets/css/style.css 'font-family: "Inter";'
assert_contains output/assets/css/style.css 'scrollbar-color: var(--python-blue) var(--python-soft)'
assert_contains output/assets/css/style.css '.card-grid .listing-card-title a, .card-grid .listing-card-title a:hover { text-decoration: none; }'
assert_contains output/assets/css/style.css '#3776ab'
assert_contains output/assets/css/style.css '#ffd343'
assert_contains output/assets/css/style.css '.docs-home-terminal { margin: 0; overflow: hidden; background: var(--docs-code); color: var(--docs-code-ink);'
assert_contains output/assets/css/style.css 'border-inline-start: .35rem solid var(--python-yellow); box-shadow: none;'
assert_contains output/assets/css/style.css '.syntax-keyword, .syntax-atrule { color: #7dd3fc; }'
assert_contains output/assets/css/style.css '.syntax-string, .syntax-code, .syntax-inserted { color: #86efac; }'
assert_contains output/assets/js/docs.js "pre.setAttribute('data-code-language', language.toUpperCase())"
assert_contains output/assets/js/docs.js "bindCopyButton(button, block.querySelector('code') || block)"
assert_contains output/assets/js/docs.js "shell.className = 'docs-code-shell'"
assert_contains output/assets/js/docs.js 'shell.appendChild(button)'
assert_contains output/assets/css/style.css '.docs-body .docs-code-shell { position: relative;'
assert_not_contains output/assets/css/style.css 'box-shadow: .75rem .75rem 0 var(--python-yellow)'
assert_contains output/robots.txt 'Allow: /'
assert_contains output/robots.txt 'Sitemap: https://python.robertdevore.com/sitemap.xml'
assert_contains output/sitemap.xml 'https://python.robertdevore.com/course/course-conclusion-from-python-novice-to-professional-developer/'
assert_contains output/feed/index.xml 'xmlns:atom="http://www.w3.org/2005/Atom"'
assert_contains output/feed/index.xml 'A complete path from Python beginner to professional developer.'
assert_contains output/llms.txt '## Lessons'
assert_contains output/llms.txt '## Feeds and discovery'
assert_contains output/404.html 'name="robots" content="noindex, follow"'
assert_contains output/CNAME 'python.robertdevore.com'
assert_contains output/assets/js/docs-search-index.json '"route": "course/welcome-to-the-complete-python-development-course/"'
assert_not_contains output/assets/js/docs-search-index.json '"route": "posts/'

home_listing_count="$(grep -o '<li class="listing-card"' output/index.html | wc -l | tr -d ' ')"
course_listing_count="$(grep -o '<li class="listing-card"' output/course/index.html | wc -l | tr -d ' ')"
[[ "$home_listing_count" == "6" ]] || fail "expected 6 homepage lesson cards, found $home_listing_count"
[[ "$course_listing_count" == "6" ]] || fail "expected 6 course lesson cards, found $course_listing_count"

if rg -n '/blog/|>Blog<' output --glob '*.html' --glob '*.xml' --glob '*.txt' --glob '*.json'; then
	fail "generated output still contains legacy blog URLs or labels"
fi

rendered_code_blocks="$(find output/course -name 'index.html' -type f -exec grep -o '<pre><code' {} + | wc -l | tr -d ' ')"
[[ "$rendered_code_blocks" -ge 300 ]] || fail "expected at least 300 rendered lesson code blocks, found $rendered_code_blocks"

python3 scripts/check-seo.py output

printf 'Python Course site contract passed (%s lessons, %s words, %s code blocks)\n' "$post_count" "$course_word_count" "$rendered_code_blocks"
