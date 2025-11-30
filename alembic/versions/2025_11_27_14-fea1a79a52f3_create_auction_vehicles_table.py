"""create_auction_vehicles_table

Revision ID: fea1a79a52f3
Revises: 72df216017d2
Create Date: 2025-11-27 14:35:23.703405

"""

import contextlib
from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op
from core.config import settings


# revision identifiers, used by Alembic.
revision: str = 'fea1a79a52f3'
down_revision: str | Sequence[str] | None = '72df216017d2'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        'auction_vehicles',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=False),
        sa.Column('auction_id', sa.Integer, nullable=False),
        sa.Column('manufacturer_id', sa.Integer, nullable=False),
        sa.Column('model_id', sa.Integer, nullable=False),
        sa.Column('manufacturing_date', sa.Date, nullable=False),
        sa.Column('mileage', sa.Integer, nullable=False),
        sa.Column('engine', sa.String(255), nullable=False),
        sa.Column('transmission', sa.String(255), nullable=False),
        sa.Column('vin', sa.String(17), nullable=False, unique=True),
        sa.Column('body_type', sa.String(255), nullable=True),
        sa.Column('color', sa.String(255), nullable=True),
        sa.Column('engine_power', sa.Integer, nullable=False),
        sa.Column('engine_cc', sa.Integer, nullable=False),
        sa.Column('start_price', sa.Integer, nullable=False),
        sa.Column('active', sa.Boolean, nullable=False, default=True),
        sa.Column('is_damaged', sa.Boolean, nullable=False, default=False),
        sa.Column('number_plates', sa.String(20), nullable=True),
        sa.Column('equipment', postgresql.ARRAY(sa.String), nullable=True),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('image_list', postgresql.ARRAY(sa.String), nullable=True),
        sa.Column('damaged_image_list', postgresql.ARRAY(sa.String), nullable=True),
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
        'ix_vehicles_auction_id',
        'auction_vehicles',
        ['auction_id'],
        schema=settings.postgres.POSTGRES_SCHEMA,
    )

    op.create_index(
        'ix_vehicles_manufacturer_id',
        'auction_vehicles',
        ['manufacturer_id'],
        schema=settings.postgres.POSTGRES_SCHEMA,
    )

    op.create_index(
        'ix_vehicles_model_id',
        'auction_vehicles',
        ['model_id'],
        schema=settings.postgres.POSTGRES_SCHEMA,
    )

    op.create_index(
        'ix_vehicles_active',
        'auction_vehicles',
        ['active'],
        schema=settings.postgres.POSTGRES_SCHEMA,
    )


def downgrade() -> None:
    """Downgrade schema."""
    with contextlib.suppress(Exception):
        op.drop_index('ix_vehicles_category', 'auction_vehicles', schema=settings.postgres.POSTGRES_SCHEMA)
        op.drop_index('ix_vehicles_active', 'auction_vehicles', schema=settings.postgres.POSTGRES_SCHEMA)
        op.drop_index('ix_vehicles_model_id', 'auction_vehicles', schema=settings.postgres.POSTGRES_SCHEMA)
        op.drop_index('ix_vehicles_manufacturer_id', 'auction_vehicles', schema=settings.postgres.POSTGRES_SCHEMA)
        op.drop_index('ix_vehicles_auction_id', 'auction_vehicles', schema=settings.postgres.POSTGRES_SCHEMA)

    with contextlib.suppress(Exception):
        op.drop_table('auction_vehicles', schema=settings.postgres.POSTGRES_SCHEMA)
