"""Asynchronous files downloader."""

# python -m block_02.task_02.downloader

import asyncio
import logging
import os
from datetime import datetime

from aiofiles import open as aopen
from aiohttp import ClientError, ClientSession, ClientTimeout, TCPConnector

from block_02.task_02.parser.parser import fetch_links

CHUNK_SIZE = 8192  # 8 KB
MAX_CONCURRENT_DOWNLOADS = 10  # ограничение количества одновременных загрузок

lgr = logging.getLogger(__name__)


async def download_file(
    session: ClientSession,
    url: str,
    filename: str,
    filedir: str,
) -> None:
    """
    Download the file and save it to file system.

    Args:
        url (str): Direct link to download file.
        filename (str): Specify a file name.
        filedir (str): Specify the location to save the file.
    """
    file_path: str = os.path.join(filedir, filename)

    try:
        async with session.get(url) as response:
            response.raise_for_status()

            async with aopen(file_path, "wb") as f:
                while chunk := await response.content.read(CHUNK_SIZE):
                    await f.write(chunk)
        lgr.debug(f"Download successful to: {file_path}")
    except ClientError as e:
        lgr.error(f"Download failed: {filename}", exc_info=e)


async def total_download(dest_dir: str = "downloads") -> None:
    """
    Download all files from existing links.

    Args:
        dest_dir (str, optional): Destination directory for file downloads.
        Defaults to "downloads".
    """
    os.makedirs(dest_dir, exist_ok=True)
    connector = TCPConnector(
        limit_per_host=MAX_CONCURRENT_DOWNLOADS,
        ttl_dns_cache=300,
    )
    timeout = ClientTimeout(total=600)

    async with ClientSession(connector=connector, timeout=timeout) as session:
        lgr.info("Start getting urls to files.")
        links_data: dict[datetime, tuple[str, str]] = await fetch_links(
            session=session
        )
        urls = [url_tuple for _, url_tuple in links_data.items()]
        lgr.info("All urls have been fetched.")

        # ограничиваем кол-во загрузок кол-вом одновременных соединений
        semaphore = asyncio.Semaphore(MAX_CONCURRENT_DOWNLOADS)

        async def download_with_semaphore(url: str, filename: str) -> None:
            async with semaphore:
                await download_file(session, url, filename, dest_dir)

        lgr.info("Start download files.")
        download_tasks = [
            download_with_semaphore(url, filename) for url, filename in urls
        ]

        await asyncio.gather(*download_tasks)
        lgr.info("All files have been dowloaded.")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(lineno)d | %(asctime)s | %(name)s | "
        "%(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    temp_dir_path: str = os.path.join(os.path.dirname(__file__), "temp")

    asyncio.run(total_download(dest_dir=temp_dir_path))
