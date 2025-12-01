#!/usr/bin/env python3
"""Fetch and parse API/reference pages from https://docs.fastf1.dev/ into a pandas DataFrame.

This script will:
- Fetch the docs homepage
- Find internal links likely to be API / reference pages
- Scrape headings and the following paragraph (as a short summary)
- Return a pandas DataFrame and optionally save to CSV

Usage:
    python load_fastf1_docs.py --output fastf1_api_docs.csv --limit 20

Notes:
 - Requires: requests, beautifulsoup4, pandas, lxml
 - Network access is required to fetch the live site.
"""
from __future__ import annotations

import argparse
import logging
import sys
from urllib.parse import urljoin, urlparse

import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://docs.fastf1.dev/"


def fetch_url(url: str, timeout: int = 15) -> str:
    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()
    return resp.text


def find_candidate_links(html: str, base_url: str) -> list[str]:
    """Return a list of full URLs that look like API/reference pages.

    Heuristics used:
    - internal links (same host or relative)
    - href containing 'api' or 'reference' or '/api/' anywhere
    - avoid anchors and mailto/tel
    """
    soup = BeautifulSoup(html, "lxml")
    anchors = soup.find_all("a", href=True)
    links = set()
    base_host = urlparse(base_url).netloc

    for a in anchors:
        href = a["href"].strip()
        if href.startswith("mailto:") or href.startswith("tel:"):
            continue
        # ignore pure anchors
        if href.startswith("#"):
            continue
        full = urljoin(base_url, href)
        p = urlparse(full)
        # only same host
        if p.netloc != "" and p.netloc != base_host:
            continue
        # heuristic: look for 'api' or 'reference'
        if "api" in p.path.lower() or "reference" in p.path.lower():
            links.add(full)
    return sorted(links)


def scrape_page(url: str) -> list[dict]:
    """Scrape headings (h1/h2/h3) and the next paragraph as a short summary.

    Returns a list of records with keys: page_url, page_title, heading_tag, heading, summary
    """
    try:
        html = fetch_url(url)
    except Exception as e:
        logging.warning("Failed to fetch %s: %s", url, e)
        return []

    soup = BeautifulSoup(html, "lxml")
    page_title_tag = soup.find(["h1"]) or soup.find("title")
    page_title = page_title_tag.get_text(strip=True) if page_title_tag else ""

    records: list[dict] = []
    for tag_name in ("h2", "h3", "h1"):
        for tag in soup.find_all(tag_name):
            heading_text = tag.get_text(strip=True)
            # find the first paragraph sibling after the heading
            summary = ""
            # look at next siblings until a <p> or another heading
            for sib in tag.find_next_siblings():
                if sib.name == "p":
                    summary = sib.get_text(strip=True)
                    break
                if sib.name and sib.name.startswith("h"):
                    # next heading - stop
                    break

            records.append(
                {
                    "page_url": url,
                    "page_title": page_title,
                    "heading_tag": tag_name,
                    "heading": heading_text,
                    "summary": summary,
                }
            )

    # fallback: if no headings found, take meta description
    if not records:
        desc = ""
        meta = soup.find("meta", attrs={"name": "description"})
        if meta and meta.get("content"):
            desc = meta.get("content").strip()
        records.append(
            {
                "page_url": url,
                "page_title": page_title,
                "heading_tag": "",
                "heading": "",
                "summary": desc,
            }
        )

    return records


def build_dataframe(start_url: str = BASE_URL, limit: int | None = None) -> pd.DataFrame:
    logging.info("Fetching homepage: %s", start_url)
    html = fetch_url(start_url)
    links = find_candidate_links(html, start_url)
    logging.info("Found %d candidate links", len(links))

    if limit:
        links = links[:limit]

    all_records: list[dict] = []
    # include the start page as well in case it contains API text
    pages = [start_url] + links
    for idx, page in enumerate(pages):
        logging.info("Scraping (%d/%d): %s", idx + 1, len(pages), page)
        records = scrape_page(page)
        all_records.extend(records)

    df = pd.DataFrame(all_records)
    # reorder columns
    cols = ["page_url", "page_title", "heading_tag", "heading", "summary"]
    for c in cols:
        if c not in df.columns:
            df[c] = ""
    return df[cols]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Load FastF1 docs API/reference pages into a DataFrame")
    parser.add_argument("--start", default=BASE_URL, help="Start URL (default: docs.fastf1.dev)")
    parser.add_argument("--limit", type=int, default=25, help="Maximum number of candidate pages to scrape (0 for no limit)")
    parser.add_argument("--output", default="fastf1_api_docs.csv", help="CSV file to write (optional)")
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    limit = None if args.limit == 0 else args.limit
    df = build_dataframe(start_url=args.start, limit=limit)

    print(df.head(20).to_string(index=False))
    if args.output:
        df.to_csv(args.output, index=False)
        logging.info("Wrote %d rows to %s", len(df), args.output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
