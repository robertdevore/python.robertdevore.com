#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOWL_BIN="${HOWL_BIN:-howl}"
OUT_DIR="$REPO_ROOT/assets/images/social"

cd "$REPO_ROOT"

if [[ "$HOWL_BIN" == */* ]]; then
	[[ -x "$HOWL_BIN" ]] || { printf 'Howl is not executable: %s\n' "$HOWL_BIN" >&2; exit 1; }
elif ! command -v "$HOWL_BIN" >/dev/null 2>&1; then
	printf 'Howl was not found. Set HOWL_BIN to the Howl launcher.\n' >&2
	exit 1
fi

"$HOWL_BIN" validate --manifest "$REPO_ROOT/howl.json"
"$HOWL_BIN" render --manifest "$REPO_ROOT/howl.json" --out "$OUT_DIR" --format svg

# Howl's social layout currently carries Kujolang.ai chrome. Apply the Python
# Course brand and remove overlays that obscure this site's background art.
while IFS= read -r svg; do
	perl -0pi -e 's~<rect width="1200" height="630" fill="url\(#wash\)"/>\n~~g; s~<rect width="1200" height="630" filter="url\(#grain\)" opacity="\.7"/>\n~~g; s~KUJOLANG\.AI  //  PYTHON COURSE~PYTHON COURSE~g; s~<rect x="78" y="570" width="84" height="4" fill="#111"/>\n~~g' "$svg"
done < <(find "$OUT_DIR" -maxdepth 1 -type f -name '*.svg' -print | sort)

if command -v rsvg-convert >/dev/null 2>&1; then
	while IFS= read -r svg; do
		png="${svg%.svg}.png"
		rsvg-convert --width 1200 --height 630 --output "$png" "$svg"
	done < <(find "$OUT_DIR" -maxdepth 1 -type f -name '*.svg' -print | sort)
elif command -v magick >/dev/null 2>&1; then
	while IFS= read -r svg; do
		png="${svg%.svg}.png"
		magick -background none "$svg" -resize 1200x630! "$png"
	done < <(find "$OUT_DIR" -maxdepth 1 -type f -name '*.svg' -print | sort)
elif command -v sips >/dev/null 2>&1; then
	find "$OUT_DIR" -maxdepth 1 -type f -name '*.svg' -print0 | \
		xargs -0 -n 1 -P 4 sh -c 'svg="$1"; sips -s format png "$svg" --out "${svg%.svg}.png" >/dev/null' _
else
	printf 'No SVG-to-PNG converter found (rsvg-convert, magick, or sips).\n' >&2
	exit 1
fi

expected="$(python3 -c 'import json; print(len(json.load(open("howl.json"))["cards"]))')"
svg_count="$(find "$OUT_DIR" -maxdepth 1 -type f -name '*.svg' | wc -l | tr -d ' ')"
png_count="$(find "$OUT_DIR" -maxdepth 1 -type f -name '*.png' | wc -l | tr -d ' ')"

[[ "$svg_count" == "$expected" ]] || { printf 'Expected %s SVG cards, found %s.\n' "$expected" "$svg_count" >&2; exit 1; }
[[ "$png_count" == "$expected" ]] || { printf 'Expected %s PNG cards, found %s.\n' "$expected" "$png_count" >&2; exit 1; }

printf 'Rendered %s social cards as SVG and PNG.\n' "$expected"
