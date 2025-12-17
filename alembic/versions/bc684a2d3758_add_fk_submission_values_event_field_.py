"""add fk submission_values.event_field_uuid

Revision ID: bc684a2d3758
Revises: 7178613fccb9
Create Date: 2025-12-17 14:54:13.752704

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bc684a2d3758'
down_revision: Union[str, Sequence[str], None] = '7178613fccb9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
