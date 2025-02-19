"""Create models.

Revision ID: aeaffd0efa8f
Revises:
Create Date: 2025-02-19 17:56:33.203449
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "aeaffd0efa8f"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create all tables here."""
    op.create_table(
        "authors",
        sa.Column("author_id", sa.Integer(), nullable=False),
        sa.Column("name_author", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("author_id"),
    )
    op.create_table(
        "cities",
        sa.Column("city_id", sa.Integer(), nullable=False),
        sa.Column("name_city", sa.String(length=255), nullable=False),
        sa.Column("days_delivery", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("city_id"),
    )
    op.create_table(
        "genres",
        sa.Column("genre_id", sa.Integer(), nullable=False),
        sa.Column("name_genre", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("genre_id"),
    )
    op.create_table(
        "steps",
        sa.Column("step_id", sa.Integer(), nullable=False),
        sa.Column("name_step", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("step_id"),
    )
    op.create_table(
        "books",
        sa.Column("book_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("author_id", sa.Integer(), nullable=False),
        sa.Column("genre_id", sa.Integer(), nullable=False),
        sa.Column("price", sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column("amount", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["author_id"],
            ["authors.author_id"],
        ),
        sa.ForeignKeyConstraint(
            ["genre_id"],
            ["genres.genre_id"],
        ),
        sa.PrimaryKeyConstraint("book_id"),
    )
    op.create_table(
        "clients",
        sa.Column("client_id", sa.Integer(), nullable=False),
        sa.Column("name_client", sa.String(length=255), nullable=False),
        sa.Column("city_id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.CheckConstraint(
            "email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'",
            name="check_email_format",
        ),
        sa.ForeignKeyConstraint(
            ["city_id"],
            ["cities.city_id"],
        ),
        sa.PrimaryKeyConstraint("client_id"),
    )
    op.create_index(
        op.f("ix_clients_email"), "clients", ["email"], unique=True
    )
    op.create_table(
        "buyer_wishes",
        sa.Column("buy_id", sa.Integer(), nullable=False),
        sa.Column("buy_description", sa.String(), nullable=False),
        sa.Column("client_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["client_id"],
            ["clients.client_id"],
        ),
        sa.PrimaryKeyConstraint("buy_id"),
    )
    op.create_table(
        "buy_books",
        sa.Column("buy_book_id", sa.Integer(), nullable=False),
        sa.Column("buy_id", sa.Integer(), nullable=False),
        sa.Column("book_id", sa.Integer(), nullable=False),
        sa.Column("amount", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["book_id"],
            ["books.book_id"],
        ),
        sa.ForeignKeyConstraint(
            ["buy_id"],
            ["buyer_wishes.buy_id"],
        ),
        sa.PrimaryKeyConstraint("buy_book_id"),
    )
    op.create_table(
        "buy_steps",
        sa.Column("buy_step_id", sa.Integer(), nullable=False),
        sa.Column("buy_id", sa.Integer(), nullable=True),
        sa.Column("step_id", sa.Integer(), nullable=False),
        sa.Column(
            "data_step_beg",
            sa.DateTime(timezone=True),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "data_step_end",
            sa.DateTime(timezone=True),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["buy_id"],
            ["buyer_wishes.buy_id"],
        ),
        sa.ForeignKeyConstraint(
            ["step_id"],
            ["steps.step_id"],
        ),
        sa.PrimaryKeyConstraint("buy_step_id"),
    )


def downgrade() -> None:
    """Drop all tables here."""
    op.drop_table("buy_steps")
    op.drop_table("buy_books")
    op.drop_table("buyer_wishes")
    op.drop_index(op.f("ix_clients_email"), table_name="clients")
    op.drop_table("clients")
    op.drop_table("books")
    op.drop_table("steps")
    op.drop_table("genres")
    op.drop_table("cities")
    op.drop_table("authors")
