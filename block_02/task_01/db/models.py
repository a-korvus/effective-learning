"""DB schema based on SQLAlchemy ORM."""

from __future__ import annotations

from decimal import Decimal

from sqlalchemy import CheckConstraint, ForeignKey, Numeric, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    validates,
)

from block_02.task_01.db.orm_utils import (
    created_at,
    int_pk,
    str_limit,
    updated_at,
    validate_email_address,
)


# ORM models
class Base(AsyncAttrs, DeclarativeBase):
    """Base model."""

    __abstract__ = True


class Genre(Base):
    """The Genre entity."""

    __tablename__ = "genres"

    genre_id: Mapped[int_pk]
    name_genre: Mapped[str_limit]

    books: Mapped[list[Book]] = relationship("Book", back_populates="genre")


class Author(Base):
    """The Author entity."""

    __tablename__ = "authors"

    author_id: Mapped[int_pk]
    name_author: Mapped[str_limit]

    books: Mapped[list[Book]] = relationship("Book", back_populates="author")


class City(Base):
    """The City entity."""

    __tablename__ = "cities"

    city_id: Mapped[int_pk]
    name_city: Mapped[str_limit]
    days_delivery: Mapped[int] = mapped_column(default=0)

    clients: Mapped[list[Client]] = relationship(
        "Client",
        back_populates="city",
    )


class Book(Base):
    """The Book entity."""

    __tablename__ = "books"

    book_id: Mapped[int_pk]
    title: Mapped[str_limit]
    author_id: Mapped[int] = mapped_column(
        ForeignKey("authors.author_id"),
        nullable=False,
    )
    genre_id: Mapped[int] = mapped_column(
        ForeignKey("genres.genre_id"),
        nullable=False,
    )
    price: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=2),
        nullable=True,
        default=None,
    )
    amount: Mapped[int] = mapped_column(default=0)

    author: Mapped[Author] = relationship("Author", back_populates="books")
    genre: Mapped[Genre] = relationship("Genre", back_populates="books")
    buy_books: Mapped[list[BuyBook]] = relationship(
        "BuyBook",
        back_populates="book",
    )


class Client(Base):
    """The Client entity."""

    __tablename__ = "clients"

    client_id: Mapped[int_pk]
    name_client: Mapped[str_limit]
    city_id: Mapped[int] = mapped_column(
        ForeignKey("cities.city_id"),
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        String(320),
        unique=True,
        nullable=False,
        index=True,
    )

    city: Mapped[City] = relationship("City", back_populates="clients")
    buy_wishes: Mapped[list[Buy]] = relationship(
        "Buy",
        back_populates="client",
    )

    @validates("email")
    def validate_email(self, _key: str, value: str) -> str:
        """Validate the email address before assignment.

        Args:
            key (str): The name of the attribute being set.
            value (str): The new value for the attribute.

        Returns:
            str: The validated (and possibly normalized) email.
        """
        return validate_email_address(value)

    __table_args__ = (
        CheckConstraint(
            "email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'",
            name="check_email_format",
        ),
    )


class Buy(Base):
    """Buyer's wishes."""

    __tablename__ = "buyer_wishes"

    buy_id: Mapped[int_pk]
    buy_description: Mapped[str] = mapped_column(nullable=False)
    client_id: Mapped[int] = mapped_column(
        ForeignKey("clients.client_id"),
        nullable=False,
    )

    client: Mapped[Client] = relationship(
        "Client",
        back_populates="buy_wishes",
    )
    buy_books: Mapped[list[BuyBook]] = relationship(
        "BuyBook",
        back_populates="buy",
    )
    buy_steps: Mapped[list[BuyStep]] = relationship(
        "BuyStep",
        back_populates="buy",
    )


class Step(Base):
    """Steps of processing of client's order."""

    __tablename__ = "steps"

    step_id: Mapped[int_pk]
    name_step: Mapped[str_limit]

    buy_steps: Mapped[list[BuyStep]] = relationship(
        "BuyStep",
        back_populates="step",
    )


class BuyBook(Base):
    """Order's data."""

    __tablename__ = "buy_books"

    buy_book_id: Mapped[int_pk]
    buy_id: Mapped[int] = mapped_column(
        ForeignKey("buyer_wishes.buy_id"),
        nullable=False,
    )
    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.book_id"),
        nullable=False,
    )
    amount: Mapped[int] = mapped_column(nullable=False)

    buy: Mapped[Buy] = relationship("Buy", back_populates="buy_books")
    book: Mapped[Book] = relationship("", back_populates="buy_books")


class BuyStep(Base):
    """Dates of steps order's processing."""

    __tablename__ = "buy_steps"

    buy_step_id: Mapped[int_pk]
    buy_id: Mapped[int] = mapped_column(
        ForeignKey("buyer_wishes.buy_id"),
        nullable=True,
        default=None,
    )
    step_id: Mapped[int] = mapped_column(
        ForeignKey("steps.step_id"),
        nullable=False,
    )
    data_step_beg: Mapped[created_at]
    data_step_end: Mapped[updated_at]

    buy: Mapped[Buy] = relationship(
        "Buy",
        back_populates="buy_steps",
    )
    step: Mapped[Step] = relationship(
        "Step",
        back_populates="buy_steps",
    )
