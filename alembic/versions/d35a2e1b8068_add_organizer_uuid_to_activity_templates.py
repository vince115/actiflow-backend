"""add organizer_uuid to activity_templates

Revision ID: d35a2e1b8068
Revises: 6e014cc628c5
Create Date: 2025-12-19 15:43:48.561716

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'd35a2e1b8068'
down_revision: Union[str, Sequence[str], None] = '6e014cc628c5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. 新增 organizer_uuid 欄位
    op.add_column(
        "activity_templates",
        sa.Column("organizer_uuid", sa.UUID(), nullable=False),
    )

    # 2. 建立 index
    op.create_index(
        "ix_activity_templates_organizer_uuid",
        "activity_templates",
        ["organizer_uuid"],
        unique=False,
    )

    # 3. 建立 FK
    op.create_foreign_key(
        None,
        "activity_templates",
        "organizers",
        ["organizer_uuid"],
        ["uuid"],
        ondelete="CASCADE",
    )

def downgrade() -> None:
    """Downgrade schema."""
    # 1. 先移除 foreign key
    op.drop_constraint(
        None,
        "activity_templates",
        type_="foreignkey",
    )

    # 2. 再移除 index
    op.drop_index(
        "ix_activity_templates_organizer_uuid",
        table_name="activity_templates",
    )

    # 3. 最後移除欄位
    op.drop_column(
        "activity_templates",
        "organizer_uuid",
    )

