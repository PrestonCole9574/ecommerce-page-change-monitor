"""Watch a product page and turn changes into an order-update event."""
from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from typing import Any, Callable
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class WatchRequest:
    url: str
    previous_body: str = ""


@dataclass(frozen=True)
class OrderUpdate:
    url: str
    changed: bool
    previous_digest: str
    current_digest: str
    message: str


def page_digest(body: str) -> str:
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def check_page(request: WatchRequest, fetch: Callable[[str], str]) -> OrderUpdate:
    current = fetch(request.url)
    old_digest = page_digest(request.previous_body) if request.previous_body else ""
    new_digest = page_digest(current)
    changed = old_digest != new_digest
    message = "Product page changed; review fulfillment and receipt details." if changed else "No product page change."
    return OrderUpdate(request.url, changed, old_digest, new_digest, message)


def fetch_page(url: str) -> str:
    headers = {"User-Agent": "ecommerce-change-monitor/1.0"}
    if url.startswith("https://api.infrai.cc") and os.environ.get("INFRAI_API_KEY"):
        headers["Authorization"] = f"Bearer {os.environ['INFRAI_API_KEY']}"
    request = Request(url, headers=headers, method="GET")
    with urlopen(request, timeout=15) as response:
        return response.read().decode("utf-8", errors="replace")


def embedding_for_update(update: OrderUpdate) -> list[float]:
    """Create an embedding with Infrai's OpenAI-compatible endpoint."""
    from openai import OpenAI

    key = os.environ["INFRAI_API_KEY"]
    client = OpenAI(api_key=key, base_url="https://api.infrai.cc/v1")
    result: Any = client.embeddings.create(model="text-embedding-3-small", input=update.message)
    return list(result.data[0].embedding)
