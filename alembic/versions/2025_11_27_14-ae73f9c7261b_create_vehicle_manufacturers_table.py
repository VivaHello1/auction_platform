"""create_vehicle_manufacturers_table

Revision ID: ae73f9c7261b
Revises: fea1a79a52f3
Create Date: 2025-11-27 14:35:43.671685

"""

import contextlib
from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op
from core.config import settings


# revision identifiers, used by Alembic.
revision: str = 'ae73f9c7261b'
down_revision: str | Sequence[str] | None = 'fea1a79a52f3'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'vehicle_manufacturers',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(255), nullable=False, unique=True),
        sa.Column('synonyms', postgresql.ARRAY(sa.String), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column(
            'updated_at',
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
        schema=settings.postgres.POSTGRES_SCHEMA,
    )

    # GIN index for synonyms array for efficient searching
    op.create_index(
        'ix_vehicle_manufacturers_synonyms',
        'vehicle_manufacturers',
        ['synonyms'],
        postgresql_using='gin',
        schema=settings.postgres.POSTGRES_SCHEMA,
    )


def downgrade() -> None:
    """Downgrade schema."""
    with contextlib.suppress(Exception):
        op.drop_index(
            'ix_vehicle_manufacturers_synonyms', 'vehicle_manufacturers', schema=settings.postgres.POSTGRES_SCHEMA
        )

    with contextlib.suppress(Exception):
        op.drop_table('vehicle_manufacturers', schema=settings.postgres.POSTGRES_SCHEMA)
