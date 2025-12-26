"""make user_uuid nullable in email_verifications

Revision ID: c0dfa4d0b2a0
Revises: ce5180d0aeff
Create Date: 2025-12-24 19:53:16.041293

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c0dfa4d0b2a0'
down_revision: Union[str, Sequence[str], None] = 'ce5180d0aeff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "email_verifications",
        "user_uuid",
        existing_type=sa.dialects.postgresql.UUID(as_uuid=True),
        nullable=True,
        comment="legacy field, replaced by ref_type + ref_uuid",
    )


def downgrade() -> None:
    op.alter_column(
        "email_verifications",
        "user_uuid",
        existing_type=sa.dialects.postgresql.UUID(as_uuid=True),
        nullable=False,
    )