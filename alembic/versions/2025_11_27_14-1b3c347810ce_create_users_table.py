"""create_users_table

Revision ID: 1b3c347810ce
Revises: 7962ef2c6d23
Create Date: 2025-11-27 14:36:08.268633

"""

import contextlib
from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import UUID

from alembic import op
from core.config import settings


# revision identifiers, used by Alembic.
revision: str = '1b3c347810ce'
down_revision: str | Sequence[str] | None = '7962ef2c6d23'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'users',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('supervisor_id', UUID(as_uuid=True), nullable=True),
        sa.Column('phone_number', sa.String(20), nullable=True),
        sa.Column('passport_number', sa.String(50), nullable=True, unique=True),
        sa.Column('address', sa.Text, nullable=True),
        sa.Column('language', sa.String(10), nullable=False, server_default='en'),
        sa.Column('email', sa.String(255), nullable=True, unique=True),
        sa.Column('registration_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('comments', postgresql.ARRAY(sa.String), nullable=True),
        sa.Column('status', sa.String(50), nullable=False, server_default='unverified'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
        schema=settings.postgres.POSTGRES_SCHEMA,
    )

    # Create indexes
    op.create_index(
        'ix_users_supervisor_id',
        'users',
        ['supervisor_id'],
        schema=settings.postgres.POSTGRES_SCHEMA,
    )

    op.create_index(
        'ix_users_email',
        'users',
        ['email'],
        schema=settings.postgres.POSTGRES_SCHEMA,
    )


def downgrade() -> None:
    """Downgrade schema."""
    with contextlib.suppress(Exception):
        op.drop_index('ix_users_supervisor_id', 'users', schema=settings.postgres.POSTGRES_SCHEMA)
    with contextlib.suppress(Exception):
        op.drop_index('ix_users_email', 'users', schema=settings.postgres.POSTGRES_SCHEMA)

    with contextlib.suppress(Exception):
        op.drop_table('users', schema=settings.postgres.POSTGRES_SCHEMA)
