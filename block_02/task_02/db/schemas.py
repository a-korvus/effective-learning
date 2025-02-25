"""Pydantic schemas for SQLAlchemy models."""

from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field


class ResultSchema(BaseModel):
    """Schema to validate the input data."""

    exchange_product_id: Annotated[str, Field(..., max_length=11)]
    exchange_product_name: Annotated[str, Field(..., max_length=255)]
    oil_id: Annotated[str, Field(..., max_length=4)]
    delivery_basis_id: Annotated[str, Field(..., max_length=3)]
    delivery_basis_name: Annotated[str, Field(..., max_length=255)]
    delivery_type_id: Annotated[str, Field(..., max_length=1)]
    volume: int
    total: int
    count: int
    date: datetime
