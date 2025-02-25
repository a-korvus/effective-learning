"""Check how incoming data will be prepared before saving it to the DB."""

from datetime import datetime
from unittest import mock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from block_02.task_02.db.query import create_data


@pytest.mark.asyncio
async def test_create_data_success():
    """Check that the 'create_data' correctly saves data in the database."""
    mock_session = mock.MagicMock(AsyncSession)
    mock_session.commit = mock.AsyncMock()

    data = [
        [
            {
                "exchange_product_id": "001",
                "exchange_product_name": "product A",
                "oil_id": "001",
                "delivery_basis_id": "001",
                "delivery_basis_name": "basis A",
                "delivery_type_id": "A",
                "volume": 100,
                "total": 1000,
                "count": 10,
                "date": datetime.strptime("02.06.2024", "%d.%m.%Y"),
            },
            {
                "exchange_product_id": "002",
                "exchange_product_name": "product B",
                "oil_id": "002",
                "delivery_basis_id": "002",
                "delivery_basis_name": "basis B",
                "delivery_type_id": "B",
                "volume": 100,
                "total": 1000,
                "count": 10,
                "date": datetime.strptime("02.06.2024", "%d.%m.%Y"),
            },
        ],
    ]

    await create_data(data, mock_session)

    assert mock_session.add_all.call_count == 1
    mock_session.commit.assert_awaited_once()
