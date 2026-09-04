#!/usr/bin/env python3
"""List and download exhibits (EX-10 material contracts by default) from an
EDGAR filing, and convert them to clean text for analysis or Chutes extraction.

Usage:
    # list documents in a filing
    python3 edgar_exhibits.py list --cik 320193 --accession 0000320193-23-000106

    # download all EX-10* exhibits as clean text into ./exhibits/
    python3 edgar_exhibits.py fetch --cik 320193 --accession 0000320193-23-000106 \
        --prefix EX-10 --outdir ./exhibits

Accession numbers accept dashes or not. Output text files are named
<accession>_<filename>.txt with a header line carrying the source URL so
citations can trace back to the exact exhibit.
"""
import argparse
import json
import re
import sys
import time
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

USER_AGENT = "Chutes Legal AI research (contact: ben@snipespc.com)"


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1
        if tag in ("p", "br", "div", "tr", "table", "h1", "h2", "h3", "h4"):
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)

    def text(self):
        raw = "".join(self.parts)
        raw = re.sub(r"[ \t\xa0]+", " ", raw)
        raw = re.sub(r"\n\s*\n+", "\n\n", raw)
        return raw.strip()


def _get(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    time.sleep(0.2)  # SEC fair-access pacing
    return data if binary else data.decode("utf-8", errors="replace")


def filing_index(cik, accession):
    cik_i = int(cik)
    acc_nodash = accession.replace("-", "")
    url = f"https://www.sec.gov/Archives/edgar/data/{cik_i}/{acc_nodash}/index.json"
    data = json.loads(_get(url))
    items = data.get("directory", {}).get("item", [])
    base = f"https://www.sec.gov/Archives/edgar/data/{cik_i}/{acc_nodash}"
    return [{"name": i["name"], "url": f"{base}/{i['name']}",
             "size": i.get("size")} for i in items]


def html_to_text(html):
    p = TextExtractor()
    p.feed(html)
    return p.text()


def cmd_list(args):
    for item in filing_index(args.cik, args.accession):
        print(json.dumps(item))


def cmd_fetch(args):
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    items = filing_index(args.cik, args.accession)
    wanted = [
        i for i in items
        if i["name"].lower().endswith((".htm", ".html", ".txt"))
        and (not args.prefix or i["name"].upper().startswith(args.prefix.upper()))
    ]
    if not wanted:
        print(f"No documents matching prefix {args.prefix!r} in filing.", file=sys.stderr)
        return
    for item in wanted:
        raw = _get(item["url"])
        text = html_to_text(raw) if item["name"].lower().endswith((".htm", ".html")) else raw
        out = outdir / f"{args.accession.replace('-', '')}_{item['name']}.txt"
        out.write_text(f"SOURCE: {item['url']}\n\n{text}", encoding="utf-8")
        print(json.dumps({"file": str(out), "source": item["url"],
                          "chars": len(text)}))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("list", "fetch"):
        p = sub.add_parser(name)
        p.add_argument("--cik", required=True)
        p.add_argument("--accession", required=True)
        if name == "fetch":
            p.add_argument("--prefix", default="EX-10",
                           help="filename prefix filter, default EX-10 (material contracts)")
            p.add_argument("--outdir", default="./exhibits")
    args = ap.parse_args()
    (cmd_list if args.cmd == "list" else cmd_fetch)(args)


if __name__ == "__main__":
    main()
