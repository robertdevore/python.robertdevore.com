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

bash -n scripts/build.sh scripts/build-parallel.sh scripts/test-site.sh scripts/validate-generated-output.sh

assert_path assets/sitekit/sitekit.css
assert_path assets/sitekit/sitekit.js
assert_path assets/sitekit/fonts/DepartureMono-Regular.woff2
assert_path assets/sitekit/fonts/DepartureMono-LICENSE.txt

post_count="$(find content/posts -maxdepth 1 -name '*.md' -type f | wc -l | tr -d ' ')"
[[ "$post_count" == "20" ]] || fail "expected 20 course lessons, found $post_count"

course_word_count="$(wc -w content/posts/*.md | tail -1 | awk '{print $1}')"
[[ "$course_word_count" -ge 40000 ]] || fail "course content looks incomplete: $course_word_count words"

SITE_URL=https://python.robertdevore.com bash scripts/build.sh

assert_path output/index.html
assert_path output/about/index.html
assert_path output/sample-page/index.html
assert_path output/blog/index.html
assert_path output/blog/python-setup-and-ides/index.html
assert_path output/blog/python-syntax-and-data-types/index.html
assert_path output/blog/syntax-and-data-types/index.html
assert_path output/blog/course-conclusion-from-python-novice-to-professional-developer/index.html
assert_path output/feed/index.xml
assert_path output/sitemap.xml
assert_path output/robots.txt
assert_path output/llms.txt
assert_path output/CNAME
assert_path output/assets/sitekit/fonts/DepartureMono-Regular.woff2
assert_path output/assets/js/docs-search-index.json

assert_contains output/index.html 'Learn Python. Build real things.'
assert_contains output/index.html 'class="course-stats"'
assert_contains output/blog/python-syntax-and-data-types/index.html '1.2. Syntax &amp; Data Types'
assert_contains output/blog/syntax-and-data-types/index.html '1.3. Control Flow (If, For, While)'
assert_contains output/blog/python-setup-and-ides/index.html 'class="docs-shell"'
assert_contains output/blog/python-setup-and-ides/index.html 'href="#installing-python"'
assert_contains output/about/index.html 'Kujo SSG and SiteKit'
assert_contains output/assets/css/style.css 'Departure Mono'
assert_contains output/assets/css/style.css '#3776ab'
assert_contains output/assets/css/style.css '#ffd343'
assert_contains output/robots.txt 'Allow: /'
assert_contains output/sitemap.xml 'https://python.robertdevore.com/blog/course-conclusion-from-python-novice-to-professional-developer/'
assert_contains output/CNAME 'python.robertdevore.com'

printf 'Python Course site contract passed (%s lessons, %s words)\n' "$post_count" "$course_word_count"
