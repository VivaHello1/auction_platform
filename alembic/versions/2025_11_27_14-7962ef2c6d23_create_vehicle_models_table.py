"""create_vehicle_models_table

Revision ID: 7962ef2c6d23
Revises: ae73f9c7261b
Create Date: 2025-11-27 14:35:53.515349

"""

import contextlib
from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op
from core.config import settings


# revision identifiers, used by Alembic.
revision: str = '7962ef2c6d23'
down_revision: str | Sequence[str] | None = 'ae73f9c7261b'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'vehicle_models',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('manufacturer_id', sa.Integer, nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('default_vehicle_type', sa.String(50), nullable=False, comment='Default vehicle type for the model (e.g., suv, sedan...)'),
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

    op.create_index(
        'ix_vehicle_models_name',
        'vehicle_models',
        ['name'],
        schema=settings.postgres.POSTGRES_SCHEMA,
    )

    # GIN index for synonyms array for efficient searching
    op.create_index(
        'ix_vehicle_models_synonyms',
        'vehicle_models',
        ['synonyms'],
        postgresql_using='gin',
        schema=settings.postgres.POSTGRES_SCHEMA,
    )


def downgrade() -> None:
    """Downgrade schema."""
    with contextlib.suppress(Exception):
        op.drop_index('ix_vehicle_models_synonyms', 'vehicle_models', schema=settings.postgres.POSTGRES_SCHEMA)
        op.drop_index('ix_vehicle_models_name', 'vehicle_models', schema=settings.postgres.POSTGRES_SCHEMA)

    with contextlib.suppress(Exception):
        op.drop_table('vehicle_models', schema=settings.postgres.POSTGRES_SCHEMA)
