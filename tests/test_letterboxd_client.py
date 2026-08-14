import pytest
import letterboxd_client
from letterboxd_client import parse_watchlist_page, has_next_page

def test_parse_watchlist_page():
    html = """
    <div
        data-component-class="LazyPoster"
        data-item-name="Arrival (2016)"
        data-item-slug="arrival">
    </div>

    <div
        data-component-class="LazyPoster"
        data-item-name="Perfect Blue (1997)"
        data-item-slug="perfect-blue">
    </div>
    """

    items = parse_watchlist_page(html)

    assert len(items) == 2
    assert items[0].title == "Arrival"
    assert items[0].year == 2016
    assert items[0].slug == "arrival"
    assert items[1].title == "Perfect Blue"
    assert items[1].year == 1997
    assert items[1].slug == "perfect-blue"

def test_has_next_page():
    html = """
    <div class="paginate-pages">
        <a href="/user/watchlist/page/2/">Older</a>
    </div>
    """

    assert has_next_page(html) is True

def test_not_has_next_page():
    html = """
    <div class="paginate-pages">
        <a href="/user/watchlist/page/3/">Newer</a>
    </div>
    """

    assert has_next_page(html) is False

def test_fetch_watchlist(monkeypatch):
    page_1 = """
    <div
        data-component-class="LazyPoster"
        data-item-name="Arrival (2016)"
        data-item-slug="arrival">
    </div>

    <div
        data-component-class="LazyPoster"
        data-item-name="Perfect Blue (1997)"
        data-item-slug="perfect-blue">
    </div>

    <a href="/user/watchlist/page/2/">Older</a>
    """

    page_2 = """
    <div
        data-component-class="LazyPoster"
        data-item-name="Heat (1995)"
        data-item-slug="heat">
    </div>
    """

def fake_watchlist_page(username, page=1):
    if page == 1:
        return page_1
    if page == 2:
        return page_2

    monkeypatch.setattr(
        letterboxd_client,
        "fetch_watchlist_page",
        fake_watchlist_page
    )

    items = letterboxd_client.fetch_watchlist("test-user")

    assert len(items) == 3
    assert items[0].title == "Arrival"
    assert items[1].title == "Perfect Blue"
    assert items[2].title == "Heat"


    
