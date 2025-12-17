"""add activity_template_uuid to events

Revision ID: 92535a151522
Revises: bc684a2d3758
Create Date: 2025-12-17 16:25:41.842299

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '92535a151522'
down_revision: Union[str, Sequence[str], None] = 'bc684a2d3758'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "events",
        sa.Column(
            "activity_template_uuid",
            sa.UUID(as_uuid=True),
            sa.ForeignKey("activity_templates.uuid", ondelete="SET NULL"),
            nullable=True,
        ),
    )
    op.create_index(
        "ix_events_activity_template_uuid",
        "events",
        ["activity_template_uuid"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_events_activity_template_uuid", table_name="events")
    op.drop_column("events", "activity_template_uuid")
