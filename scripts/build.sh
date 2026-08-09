#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
KUJO_BIN="${KUJO_BIN:-kujo}"
SITE_URL="${SITE_URL:-}"

cd "$REPO_ROOT"

search_args=(
	--content content
	--output assets/js/docs-search-index.json
	--base-route course
)
build_args=("$@")

if [[ -n "$SITE_URL" ]]; then
	search_args+=(--site-url "$SITE_URL")
	build_args+=(--site-url "$SITE_URL")
fi

"$KUJO_BIN" run scripts/docs_search_index.kujo -- "${search_args[@]}"
bash scripts/build-parallel.sh auto auto "${build_args[@]}"
cp CNAME output/CNAME
bash scripts/validate-generated-output.sh output
