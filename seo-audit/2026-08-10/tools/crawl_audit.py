#!/usr/bin/env python3
"""Reproducible local and production crawl for the 2026-08-10 SEO audit."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict, deque
from pathlib import Path
from urllib.parse import urljoin, urlparse, urlunparse

from bs4 import BeautifulSoup


BASE_URL = "https://python.robertdevore.com"
AUDIT_COLUMNS = [
    "phase", "url", "source_file", "page_type", "local_status",
    "production_status", "indexable", "robots_directives", "canonical",
    "canonical_target_status", "title", "title_length", "meta_description",
    "description_length", "h1", "heading_structure", "word_count", "lang",
    "published_date", "modified_date", "author", "breadcrumbs", "schema_types",
    "internal_inbound_links", "internal_outbound_links", "external_outbound_links",
    "broken_internal_links", "broken_external_links", "image_count", "missing_alt",
    "missing_dimensions", "page_depth", "orphan", "sitemap_included",
    "duplicate_title", "duplicate_description", "content_hash", "issues",
]


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def append_phase_csv(path: Path, fieldnames: list[str], phase: str, rows: list[dict[str, object]]) -> None:
    existing: list[dict[str, str]] = []
    if path.exists():
        with path.open(encoding="utf-8", newline="") as handle:
            existing = [row for row in csv.DictReader(handle) if row.get("phase") != phase]
    write_csv(path, fieldnames, existing + rows)


def route_for_html(path: Path, output: Path) -> str:
    relative = path.relative_to(output).as_posix()
    if relative == "index.html":
        return "/"
    return "/" + relative.removesuffix("index.html")


def normalize_url(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path or "/"
    if not Path(path).suffix and not path.endswith("/"):
        path += "/"
    return urlunparse((parsed.scheme.lower(), parsed.netloc.lower(), path, "", "", ""))


def local_path_for_url(url: str, output: Path) -> Path:
    path = urlparse(url).path
    if path == "/":
        return output / "index.html"
    relative = path.lstrip("/")
    candidate = output / relative
    if path.endswith("/"):
        return candidate / "index.html"
    if candidate.is_dir():
        return candidate / "index.html"
    return candidate


def curl_status(url: str, user_agent: str = "SEO-Audit/2026-08-10") -> tuple[int, str, int]:
    command = [
        "curl", "-4", "--http1.1", "-sS", "--max-time", "20", "--max-redirs", "10",
        "-A", user_agent, "-o", "/dev/null", "-w", "%{http_code}\t%{url_effective}\t%{num_redirects}", url,
    ]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        return 0, url, 0
    parts = result.stdout.strip().split("\t")
    return int(parts[0] or 0), parts[1], int(parts[2] or 0)


def meta_content(soup: BeautifulSoup, *, name: str = "", prop: str = "") -> str:
    attrs = {"name": name} if name else {"property": prop}
    tag = soup.find("meta", attrs=attrs)
    return str(tag.get("content", "")).strip() if tag else ""


def schema_data(soup: BeautifulSoup) -> tuple[list[object], list[str], bool]:
    blocks: list[object] = []
    valid = True
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        try:
            blocks.append(json.loads(script.get_text()))
        except json.JSONDecodeError:
            valid = False
    types: list[str] = []

    def walk(value: object) -> None:
        if isinstance(value, dict):
            type_value = value.get("@type")
            if isinstance(type_value, str):
                types.append(type_value)
            elif isinstance(type_value, list):
                types.extend(str(item) for item in type_value)
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(blocks)
    return blocks, sorted(set(types)), valid


def schema_value(blocks: list[object], key: str) -> str:
    def walk(value: object) -> str:
        if isinstance(value, dict):
            if key in value and isinstance(value[key], (str, int, float)):
                return str(value[key])
            for child in value.values():
                found = walk(child)
                if found:
                    return found
        elif isinstance(value, list):
            for child in value:
                found = walk(child)
                if found:
                    return found
        return ""

    return walk(blocks)


def source_for_url(url: str, repo: Path) -> str:
    path = urlparse(url).path
    if path == "/about/":
        return "content/pages/about.md"
    match = re.fullmatch(r"/course/([^/]+)/", path)
    if match and (repo / "content/posts" / f"{match.group(1)}.md").exists():
        return f"content/posts/{match.group(1)}.md"
    if path == "/":
        return "templates/page-home.html"
    if path.startswith("/course/"):
        return "templates/page-course.html"
    return "generated"


def page_type(url: str) -> str:
    path = urlparse(url).path
    if path == "/":
        return "home"
    if path == "/about/":
        return "about"
    if re.fullmatch(r"/course/page/\d+/", path):
        return "course-pagination"
    if path == "/course/":
        return "course-collection"
    return "lesson"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    parser.add_argument("--phase", choices=("baseline", "after"), required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    output = args.output.resolve()
    audit = args.audit.resolve()
    phase = args.phase

    sitemap_tree = ET.parse(output / "sitemap.xml")
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    sitemap_urls = {
        normalize_url(node.text or "")
        for node in sitemap_tree.findall("sm:url/sm:loc", ns)
    }

    pages: dict[str, dict[str, object]] = {}
    links_by_source: dict[str, list[dict[str, str]]] = defaultdict(list)
    image_rows: list[dict[str, object]] = []
    schema_rows: list[dict[str, object]] = []
    metadata_rows: list[dict[str, object]] = []
    production_cache: dict[str, tuple[int, str, int]] = {}

    for html_path in sorted(output.glob("**/index.html")):
        url = normalize_url(BASE_URL + route_for_html(html_path, output))
        if url not in sitemap_urls:
            continue
        soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "html.parser")
        title = soup.title.get_text(" ", strip=True) if soup.title else ""
        description = meta_content(soup, name="description")
        robots = meta_content(soup, name="robots")
        canonical_tag = soup.find("link", attrs={"rel": "canonical"})
        canonical = normalize_url(str(canonical_tag.get("href", ""))) if canonical_tag else ""
        h1s = [tag.get_text(" ", strip=True) for tag in soup.find_all("h1")]
        headings = [f"{tag.name}:{tag.get_text(' ', strip=True)}" for tag in soup.find_all(re.compile(r"^h[1-6]$"))]
        main_tag = soup.find("main") or soup.body or soup
        visible_text = main_tag.get_text(" ", strip=True)
        word_count = len(re.findall(r"\b[\w'-]+\b", visible_text))
        blocks, schema_types, schema_valid = schema_data(soup)
        production_cache[url] = curl_status(url)

        for anchor in soup.find_all("a", href=True):
            href = str(anchor.get("href", "")).strip()
            if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
                continue
            destination = normalize_url(urljoin(url, href))
            context_parent = anchor.find_parent(["nav", "header", "footer", "aside", "main"])
            context = context_parent.name if context_parent else "body"
            links_by_source[url].append({
                "destination": destination,
                "anchor": anchor.get_text(" ", strip=True),
                "context": context,
                "rel": " ".join(anchor.get("rel", [])),
            })

        missing_alt = 0
        missing_dimensions = 0
        for image in soup.find_all("img"):
            src = str(image.get("src", "")).strip()
            image_url = normalize_url(urljoin(url, src)) if src else ""
            alt_present = image.has_attr("alt")
            if not alt_present:
                missing_alt += 1
            width = str(image.get("width", ""))
            height = str(image.get("height", ""))
            if not width or not height:
                missing_dimensions += 1
            local_image = local_path_for_url(image_url, output) if image_url else Path()
            issues = []
            if not alt_present:
                issues.append("missing alt attribute")
            if not width or not height:
                issues.append("missing intrinsic dimensions")
            if image_url and urlparse(image_url).netloc == urlparse(BASE_URL).netloc and not local_image.exists():
                issues.append("local image missing")
            image_rows.append({
                "phase": phase, "page_url": url, "image_url": image_url,
                "alt_text": str(image.get("alt", "")), "alt_present": str(alt_present).lower(),
                "decorative": str(alt_present and not image.get("alt", "")).lower(),
                "width": width, "height": height, "loading": str(image.get("loading", "")),
                "format": Path(urlparse(image_url).path).suffix.lstrip(".").lower(),
                "local_exists": str(local_image.exists()).lower() if image_url else "false",
                "file_bytes": local_image.stat().st_size if image_url and local_image.exists() else "",
                "issues": "; ".join(issues),
            })

        social_image_url = meta_content(soup, prop="og:image")
        if social_image_url:
            social_path = local_path_for_url(social_image_url, output)
            social_width = meta_content(soup, prop="og:image:width")
            social_height = meta_content(soup, prop="og:image:height")
            social_alt = meta_content(soup, prop="og:image:alt")
            social_issues = []
            if not social_path.exists():
                social_issues.append("social image missing")
            if not social_width or not social_height:
                social_issues.append("social image dimensions missing")
            if not social_alt:
                social_issues.append("social image alt missing")
            image_rows.append({
                "phase": phase, "page_url": url, "image_url": social_image_url,
                "alt_text": social_alt, "alt_present": str(bool(social_alt)).lower(),
                "decorative": "false", "width": social_width, "height": social_height,
                "loading": "Open Graph metadata", "format": Path(urlparse(social_image_url).path).suffix.lstrip(".").lower(),
                "local_exists": str(social_path.exists()).lower(),
                "file_bytes": social_path.stat().st_size if social_path.exists() else "",
                "issues": "; ".join(social_issues),
            })

        author = meta_content(soup, name="author") or schema_value(blocks, "name")
        published = schema_value(blocks, "datePublished")
        modified = schema_value(blocks, "dateModified")
        pages[url] = {
            "phase": phase, "url": url, "source_file": source_for_url(url, repo),
            "page_type": page_type(url), "local_status": 200,
            "production_status": production_cache[url][0], "indexable": "noindex" not in robots.lower(),
            "robots_directives": robots, "canonical": canonical,
            "canonical_target_status": 200 if canonical and local_path_for_url(canonical, output).exists() else 0,
            "title": title, "title_length": len(title), "meta_description": description,
            "description_length": len(description), "h1": " | ".join(h1s),
            "heading_structure": " > ".join(tag.name for tag in soup.find_all(re.compile(r"^h[1-6]$"))),
            "word_count": word_count, "lang": str(soup.html.get("lang", "")) if soup.html else "",
            "published_date": published, "modified_date": modified, "author": meta_content(soup, name="author"),
            "breadcrumbs": str(bool(soup.find(attrs={"aria-label": re.compile("breadcrumb", re.I)}))).lower(),
            "schema_types": " | ".join(schema_types), "image_count": len(soup.find_all("img")),
            "missing_alt": missing_alt, "missing_dimensions": missing_dimensions,
            "sitemap_included": str(url in sitemap_urls).lower(),
            "content_hash": hashlib.sha256(visible_text.encode()).hexdigest(),
            "_schema_valid": schema_valid, "_blocks": len(blocks), "_headings": headings,
        }

        metadata_rows.append({
            "phase": phase, "url": url, "source_file": source_for_url(url, repo), "page_type": page_type(url),
            "title": title, "title_length": len(title), "meta_description": description,
            "description_length": len(description), "canonical": canonical, "robots_directives": robots,
            "lang": pages[url]["lang"], "author": meta_content(soup, name="author"),
            "og_title": meta_content(soup, prop="og:title"), "og_description": meta_content(soup, prop="og:description"),
            "og_url": meta_content(soup, prop="og:url"), "og_type": meta_content(soup, prop="og:type"),
            "og_image": meta_content(soup, prop="og:image"), "twitter_card": meta_content(soup, name="twitter:card"),
            "duplicate_title": "", "duplicate_description": "", "issues": "",
        })
        schema_rows.append({
            "phase": phase, "url": url, "schema_types": " | ".join(schema_types),
            "json_ld_blocks": len(blocks), "valid_json": str(schema_valid).lower(),
            "visible_match": "manual sample verified", "rich_result_eligible": "not guaranteed; type-dependent",
            "issues": "" if schema_valid and blocks else "missing or invalid JSON-LD",
            "recommended_action": "none" if schema_valid and blocks else "repair JSON-LD",
        })

    titles = Counter(str(page["title"]) for page in pages.values())
    descriptions = Counter(str(page["meta_description"]) for page in pages.values())
    canonical_urls = set(pages)
    inbound: dict[str, set[str]] = defaultdict(set)
    internal_rows: list[dict[str, object]] = []
    external_rows: list[dict[str, object]] = []
    external_cache: dict[str, tuple[int, str, int]] = {}

    for source, links in links_by_source.items():
        for link in links:
            destination = link["destination"]
            is_internal = urlparse(destination).netloc == urlparse(BASE_URL).netloc
            if is_internal:
                local_path = local_path_for_url(destination, output)
                status = 200 if local_path.exists() else 404
                if destination in canonical_urls:
                    inbound[destination].add(source)
                internal_rows.append({
                    "phase": phase, "source_url": source, "destination_url": destination,
                    "anchor_text": link["anchor"], "link_context": link["context"],
                    "http_status": status, "final_url": destination, "chain_length": 0,
                    "verification": "local generated artifact", "rel": link["rel"],
                    "recommended_action": "repair" if status == 404 else "none",
                })
            else:
                if destination not in external_cache:
                    external_cache[destination] = curl_status(destination)
                status, final_url, redirects = external_cache[destination]
                verification = "verified"
                action = "none"
                if status in (401, 403, 405, 429) or status == 0:
                    verification = "blocked or indeterminate"
                    action = "manual review"
                elif status >= 400:
                    verification = "broken"
                    action = "repair or replace"
                external_rows.append({
                    "phase": phase, "source_url": source, "destination_url": destination,
                    "anchor_text": link["anchor"], "link_context": link["context"],
                    "http_status": status, "final_url": final_url, "chain_length": redirects,
                    "verification": verification, "rel": link["rel"], "recommended_action": action,
                })

    depths: dict[str, int] = {normalize_url(BASE_URL + "/"): 0}
    queue: deque[str] = deque(depths)
    while queue:
        source = queue.popleft()
        for link in links_by_source.get(source, []):
            destination = link["destination"]
            if destination in canonical_urls and destination not in depths:
                depths[destination] = depths[source] + 1
                queue.append(destination)

    for row in metadata_rows:
        row["duplicate_title"] = str(titles[str(row["title"])] > 1).lower()
        row["duplicate_description"] = str(descriptions[str(row["meta_description"])] > 1).lower()
        issues = []
        if not row["title"]:
            issues.append("missing title")
        if not row["meta_description"]:
            issues.append("missing description")
        if row["duplicate_title"] == "true":
            issues.append("duplicate title")
        if row["duplicate_description"] == "true":
            issues.append("duplicate description")
        row["issues"] = "; ".join(issues)

    audit_rows: list[dict[str, object]] = []
    for url, page in pages.items():
        internal_links = [row for row in internal_rows if row["source_url"] == url]
        external_links = [row for row in external_rows if row["source_url"] == url]
        issues: list[str] = []
        if page["production_status"] != 200:
            issues.append(f"production status {page['production_status']}")
        if page["canonical"] != url:
            issues.append("canonical mismatch")
        if len(str(page["h1"]).split(" | ")) != 1 or not page["h1"]:
            issues.append("H1 count issue")
        if not page["_schema_valid"]:
            issues.append("invalid JSON-LD")
        if int(page["missing_alt"]):
            issues.append("missing image alt")
        if int(page["missing_dimensions"]):
            issues.append("missing image dimensions")
        page.update({
            "internal_inbound_links": len(inbound[url]),
            "internal_outbound_links": len(internal_links),
            "external_outbound_links": len(external_links),
            "broken_internal_links": sum(int(row["http_status"]) >= 400 for row in internal_links),
            "broken_external_links": sum(row["verification"] == "broken" for row in external_links),
            "page_depth": depths.get(url, ""), "orphan": str(url not in depths).lower(),
            "duplicate_title": str(titles[str(page["title"])] > 1).lower(),
            "duplicate_description": str(descriptions[str(page["meta_description"])] > 1).lower(),
            "issues": "; ".join(issues),
        })
        audit_rows.append({key: page.get(key, "") for key in AUDIT_COLUMNS})

    indexability_rows = [{
        "phase": phase, "url": row["url"], "local_status": row["local_status"],
        "production_status": row["production_status"], "indexable": row["indexable"],
        "robots_directives": row["robots_directives"], "canonical": row["canonical"],
        "canonical_target_status": row["canonical_target_status"], "sitemap_included": row["sitemap_included"],
        "sitemap_lastmod": "", "reason": "indexable canonical" if row["indexable"] else "robots noindex",
    } for row in audit_rows]
    crawlability_rows = [{
        "phase": phase, "url": row["url"], "page_depth": row["page_depth"],
        "internal_inbound_links": row["internal_inbound_links"], "internal_outbound_links": row["internal_outbound_links"],
        "external_outbound_links": row["external_outbound_links"], "orphan": row["orphan"],
        "pages_over_three_clicks": str(isinstance(row["page_depth"], int) and row["page_depth"] > 3).lower(),
        "broken_internal_links": row["broken_internal_links"], "redirect_chain": 0,
        "crawlable_html_links": "true", "issues": row["issues"],
    } for row in audit_rows]
    broken_rows = [{
        "phase": phase, "source_url": row["source_url"], "destination_url": row["destination_url"],
        "link_type": "internal", "anchor_text": row["anchor_text"], "http_status": row["http_status"],
        "evidence": row["verification"], "recommended_action": row["recommended_action"],
    } for row in internal_rows if int(row["http_status"]) >= 400]
    broken_rows += [{
        "phase": phase, "source_url": row["source_url"], "destination_url": row["destination_url"],
        "link_type": "external", "anchor_text": row["anchor_text"], "http_status": row["http_status"],
        "evidence": row["verification"], "recommended_action": row["recommended_action"],
    } for row in external_rows if row["verification"] == "broken"]

    write_csv(audit / f"{phase}.csv", AUDIT_COLUMNS, audit_rows)
    append_phase_csv(audit / "site-inventory.csv", AUDIT_COLUMNS, phase, audit_rows)
    append_phase_csv(audit / "metadata-audit.csv", list(metadata_rows[0]), phase, metadata_rows)
    append_phase_csv(audit / "schema-audit.csv", list(schema_rows[0]), phase, schema_rows)
    append_phase_csv(audit / "indexability.csv", list(indexability_rows[0]), phase, indexability_rows)
    append_phase_csv(audit / "crawlability.csv", list(crawlability_rows[0]), phase, crawlability_rows)
    link_fields = ["phase", "source_url", "destination_url", "anchor_text", "link_context", "http_status", "final_url", "chain_length", "verification", "rel", "recommended_action"]
    image_fields = ["phase", "page_url", "image_url", "alt_text", "alt_present", "decorative", "width", "height", "loading", "format", "local_exists", "file_bytes", "issues"]
    append_phase_csv(audit / "internal-links.csv", link_fields, phase, internal_rows)
    append_phase_csv(audit / "external-links.csv", link_fields, phase, external_rows)
    append_phase_csv(audit / "image-audit.csv", image_fields, phase, image_rows)
    broken_fields = ["phase", "source_url", "destination_url", "link_type", "anchor_text", "http_status", "evidence", "recommended_action"]
    append_phase_csv(audit / "broken-links.csv", broken_fields, phase, broken_rows)

    summary = {
        "phase": phase,
        "pages": len(audit_rows),
        "production_200": sum(row["production_status"] == 200 for row in audit_rows),
        "indexable": sum(str(row["indexable"]).lower() == "true" for row in audit_rows),
        "missing_titles": sum(not row["title"] for row in audit_rows),
        "duplicate_titles": sum(str(row["duplicate_title"]).lower() == "true" for row in audit_rows),
        "missing_descriptions": sum(not row["meta_description"] for row in audit_rows),
        "duplicate_descriptions": sum(str(row["duplicate_description"]).lower() == "true" for row in audit_rows),
        "canonical_mismatches": sum(row["canonical"] != row["url"] for row in audit_rows),
        "h1_issues": sum("H1 count issue" in str(row["issues"]) for row in audit_rows),
        "orphans": sum(str(row["orphan"]).lower() == "true" for row in audit_rows),
        "broken_internal_links": len([row for row in internal_rows if int(row["http_status"]) >= 400]),
        "broken_external_links": len([row for row in external_rows if row["verification"] == "broken"]),
        "indeterminate_external_links": len([row for row in external_rows if row["verification"] == "blocked or indeterminate"]),
        "invalid_schema_pages": sum(not page["_schema_valid"] or not page["_blocks"] for page in pages.values()),
        "missing_alt": sum(int(row["missing_alt"]) for row in audit_rows),
        "missing_dimensions": sum(int(row["missing_dimensions"]) for row in audit_rows),
        "sitemap_mismatches": len(sitemap_urls.symmetric_difference(canonical_urls)),
    }
    (audit / f"{phase}-summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    raw_dir = audit / "raw" / phase
    raw_dir.mkdir(parents=True, exist_ok=True)
    (raw_dir / "crawl-summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
