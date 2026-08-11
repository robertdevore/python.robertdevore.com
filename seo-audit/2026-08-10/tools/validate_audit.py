#!/usr/bin/env python3
"""Validate completeness and internal consistency of the audit bundle."""

from __future__ import annotations

import csv
import json
from pathlib import Path


AUDIT = Path(__file__).resolve().parents[1]
UNAVAILABLE = "NOT AVAILABLE — DATA ACCESS REQUIRED"

required = [
    "executive-summary.md", "methodology.md", "research-sources.md", "data-availability.md",
    "site-inventory.csv", "baseline.csv", "baseline-summary.json", "after.csv", "after-summary.json",
    "metadata-audit.csv", "content-audit.csv", "keyword-map.csv", "search-rankings.csv",
    "ai-search-benchmark.csv", "internal-links.csv", "external-links.csv", "broken-links.csv",
    "schema-audit.csv", "indexability.csv", "crawlability.csv", "crawler-access.csv",
    "performance.csv", "image-audit.csv", "redirects.csv", "issues.csv", "changes.md",
    "before-after.md", "unresolved.md", "recommendations.md",
]
for name in required:
    path = AUDIT / name
    assert path.is_file() and path.stat().st_size > 0, f"missing or empty artifact: {name}"


def rows(name: str) -> list[dict[str, str]]:
    with (AUDIT / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


baseline = rows("baseline.csv")
after = rows("after.csv")
assert len(baseline) == len(after) == 26
assert {row["url"] for row in baseline} == {row["url"] for row in after}
assert all(row["canonical"] == row["url"] for row in baseline + after)
assert all(row["production_status"] == "200" for row in baseline + after)

baseline_summary = json.loads((AUDIT / "baseline-summary.json").read_text())
after_summary = json.loads((AUDIT / "after-summary.json").read_text())
assert baseline_summary["broken_internal_links"] == 3
assert after_summary["broken_internal_links"] == 0
for key in ("missing_titles", "duplicate_titles", "missing_descriptions", "duplicate_descriptions", "canonical_mismatches", "h1_issues", "orphans", "invalid_schema_pages", "sitemap_mismatches"):
    assert after_summary[key] == 0, f"after summary regression: {key}"

assert len(rows("site-inventory.csv")) == 52
assert len(rows("content-audit.csv")) == 26
assert len(rows("keyword-map.csv")) == 26
assert len(rows("schema-audit.csv")) == 52
assert len(rows("image-audit.csv")) == 52
assert len(rows("performance.csv")) == 6
assert len(rows("crawler-access.csv")) == 9
assert len(rows("ai-search-benchmark.csv")) == 10
assert len(rows("issues.csv")) >= 8
assert len(rows("redirects.csv")) >= 7

for name in ("data-availability.md", "unresolved.md"):
    assert UNAVAILABLE in (AUDIT / name).read_text(encoding="utf-8")
for row in rows("ai-search-benchmark.csv"):
    assert row["evidence"] == UNAVAILABLE and row["limitations"] == UNAVAILABLE

baseline_output = AUDIT / "raw/baseline/output"
assert len(list(baseline_output.glob("**/index.html"))) == 26
assert (baseline_output / "sitemap.xml").is_file()
assert (AUDIT / "raw/baseline/commit.txt").read_text().strip() == "dcd0ed0fd949dad071e773d9ef2f2703311319cf"

production_summary = json.loads((AUDIT / "raw/production/after-summary.json").read_text())
assert production_summary == {
    "deployment_run": 31464566449,
    "cloudflare_bulk_redirect_list_id": "4ecb2aecd75a48aeb27a4bd575b0198b",
    "cloudflare_bulk_redirect_rule_id": "1a0ee52fa1654bd7ae652f5987e89cea",
    "cloudflare_redirect_status": 301,
    "cloudflare_query_preservation_verified": True,
    "canonical_urls_verified": 26,
    "canonical_failures": 0,
    "legacy_redirects_verified": 24,
    "legacy_redirect_failures": 0,
    "discovery_assets_verified": 5,
    "status": "pass",
}
assert len(rows("raw/production/canonical-after.csv")) == 26
assert len(rows("raw/production/legacy-redirects-after.csv")) == 24
assert all(row["status"] == "301" and row["location"] == row["target"] and row["result"] == "pass"
           for row in rows("raw/production/legacy-redirects-after.csv"))

print("SEO audit bundle validation passed")
