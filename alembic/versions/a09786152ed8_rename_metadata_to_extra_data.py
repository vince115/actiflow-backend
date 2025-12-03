"""rename metadata to extra_data

Revision ID: a09786152ed8
Revises: 2b2c468a9e63
Create Date: 2025-12-03 18:13:05.030551

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a09786152ed8'
down_revision: Union[str, Sequence[str], None] = '2b2c468a9e63'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "submission",
        "metadata",
        new_column_name="extra_data"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "submission",
        "extra_data",
        new_column_name="metadata"
    )