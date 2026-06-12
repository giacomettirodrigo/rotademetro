#!/usr/bin/env python3
"""
blogger_to_jekyll.py
====================
Converts a Blogger XML export to Jekyll _posts files.

PRESERVES:
  - Exact URL slugs  →  no broken links, no lost SEO authority
  - Publish dates
  - Labels (tags)
  - Post content (HTML kept as-is)
  - Images referenced in posts (lists them for manual download)

USAGE:
  python3 scripts/blogger_to_jekyll.py path/to/blog-export.xml

OUTPUT:
  _posts/YYYY-MM-DD-slug.html   for each published post
  _pages/slug.html              for each page (Sobre, Contato, etc.)
  migration_report.txt          summary + image URLs to download
"""

import sys
import re
import os
from xml.etree import ElementTree as ET
from datetime import datetime
from urllib.parse import urlparse

# ── Namespaces used in Blogger XML ─────────────────────────────────────────
NS = {
    "atom":   "http://www.w3.org/2005/Atom",
    "app":    "http://purl.org/atom/app#",
    "thr":    "http://purl.org/syndication/thread/1.0",
    "georss": "http://www.georss.org/georss",
    "gd":     "http://schemas.google.com/g/2005",
}

BLOGGER_POST_KIND = "http://schemas.google.com/blogger/2008/kind#post"
BLOGGER_PAGE_KIND = "http://schemas.google.com/blogger/2008/kind#page"


def slug_from_url(url: str) -> str:
    """Extract slug from Blogger post URL, e.g. /2026/06/my-post.html → my-post"""
    path = urlparse(url).path          # /2026/06/my-post.html
    name = os.path.basename(path)      # my-post.html
    return name.replace(".html", "")   # my-post


def safe_filename(slug: str) -> str:
    slug = re.sub(r"[^\w\-]", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug


def extract_images(html: str) -> list:
    return re.findall(r'src=["\']([^"\']+)["\']', html)


def convert(xml_path: str):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    posts_dir = "_posts"
    pages_dir = "p"
    os.makedirs(posts_dir, exist_ok=True)
    os.makedirs(pages_dir, exist_ok=True)

    report_lines = []
    all_images = []
    post_count = 0
    page_count = 0
    skipped = 0

    for entry in root.findall("atom:entry", NS):

        # ── Determine kind (post vs page) ─────────────────────────────────
        kind = None
        for cat in entry.findall("atom:category", NS):
            term = cat.get("term", "")
            if term == BLOGGER_POST_KIND:
                kind = "post"
            elif term == BLOGGER_PAGE_KIND:
                kind = "page"
        if kind is None:
            skipped += 1
            continue

        # ── Published status ──────────────────────────────────────────────
        control = entry.find("app:control/app:draft", NS)
        if control is not None and control.text == "yes":
            skipped += 1
            continue  # Skip unpublished drafts (you have them as local files)

        # ── Date ──────────────────────────────────────────────────────────
        published_el = entry.find("atom:published", NS)
        if published_el is None:
            skipped += 1
            continue
        pub_str = published_el.text  # 2026-06-06T09:00:00.000-03:00
        try:
            pub_dt = datetime.fromisoformat(pub_str.replace("Z", "+00:00"))
        except Exception:
            skipped += 1
            continue

        # ── Title ─────────────────────────────────────────────────────────
        title_el = entry.find("atom:title", NS)
        title = title_el.text if title_el is not None else "Untitled"
        title = title.replace('"', '\\"')

        # ── Content ───────────────────────────────────────────────────────
        content_el = entry.find("atom:content", NS)
        content = content_el.text if content_el is not None else ""

        # ── Labels ────────────────────────────────────────────────────────
        labels = []
        for cat in entry.findall("atom:category", NS):
            scheme = cat.get("scheme", "")
            if "ns1.0" in scheme or "blogger.com" not in scheme.lower():
                term = cat.get("term", "")
                if term and "schemas.google.com" not in term:
                    labels.append(term)

        # ── URL / Slug ────────────────────────────────────────────────────
        post_url = None
        for link in entry.findall("atom:link", NS):
            if link.get("rel") == "alternate":
                post_url = link.get("href", "")
                break

        # ── Build Jekyll file ─────────────────────────────────────────────
        if kind == "post":
            if not post_url:
                skipped += 1
                continue
            slug = slug_from_url(post_url)
            date_str = pub_dt.strftime("%Y-%m-%d")
            time_str = pub_dt.strftime("%H:%M:%S %z")
            dest_filename = f"{date_str}-{safe_filename(slug)}.html"
            dest_path = os.path.join(posts_dir, dest_filename)

            # Extract images for the report
            imgs = extract_images(content or "")
            blogger_imgs = [i for i in imgs if "blogger.googleusercontent.com" in i or "bp.blogspot.com" in i]
            all_images.extend(blogger_imgs)

            labels_yml = "\n".join(f'  - "{l}"' for l in labels) if labels else ""

            front_matter = f"""---
layout: post
title: "{title}"
date: {date_str} {time_str}
description: ""
{'labels:' + chr(10) + labels_yml if labels_yml else ''}
---

"""
            with open(dest_path, "w", encoding="utf-8") as f:
                f.write(front_matter + (content or ""))
            post_count += 1
            report_lines.append(f"POST  {dest_filename}  ← {post_url}")

        elif kind == "page":
            slug = safe_filename(title.lower().replace(" ", "-"))
            if post_url:
                slug = slug_from_url(post_url) or slug
            dest_filename = f"{slug}.html"
            dest_path = os.path.join(pages_dir, dest_filename)
            front_matter = f"""---
layout: default
title: "{title}"
permalink: /p/{dest_filename}
---

<div class="page-content">
"""
            with open(dest_path, "w", encoding="utf-8") as f:
                f.write(front_matter + (content or "") + "\n</div>")
            page_count += 1
            report_lines.append(f"PAGE  {dest_filename}")

    # ── Migration report ──────────────────────────────────────────────────
    report = [
        "=" * 60,
        "ROTA DE METRÔ — Blogger → Jekyll Migration Report",
        "=" * 60,
        f"Posts converted : {post_count}",
        f"Pages converted : {page_count}",
        f"Entries skipped : {skipped} (drafts / meta entries)",
        "",
        "FILES CREATED:",
        *report_lines,
        "",
    ]

    if all_images:
        unique_imgs = sorted(set(all_images))
        report += [
            "=" * 60,
            "IMAGES HOSTED ON BLOGGER CDN (need manual download):",
            "=" * 60,
            "These images are in your posts but hosted on Blogger's servers.",
            "After you're done migrating, download each one and add to",
            "assets/images/ — then update the src= in the post files.",
            "",
            *unique_imgs,
        ]
    else:
        report.append("No Blogger-CDN images found (all images are external links).")

    report_text = "\n".join(report)
    with open("migration_report.txt", "w", encoding="utf-8") as f:
        f.write(report_text)

    print(report_text)
    print("\n✅ Done. Check migration_report.txt for details.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/blogger_to_jekyll.py path/to/blog-export.xml")
        sys.exit(1)
    convert(sys.argv[1])
