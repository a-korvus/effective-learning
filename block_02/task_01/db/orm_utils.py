"""Some useful ORM tools."""

from datetime import datetime
from typing import Annotated

from email_validator import EmailNotValidError, validate_email
from sqlalchemy import DateTime, String, func, text
from sqlalchemy.orm import mapped_column

# custom ORM Model fields
int_pk = Annotated[int, mapped_column(primary_key=True)]
str_limit = Annotated[str, mapped_column(String(255), nullable=False)]
created_at = Annotated[
    datetime,
    mapped_column(
        DateTime(timezone=True), server_default=text("timezone('utc', now())")
    ),
]
updated_at = Annotated[
    datetime,
    mapped_column(
        DateTime(timezone=True),
        server_default=text("timezone('utc', now())"),
        onupdate=func.now(),
    ),
]


# auxiliary functions
def validate_email_address(email: str) -> str:
    """Confirm email address during the model creation stage.

    Args:
        email (str): Customer's email address.

    Raises:
        ValueError: Customer passed an invalid email.

    Returns:
        str: Normalized email address.
    """
    try:
        result = validate_email(email, check_deliverability=False)
        return result.normalized
    except EmailNotValidError as _ex:
        raise ValueError(f"Invalid email: {_ex}")
