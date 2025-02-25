"""Some db queries."""

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from block_02.task_02.db.models import Result
from block_02.task_02.db.schemas import ResultSchema

lgr = logging.getLogger(__name__)


async def create_data(data: list[list[dict]], session: AsyncSession) -> None:
    """Process all parsed data and save it to db."""
    lgr.info("Start saving data to db.")
    for file_data in data:
        res_schs = [ResultSchema(**rows) for rows in file_data]
        models = [Result(**result.model_dump()) for result in res_schs]

        session.add_all(models)

    await session.commit()
    lgr.info("Data have been saved to db.")
