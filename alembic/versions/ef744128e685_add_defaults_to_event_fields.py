"""add defaults to event_fields

Revision ID: ef744128e685
Revises: d35a2e1b8068
Create Date: 2025-12-24 13:04:59.379990

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ef744128e685'
down_revision: Union[str, Sequence[str], None] = 'd35a2e1b8068'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    # --------------------------------------------------------
    # 0. 補齊既有資料（避免 NOT NULL / DEFAULT 失敗）
    # --------------------------------------------------------
    op.execute(
        "UPDATE event_fields SET options='{}'::jsonb WHERE options IS NULL"
    )
    op.execute(
        "UPDATE event_fields SET config='{}'::jsonb WHERE config IS NULL"
    )
    op.execute(
        "UPDATE event_fields SET validation='{}'::jsonb WHERE validation IS NULL"
    )
    op.execute(
        "UPDATE event_fields SET is_enabled=true WHERE is_enabled IS NULL"
    )
    op.execute(
        "UPDATE event_fields SET is_active=true WHERE is_active IS NULL"
    )
    op.execute(
        "UPDATE event_fields SET is_deleted=false WHERE is_deleted IS NULL"
    )
    op.execute(
        "UPDATE event_fields SET version=1 WHERE version IS NULL"
    )

    # --------------------------------------------------------
    # 1. 設定欄位 DEFAULT（未來 INSERT 安全）
    # --------------------------------------------------------
    op.alter_column(
        "event_fields",
        "options",
        server_default=sa.text("'{}'::jsonb"),
        existing_type=postgresql.JSONB,
        existing_nullable=False,
    )

    op.alter_column(
        "event_fields",
        "config",
        server_default=sa.text("'{}'::jsonb"),
        existing_type=postgresql.JSONB,
        existing_nullable=False,
    )

    op.alter_column(
        "event_fields",
        "validation",
        server_default=sa.text("'{}'::jsonb"),
        existing_type=postgresql.JSONB,
        existing_nullable=False,
    )

    op.alter_column(
        "event_fields",
        "is_enabled",
        server_default=sa.true(),
        existing_type=sa.Boolean,
        existing_nullable=False,
    )

    op.alter_column(
        "event_fields",
        "is_active",
        server_default=sa.true(),
        existing_type=sa.Boolean,
        existing_nullable=False,
    )

    op.alter_column(
        "event_fields",
        "is_deleted",
        server_default=sa.false(),
        existing_type=sa.Boolean,
        existing_nullable=False,
    )

    op.alter_column(
        "event_fields",
        "version",
        server_default=sa.text("1"),
        existing_type=sa.Integer,
        existing_nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    # --------------------------------------------------------
    # 1. 移除 DEFAULT（未來 INSERT 安全）
    #   - 保留 NULL
    #   - 保留 NOT NULL
    # --------------------------------------------------------  
    op.alter_column(
        "event_fields",
        "options",
        server_default=None,
        existing_type=postgresql.JSONB,
        existing_nullable=False,
    )

    op.alter_column(
        "event_fields",
        "config",
        server_default=None,
        existing_type=postgresql.JSONB,
        existing_nullable=False,
    )

    op.alter_column(
        "event_fields",
        "validation",
        server_default=None,
        existing_type=postgresql.JSONB,
        existing_nullable=False,
    )

    op.alter_column(
        "event_fields",
        "is_enabled",
        server_default=None,
        existing_type=sa.Boolean,
        existing_nullable=False,
    )

    op.alter_column(
        "event_fields",
        "is_active",
        server_default=None,
        existing_type=sa.Boolean,
        existing_nullable=False,
    )

    op.alter_column(
        "event_fields",
        "is_deleted",
        server_default=None,
        existing_type=sa.Boolean,
        existing_nullable=False,
    )

    op.alter_column(
        "event_fields",
        "version",
        server_default=None,
        existing_type=sa.Integer,
        existing_nullable=False,    
    )
