"""Asynchronous links parser."""

import asyncio
import logging
import sys
import time
from datetime import datetime
from pprint import pprint

from aiohttp import ClientError, ClientSession, ClientTimeout, TCPConnector
from bs4 import BeautifulSoup
from bs4.element import Tag

lgr = logging.getLogger(__name__)


async def fetch_html(session: ClientSession, url: str) -> str:
    """
    Asynchronously fetch HTML content from a given URL.

    Args:
        session (ClientSession): The session for making HTTP requests.
        url (str): The URL to fetch.

    Returns:
        str: HTML content of the page.
    """
    try:
        async with session.get(url) as response:
            return await response.text()
    except ClientError as e:
        lgr.error(f"Error fetching URL: {url}", exc_info=e)
        raise e
    except asyncio.TimeoutError:
        lgr.error("Request timed out.")
        sys.exit(1)


async def fetch_links(
    session: ClientSession,
    path: str | None = None,
) -> dict[datetime, tuple[str, str]]:
    """
    Asynchronously parse HTML and extract download links from the web page.

    Args:
        session (ClientSession): Opened async session for HTTP requests.
        path (str | None): URL path to process. Defaults to the main page.

    Returns:
        dict[str, str]: Extracted links matched with dates.
    """
    domain = "https://spimex.com"
    if not path:
        path = "/markets/oil_products/trades/results/"
    url = domain + path
    lgr.debug(f"active_url: {url}")

    html_content: str = await fetch_html(session, url)
    soup = await asyncio.to_thread(BeautifulSoup, html_content, "lxml")
    links: dict[datetime, tuple] = {}

    # извлечение блоков со ссылками
    items = await asyncio.to_thread(
        soup.select,
        "div.accordeon-inner__wrap-item",
    )
    for item in items:
        link_tag = await asyncio.to_thread(item.find, "a")
        if not isinstance(link_tag, Tag):
            continue

        # извлечение ссылок, сохранение в список
        if "Бюллетень" in (link_tag.string or ""):
            span_tag = item.find("span")
            if not (isinstance(span_tag, Tag) and span_tag.string):
                raise TypeError(f"Get {type(span_tag)} instead of Tag.")

            date_str = span_tag.string
            date = datetime.strptime(date_str, "%d.%m.%Y")
            if date.year == 2022:
                lgr.warning("Stop links parsing.")
                return links

            path_to_file = await asyncio.to_thread(link_tag.get, "href")
            if not isinstance(path_to_file, str):
                raise TypeError(f"Get {type(path_to_file)} instead of str.")

            link = domain + path_to_file
            ext = path_to_file.split("?")[0].split("/")[-1].split(".")[-1]
            filename = f"{date_str}.{ext}"

            links[date] = (link, filename)
            lgr.debug(f"Saving link {date_str}: {link} for file {filename}")
        else:
            break

    # поиск кнопки пагинации
    pag_btn = await asyncio.to_thread(soup.select_one, ".bx-pag-next")
    if pag_btn:
        link_next_tag = await asyncio.to_thread(pag_btn.find, "a")
        if not isinstance(link_next_tag, Tag):
            raise TypeError(f"Get {type(link_next_tag)} instead of Tag.")

        link_next = await asyncio.to_thread(link_next_tag.get, "href")
        if not isinstance(link_next, str):
            raise TypeError(f"Get {type(path_to_file)} instead of str.")

        lgr.debug(f"Recursing with: {link_next}")
        links.update(await fetch_links(session, link_next))

    return links


async def main() -> None:
    """
    Use thes main asynchronous function.

    Create a session and initiate link parsing here.
    """
    start = time.time()
    timeout = ClientTimeout(total=5)
    connector = TCPConnector(limit=100, ttl_dns_cache=60)

    async with ClientSession(
        timeout=timeout,
        connector=connector,
        raise_for_status=True,
    ) as session:
        # открываю сессию и передаю в парсер
        links: dict[datetime, tuple] = await fetch_links(session)

    delta = round(time.time() - start, 4)
    pprint(links)
    lgr.info(f"Parsed {len(links)} links in {delta} sec.")
    # Parsed 527 links in 18.248 sec


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(lineno)d | %(asctime)s | %(name)s | "
        "%(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    asyncio.run(main())
