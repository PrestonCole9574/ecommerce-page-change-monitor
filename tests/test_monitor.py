import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from monitor import WatchRequest, check_page


def test_changed_product_page_creates_fulfillment_update():
    update = check_page(WatchRequest("https://shop.test/item", "price: 10"), lambda _: "price: 12")
    assert update.changed is True
    assert "fulfillment" in update.message


def test_same_product_page_stays_quiet():
    update = check_page(WatchRequest("https://shop.test/item", "price: 10"), lambda _: "price: 10")
    assert update.changed is False
    assert update.message == "No product page change."
