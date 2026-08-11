#!/usr/bin/env python3
"""Verify the deployed canonical and legacy-route contracts."""

from __future__ import annotations

import csv
import json
import subprocess
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse

from bs4 import BeautifulSoup


AUDIT = Path(__file__).resolve().parents[1]
BASE = "https://python.robertdevore.com"


def fetch(url: str, user_agent: str = "SEO-Production-Verify/2026-08-10") -> tuple[int, str, str]:
    result = subprocess.run(
        ["curl", "-4", "--http1.1", "-sS", "--max-time", "20", "-A", user_agent,
         "-w", "\n__AUDIT_STATUS__%{http_code}\n__AUDIT_URL__%{url_effective}", url],
        capture_output=True, text=True, encoding="utf-8", errors="replace", check=False,
    )
    assert result.returncode == 0, f"curl failed for {url}: {result.stderr}"
    body, trailer = result.stdout.rsplit("\n__AUDIT_STATUS__", 1)
    status_text, final_url = trailer.split("\n__AUDIT_URL__", 1)
    return int(status_text), final_url.strip(), body


def fetch_redirect(url: str, expected_location: str) -> tuple[int, str]:
    """Fetch an edge redirect without following it, allowing brief rule propagation."""
    last_result = (0, "")
    for attempt in range(4):
        result = subprocess.run(
            ["curl", "-4", "--http1.1", "-sS", "--max-time", "20", "--max-redirs", "0",
             "-H", "Cache-Control: no-cache", "-o", "/dev/null", "-w", "%{http_code}\n%{redirect_url}", url],
            capture_output=True, text=True, encoding="utf-8", errors="replace", check=False,
        )
        assert result.returncode == 0, f"curl failed for {url}: {result.stderr}"
        status_text, location = result.stdout.split("\n", 1)
        last_result = (int(status_text), location.strip())
        if last_result == (301, expected_location):
            return last_result
        if attempt < 3:
            time.sleep(1)
    return last_result


sitemap_status, _, sitemap_text = fetch(f"{BASE}/sitemap.xml")
assert sitemap_status == 200
root = ET.fromstring(sitemap_text)
ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
canonical_urls = [node.text or "" for node in root.findall("sm:url/sm:loc", ns)]
assert len(canonical_urls) == len(set(canonical_urls)) == 26

canonical_rows = []
for url in canonical_urls:
    status, final_url, body = fetch(url)
    soup = BeautifulSoup(body, "html.parser")
    canonical = soup.find("link", attrs={"rel": "canonical"})
    canonical_href = str(canonical.get("href", "")) if canonical else ""
    robots = soup.find("meta", attrs={"name": "robots"})
    robots_content = str(robots.get("content", "")) if robots else ""
    assert status == 200 and final_url == url
    assert canonical_href == url
    assert "index" in robots_content and "follow" in robots_content
    canonical_rows.append({"url": url, "status": status, "final_url": final_url, "canonical": canonical_href, "robots": robots_content, "result": "pass"})

lesson_urls = [url for url in canonical_urls if "/course/" in url and "/page/" not in url and url.rstrip("/") != f"{BASE}/course"]
redirect_map = {f"{BASE}/blog/": f"{BASE}/course/"}
for url in lesson_urls:
    slug = urlparse(url).path.rstrip("/").rsplit("/", 1)[-1]
    redirect_map[f"{BASE}/blog/{slug}/"] = url
for number in range(2, 5):
    redirect_map[f"{BASE}/page/{number}/"] = f"{BASE}/course/page/{number}/"
assert len(redirect_map) == 24

redirect_rows = []
for source, target in redirect_map.items():
    status, location = fetch_redirect(source, target)
    query_source = f"{source}?utm_source=seo-audit"
    query_target = f"{target}?utm_source=seo-audit"
    query_status, query_location = fetch_redirect(query_source, query_target)
    assert status == query_status == 301
    assert location == target and query_location == query_target
    redirect_rows.append({"source": source, "status": status, "target": target, "location": location,
                          "query_location": query_location, "result": "pass"})

for path in ("robots.txt", "sitemap.xml", "feed/index.xml", "llms.txt", "assets/images/python-course-social.png"):
    status, _, _ = fetch(f"{BASE}/{path}")
    assert status == 200, f"production discovery asset failed: {path}"

home_status, _, home_body = fetch(f"{BASE}/")
assert home_status == 200 and 'class="docs-brand" href="/"' in home_body
setup_status, _, setup_body = fetch(f"{BASE}/course/python-setup-and-ides/")
assert setup_status == 200 and "Python 3.14.6" in setup_body

fields = ["url", "status", "final_url", "canonical", "robots", "result"]
with (AUDIT / "raw/production/canonical-after.csv").open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(canonical_rows)
with (AUDIT / "raw/production/legacy-redirects-after.csv").open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=["source", "status", "target", "location", "query_location", "result"], lineterminator="\n")
    writer.writeheader()
    writer.writerows(redirect_rows)

summary = {
    "deployment_run": 31452140745,
    "cloudflare_bulk_redirect_list_id": "4ecb2aecd75a48aeb27a4bd575b0198b",
    "cloudflare_bulk_redirect_rule_id": "1a0ee52fa1654bd7ae652f5987e89cea",
    "cloudflare_redirect_status": 301,
    "cloudflare_query_preservation_verified": True,
    "canonical_urls_verified": len(canonical_rows),
    "canonical_failures": 0,
    "legacy_redirects_verified": len(redirect_rows),
    "legacy_redirect_failures": 0,
    "discovery_assets_verified": 5,
    "status": "pass",
}
(AUDIT / "raw/production/after-summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
print(json.dumps(summary, indent=2))
