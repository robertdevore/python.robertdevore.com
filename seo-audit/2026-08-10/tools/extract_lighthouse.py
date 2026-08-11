#!/usr/bin/env python3
"""Convert preserved Lighthouse JSON receipts into performance.csv."""

from __future__ import annotations

import csv
import json
from pathlib import Path


AUDIT = Path(__file__).resolve().parents[1]
RAW = AUDIT / "raw/performance"
FIELDS = [
    "phase", "url", "template", "run_date", "environment", "lighthouse_version",
    "html_bytes", "css_bytes", "js_bytes", "image_bytes", "font_bytes", "requests",
    "lcp_ms", "inp_ms", "cls", "ttfb_ms", "source", "notes",
]


def resource_bytes(items: list[dict], resource_type: str) -> int:
    return sum(int(item.get("transferSize") or 0) for item in items if item.get("resourceType") == resource_type)


rows = []
for path in sorted(RAW.glob("*.json")):
    if not path.name.startswith(("baseline-", "after-")):
        continue
    data = json.loads(path.read_text(encoding="utf-8"))
    phase, template = path.stem.split("-", 1)
    audits = data["audits"]
    requests = audits.get("network-requests", {}).get("details", {}).get("items", [])
    rows.append({
        "phase": phase,
        "url": data.get("finalDisplayedUrl", data.get("finalUrl", "")),
        "template": template,
        "run_date": data.get("fetchTime", ""),
        "environment": "local static server; Lighthouse mobile simulated throttling",
        "lighthouse_version": data.get("lighthouseVersion", ""),
        "html_bytes": resource_bytes(requests, "Document"),
        "css_bytes": resource_bytes(requests, "Stylesheet"),
        "js_bytes": resource_bytes(requests, "Script"),
        "image_bytes": resource_bytes(requests, "Image"),
        "font_bytes": resource_bytes(requests, "Font"),
        "requests": len(requests),
        "lcp_ms": round(audits.get("largest-contentful-paint", {}).get("numericValue", 0), 1),
        "inp_ms": "",
        "cls": round(audits.get("cumulative-layout-shift", {}).get("numericValue", 0), 4),
        "ttfb_ms": round(audits.get("server-response-time", {}).get("numericValue", 0), 1),
        "source": path.relative_to(AUDIT).as_posix(),
        "notes": "Lab result; INP and field Core Web Vitals require RUM/CrUX data.",
    })

with (AUDIT / "performance.csv").open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

print(json.dumps(rows, indent=2))
