#!/usr/bin/env bash
set -euo pipefail

OUT_DIR="${1:-output}"

if [[ ! -d "$OUT_DIR" ]]; then
	echo "ERROR: output directory not found: $OUT_DIR"
	exit 1
fi

failures=0
html_count=0

record_failure() {
	echo "$1"
	failures=$((failures + 1))
}

while IFS= read -r html_file; do
	html_count=$((html_count + 1))

	if ! grep -Eqi '^<!doctype html>' "$html_file"; then
		record_failure "FAIL doctype: $html_file"
	fi

	if ! grep -Eqi '<html[^>]* lang="[^"]+"' "$html_file"; then
		record_failure "FAIL html-lang: $html_file"
	fi

	if ! grep -Eqi '<main[ >]' "$html_file"; then
		record_failure "FAIL main-landmark: $html_file"
	fi

	if grep -Eqi '<a[^>]*></a>' "$html_file"; then
		record_failure "FAIL empty-link: $html_file"
	fi

	if grep -Eqi '<img[[:space:]][^>]*>' "$html_file"; then
		if grep -Eio '<img[[:space:]][^>]*>' "$html_file" | grep -Eiv ' alt="' >/dev/null; then
			record_failure "FAIL image-alt: $html_file"
		fi
	fi

	if grep -qi 'class="skip-link"' "$html_file"; then
		if ! grep -qi 'id="main-content"' "$html_file"; then
			record_failure "FAIL skip-link-target: $html_file"
		fi
	fi

done < <(find "$OUT_DIR" -name '*.html' -type f | sort)

if [[ "$html_count" -eq 0 ]]; then
	record_failure "FAIL no-html: no HTML files found in $OUT_DIR"
fi

if [[ -f "$OUT_DIR/sitemap.xml" ]]; then
	if ! grep -q '<urlset' "$OUT_DIR/sitemap.xml"; then
		record_failure "FAIL sitemap-format: $OUT_DIR/sitemap.xml"
	fi
fi

if [[ -f "$OUT_DIR/feed/index.xml" ]]; then
	if ! grep -q '<rss' "$OUT_DIR/feed/index.xml"; then
		record_failure "FAIL rss-format: $OUT_DIR/feed/index.xml"
	fi
fi

if [[ ! -s "$OUT_DIR/.well-known/kujo-site-index.json" || ! -s "$OUT_DIR/assets/js/kujo-webmcp.js" ]]; then
	record_failure "FAIL webmcp-artifacts: index or runtime missing"
fi
if [[ -f "$OUT_DIR/index.html" ]] && [[ "$(grep -o 'data-kujo-webmcp' "$OUT_DIR/index.html" | wc -l | tr -d ' ')" != "1" ]]; then
	record_failure "FAIL webmcp-homepage: expected exactly one runtime marker"
fi
if [[ -f "$OUT_DIR/404.html" ]] && grep -q 'data-kujo-webmcp' "$OUT_DIR/404.html"; then
	record_failure "FAIL webmcp-404: runtime marker must be absent"
fi

echo "Checked HTML files: $html_count"

if [[ "$failures" -gt 0 ]]; then
	echo "Validation failed: $failures issue(s)"
	exit 1
fi

echo "Validation passed"
