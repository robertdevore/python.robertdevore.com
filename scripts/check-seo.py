#!/usr/bin/env python3
"""Validate the generated Python Course discovery and sharing contract."""

from __future__ import annotations

import json
import struct
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


BASE_URL = "https://python.robertdevore.com"
OUTPUT = Path(sys.argv[1] if len(sys.argv) > 1 else "output")


class HeadParser(HTMLParser):
	def __init__(self) -> None:
		super().__init__(convert_charrefs=True)
		self.in_title = False
		self.in_json_ld = False
		self.title_parts: list[str] = []
		self.json_ld_parts: list[str] = []
		self.meta_name: dict[str, str] = {}
		self.meta_property: dict[str, str] = {}
		self.links: list[dict[str, str]] = []

	def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
		values = {key: value or "" for key, value in attrs}
		if tag == "title":
			self.in_title = True
		elif tag == "meta":
			if values.get("name"):
				self.meta_name[values["name"]] = values.get("content", "")
			if values.get("property"):
				self.meta_property[values["property"]] = values.get("content", "")
		elif tag == "link":
			self.links.append(values)
		elif tag == "script" and values.get("type") == "application/ld+json":
			self.in_json_ld = True

	def handle_endtag(self, tag: str) -> None:
		if tag == "title":
			self.in_title = False
		elif tag == "script" and self.in_json_ld:
			self.in_json_ld = False

	def handle_data(self, data: str) -> None:
		if self.in_title:
			self.title_parts.append(data)
		if self.in_json_ld:
			self.json_ld_parts.append(data)

	@property
	def title(self) -> str:
		return "".join(self.title_parts).strip()

	@property
	def schema(self) -> dict:
		return json.loads("".join(self.json_ld_parts))

	def link(self, rel: str, type_: str | None = None) -> dict[str, str] | None:
		for link in self.links:
			if rel not in link.get("rel", "").split():
				continue
			if type_ is not None and link.get("type") != type_:
				continue
			return link
		return None


def fail(message: str) -> None:
	raise AssertionError(message)


def canonical_url(path: Path) -> str:
	relative = path.relative_to(OUTPUT).as_posix()
	if relative == "index.html":
		return f"{BASE_URL}/"
	if not relative.endswith("/index.html"):
		fail(f"canonical route is not an index page: {path}")
	return f"{BASE_URL}/{relative.removesuffix('index.html')}"


def social_image_url(path: Path) -> str:
	relative = path.relative_to(OUTPUT).as_posix()
	if relative == "index.html":
		card_id = "home"
	elif relative == "404.html":
		card_id = "404"
	else:
		card_id = relative.removesuffix("/index.html").replace("/", "-")
	return f"{BASE_URL}/assets/images/social/{card_id}.png"


def parse_html(path: Path) -> HeadParser:
	parser = HeadParser()
	parser.feed(path.read_text(encoding="utf-8"))
	return parser


def assert_png_dimensions(path: Path, expected: tuple[int, int]) -> None:
	data = path.read_bytes()[:24]
	if data[:8] != b"\x89PNG\r\n\x1a\n":
		fail(f"social image is not a PNG: {path}")
	width, height = struct.unpack(">II", data[16:24])
	if (width, height) != expected:
		fail(f"social image dimensions are {width}x{height}, expected {expected[0]}x{expected[1]}")


def main() -> None:
	if not OUTPUT.is_dir():
		fail(f"output directory does not exist: {OUTPUT}")

	canonical_files = [
		path for path in sorted(OUTPUT.glob("**/index.html"))
		if not path.relative_to(OUTPUT).as_posix().startswith(("blog/", "page/"))
	]
	if len(canonical_files) != 26:
		fail(f"expected 26 canonical HTML routes, found {len(canonical_files)}")

	titles: dict[str, Path] = {}
	canonicals: set[str] = set()
	lesson_urls: set[str] = set()
	for path in canonical_files:
		page = parse_html(path)
		expected_canonical = canonical_url(path)
		canonical = page.link("canonical")
		if not canonical or canonical.get("href") != expected_canonical:
			fail(f"canonical mismatch in {path}: {canonical}")
		canonicals.add(expected_canonical)

		if not page.title or page.title in titles:
			fail(f"missing or duplicate title in {path}: {page.title!r}")
		titles[page.title] = path
		for name in ("description", "keywords", "author", "robots"):
			if not page.meta_name.get(name):
				fail(f"missing meta {name} in {path}")
		if "index" not in page.meta_name["robots"] or "follow" not in page.meta_name["robots"]:
			fail(f"route is not indexable in {path}")
		if "Static Site Generator" in page.meta_name["keywords"]:
			fail(f"starter keywords leaked into {path}")

		for prop in ("og:title", "og:description", "og:url", "og:type", "og:site_name", "og:locale", "og:image", "og:image:secure_url", "og:image:type", "og:image:width", "og:image:height", "og:image:alt"):
			if not page.meta_property.get(prop):
				fail(f"missing {prop} in {path}")
		if page.meta_property["og:url"] != expected_canonical:
			fail(f"Open Graph URL mismatch in {path}")
		expected_social_image = social_image_url(path)
		if page.meta_property["og:image"] != expected_social_image:
			fail(f"social image mismatch in {path}")
		for name in ("twitter:card", "twitter:title", "twitter:description", "twitter:image", "twitter:image:alt"):
			if not page.meta_name.get(name):
				fail(f"missing {name} in {path}")
		if page.meta_name["twitter:card"] != "summary_large_image":
			fail(f"unexpected Twitter card type in {path}")
		if page.meta_name["twitter:image"] != expected_social_image:
			fail(f"Twitter social image mismatch in {path}")
		card_path = OUTPUT / urlparse(expected_social_image).path.lstrip("/")
		assert_png_dimensions(card_path, (1200, 630))

		feed = page.link("alternate", "application/rss+xml")
		if not feed or feed.get("href") != f"{BASE_URL}/feed/index.xml":
			fail(f"RSS autodiscovery mismatch in {path}")

		schema = page.schema
		if schema.get("@context") != "https://schema.org":
			fail(f"invalid JSON-LD context in {path}")
		relative = path.relative_to(OUTPUT).as_posix()
		if relative == "index.html":
			types = {node.get("@type") for node in schema.get("@graph", [])}
			if not {"WebSite", "Course", "Organization", "Person"}.issubset(types):
				fail("homepage JSON-LD graph is incomplete")
			course = next(node for node in schema["@graph"] if node.get("@type") == "Course")
			if course.get("provider", {}).get("@type") != "Organization":
				fail("homepage Course schema requires an Organization provider")
		elif relative == "about/index.html":
			if schema.get("@type") != "AboutPage":
				fail("about page must use AboutPage schema")
		elif relative == "course/index.html" or relative.startswith("course/page/"):
			if schema.get("@type") != "CollectionPage" or schema.get("mainEntity", {}).get("@type") != "Course":
				fail(f"course listing schema is incomplete in {path}")
			if schema["mainEntity"].get("provider", {}).get("@type") != "Organization":
				fail(f"course provider schema is incomplete in {path}")
		else:
			lesson_urls.add(expected_canonical)
			if schema.get("@type") != "Article":
				fail(f"lesson must use Article schema in {path}")
			for key in ("headline", "description", "url", "image", "author", "publisher", "datePublished", "dateModified", "learningResourceType", "isPartOf"):
				if not schema.get(key):
					fail(f"lesson schema missing {key} in {path}")

	if len(lesson_urls) != 20:
		fail(f"expected 20 lesson URLs, found {len(lesson_urls)}")

	page_404 = parse_html(OUTPUT / "404.html")
	if "noindex" not in page_404.meta_name.get("robots", ""):
		fail("404 page must be noindex")
	if page_404.link("canonical", None).get("href") != f"{BASE_URL}/404.html":
		fail("404 canonical is incorrect")
	if page_404.meta_property.get("og:image") != social_image_url(OUTPUT / "404.html"):
		fail("404 social image is incorrect")
	assert_png_dimensions(OUTPUT / "assets/images/social/404.png", (1200, 630))

	social_pngs = sorted((OUTPUT / "assets/images/social").glob("*.png"))
	if len(social_pngs) != 27:
		fail(f"expected 27 page-specific social images, found {len(social_pngs)}")

	sitemap_root = ET.parse(OUTPUT / "sitemap.xml").getroot()
	namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
	sitemap_urls = [node.text or "" for node in sitemap_root.findall("sm:url/sm:loc", namespace)]
	if len(sitemap_urls) != len(set(sitemap_urls)):
		fail("sitemap contains duplicate URLs")
	if set(sitemap_urls) != canonicals:
		missing = sorted(canonicals - set(sitemap_urls))
		extra = sorted(set(sitemap_urls) - canonicals)
		fail(f"sitemap mismatch; missing={missing}, extra={extra}")
	if any("/blog/" in url or "/sample-page/" in url or "/page/" in url and "/course/page/" not in url for url in sitemap_urls):
		fail("sitemap contains a legacy or duplicate route")

	robots = (OUTPUT / "robots.txt").read_text(encoding="utf-8")
	for directive in ("User-agent: *", "Allow: /", f"Sitemap: {BASE_URL}/sitemap.xml"):
		if directive not in robots:
			fail(f"robots.txt missing {directive}")
	if "Disallow: /" in robots:
		fail("robots.txt blocks public crawling")

	feed_path = OUTPUT / "feed/index.xml"
	feed_text = feed_path.read_text(encoding="utf-8")
	feed_root = ET.fromstring(feed_text)
	channel = feed_root.find("channel")
	if channel is None:
		fail("RSS channel is missing")
	atom_self = channel.find("{http://www.w3.org/2005/Atom}link")
	if atom_self is None or atom_self.get("href") != f"{BASE_URL}/feed/index.xml" or atom_self.get("rel") != "self":
		fail("RSS atom:self link is missing or invalid")
	items = channel.findall("item")
	feed_urls = [item.findtext("link", "") for item in items]
	if len(items) != 20 or set(feed_urls) != lesson_urls:
		fail("RSS feed does not contain the complete 20-lesson course")
	if "&amp;apos;" in feed_text:
		fail("RSS descriptions contain double-escaped apostrophes")

	llms = (OUTPUT / "llms.txt").read_text(encoding="utf-8")
	for heading in ("# Python Course", "## Course", "## Lessons", "## Pages", "## Feeds and discovery", "## Author"):
		if heading not in llms:
			fail(f"llms.txt missing {heading}")
	for url in lesson_urls:
		if url not in llms:
			fail(f"llms.txt missing lesson URL: {url}")
	if "/blog/" in llms or "/sample-page/" in llms:
		fail("llms.txt contains a legacy route")

	legacy_artifacts = list(OUTPUT.glob("blog/**/index.html")) + list(OUTPUT.glob("page/**/index.html"))
	if legacy_artifacts:
		fail("generated output contains legacy redirect artifacts managed at the Cloudflare edge")

	print(f"SEO discovery contract passed ({len(canonical_files)} canonical routes, {len(lesson_urls)} lessons, {len(items)} feed items)")


if __name__ == "__main__":
	try:
		main()
	except (AssertionError, json.JSONDecodeError, ET.ParseError) as error:
		print(f"FAIL: {error}", file=sys.stderr)
		sys.exit(1)
