from __future__ import annotations

import argparse
import json
from pathlib import Path

from monitor import WatchRequest, check_page, fetch_page


def main() -> None:
    parser = argparse.ArgumentParser(description="Check an ecommerce page for a content change")
    parser.add_argument("url")
    parser.add_argument("--previous", type=Path, help="file containing the previous response body")
    args = parser.parse_args()
    previous = args.previous.read_text(encoding="utf-8") if args.previous else ""
    update = check_page(WatchRequest(args.url, previous), fetch_page)
    print(json.dumps(update.__dict__, indent=2))


if __name__ == "__main__":
    main()

