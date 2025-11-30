"""create_auction_table

Revision ID: 72df216017d2
Revises:
Create Date: 2025-11-27 14:32:10.590909

"""

import contextlib
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op
from core.config import settings


# revision identifiers, used by Alembic.
revision: str = '72df216017d2'
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        'auctions',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('type', sa.String(255), nullable=False),
        sa.Column('leasing_company_id', sa.Integer, nullable=True),
        sa.Column('reference_url', sa.String(2048), nullable=True),
        sa.Column('country', sa.String(2), nullable=False),
        sa.Column('end_datetime', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        schema=settings.postgres.POSTGRES_SCHEMA,
    )

    op.create_index(
        'ix_auctions_end_datetime',
        'auctions',
        ['end_datetime'],
        schema=settings.postgres.POSTGRES_SCHEMA,
    )


def downgrade() -> None:
    # Drop index if it exists
    with contextlib.suppress(Exception):
        op.drop_index('ix_auctions_end_datetime', 'auctions', schema=settings.postgres.POSTGRES_SCHEMA)

    # Drop table if it exists
    with contextlib.suppress(Exception):
        op.drop_table('auctions', schema=settings.postgres.POSTGRES_SCHEMA)
