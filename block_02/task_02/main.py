"""Main entrypoint to the task execution."""

import asyncio
import logging
import os
import shutil
import time

from block_02.task_02.db.query import create_data
from block_02.task_02.db.setup import session_wrapper
from block_02.task_02.parser.downloader import total_download
from block_02.task_02.parser.extracter import main_extract

lgr = logging.getLogger(__name__)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(lineno)d | %(asctime)s | %(name)s | "
        "%(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    temp_dir_path: str = os.path.join(os.path.dirname(__file__), "temp")
    start: float = time.time()

    lgr.info("Start parse data.")

    asyncio.run(total_download(dest_dir=temp_dir_path))
    result_for_db: list[list[dict]] = main_extract(temp_dir_path)
    asyncio.run(session_wrapper(create_data, result_for_db))
    shutil.rmtree(temp_dir_path)

    lgr.info("Temp dir have been deleted.")
    lgr.info(f"Lenght of results: {len(result_for_db)}")
    lgr.info(f"Task execution time: {round(time.time() - start, 4)}")
    # Task execution time: 57.4417
    # after Semaphore: Task execution time: 44.9057
