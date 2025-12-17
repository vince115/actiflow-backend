"""fix submission_value FK

Revision ID: 7178613fccb9
Revises: dd428d06cbdf
Create Date: 2025-12-17 14:47:45.269448

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7178613fccb9'
down_revision: Union[str, Sequence[str], None] = 'dd428d06cbdf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
