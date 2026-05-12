"""Crawl https://vitawise.life and report broken internal links.

Output: writes a JSON report to .maintenance/<date>-broken.json
        prints a summary to stdout
        exits with status 1 if any links are broken (so the wrapping script
        can branch on it).

Handles Hugo's minified HTML (unquoted attributes)."""
import json
import os
import re
import sys
import urllib.error
import urllib.request
from collections import Counter, deque
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse

ROOT = "https://vitawise.life/"
HREF_RE = re.compile(r"""href\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))""", re.I)
MAX_PAGES = 2000
TIMEOUT = 15


def normalize(u: str) -> str:
    return u.split("#", 1)[0].rstrip("?")


def main() -> int:
    seen = set()
    broken: list[tuple[str, object, str]] = []
    queue = deque([(ROOT, "(seed)")])
    while queue and len(seen) < MAX_PAGES:
        url, referrer = queue.popleft()
        if url in seen:
            continue
        seen.add(url)
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "VitaWise-Maintenance/1.0"}
            )
            resp = urllib.request.urlopen(req, timeout=TIMEOUT)
            code = resp.getcode()
            content_type = resp.headers.get("content-type", "")
            body = ""
            if "html" in content_type:
                body = resp.read(3_000_000).decode("utf-8", "ignore")
            if code >= 400:
                broken.append((url, code, referrer))
                continue
            for m in HREF_RE.finditer(body):
                href = (m.group(1) or m.group(2) or m.group(3) or "").strip()
                if not href or href.startswith(
                    ("mailto:", "tel:", "javascript:", "#", "data:")
                ):
                    continue
                # Skip JS template literals: hrefs containing concat (`'+x+'`)
                # or template syntax (`${...}`) are runtime JS, not real links.
                if "${" in href or "'+" in href or '+"' in href:
                    continue
                target = normalize(urljoin(url, href))
                if urlparse(target).netloc != "vitawise.life":
                    continue
                if target not in seen:
                    queue.append((target, url))
        except urllib.error.HTTPError as e:
            broken.append((url, e.code, referrer))
        except Exception as e:  # noqa: BLE001
            broken.append((url, f"ERR:{type(e).__name__}", referrer))
        if len(seen) % 200 == 0:
            print(
                f"  ... visited {len(seen)}, queue {len(queue)}, broken {len(broken)}",
                file=sys.stderr,
            )

    repo_root = Path(__file__).resolve().parent.parent
    maintenance_dir = repo_root / ".maintenance"
    maintenance_dir.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    out_path = maintenance_dir / f"{today}-broken.json"
    out_path.write_text(
        json.dumps(
            {
                "date": today,
                "crawled": len(seen),
                "broken": [
                    {"url": u, "status": c, "referrer": r} for u, c, r in broken
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    by_status = Counter(b[1] for b in broken)
    print(f"Crawled: {len(seen)} URLs")
    print(f"Broken:  {len(broken)}")
    for status, n in by_status.most_common():
        print(f"  status {status}: {n}")
    print(f"\nReport: {out_path}")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
