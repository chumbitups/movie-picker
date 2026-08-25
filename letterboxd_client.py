import httpx
from bs4 import BeautifulSoup
from models import WatchlistItem

def fetch_watchlist(username: str) -> list[WatchlistItem]:
    page = 1
    result = []

    while True:
        html = fetch_watchlist_page(username, page=page)
        items = parse_watchlist_page(html=html)

        result.extend(items)

        if not has_next_page(html):
            break

        page += 1

    return result

def fetch_watchlist_page(username: str, page: int = 1) -> str:
    if page == 1:
        url = f"https://letterboxd.com/{username}/watchlist/"
    elif page > 1:
        url = f"https://letterboxd.com/{username}/watchlist/page/{page}/"

    response = httpx.get(
        url,
        follow_redirects=True
    )

    response.raise_for_status()

    return response.text

def parse_watchlist_page(html: str) -> list[WatchlistItem]:
    soup = BeautifulSoup(html, "html.parser")

    films = soup.select('[data-component-class="LazyPoster"]')

    parsed_films = []

    for film in films:
        name = film.get("data-item-name")
        slug = film.get("data-item-slug")
        title_part, year_part = name.rsplit(" (", 1)
        year_part = year_part.removesuffix(")")
        year_part = int(year_part)
        parsed_films.append(WatchlistItem(
            title=title_part,
            year=year_part,
            slug=slug
        ))
    return parsed_films

def has_next_page(html: str) -> bool:
    soup = BeautifulSoup(html, "html.parser")

    for link in soup.find_all("a"):
        text = link.get_text(strip=True)

        if text == "Older":
            return True
    return False






    
