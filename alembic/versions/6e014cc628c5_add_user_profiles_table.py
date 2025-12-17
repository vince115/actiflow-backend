"""add user_profiles table

Revision ID: 6e014cc628c5
Revises: 92535a151522
Create Date: 2025-12-17 18:42:37.385666

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '6e014cc628c5'
down_revision: Union[str, Sequence[str], None] = '92535a151522'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        "user_profiles",
        sa.Column("id", sa.Integer, primary_key=True),

        sa.Column(
            "uuid",
            postgresql.UUID(as_uuid=True),
            nullable=False,
            unique=True,
            server_default=sa.text("gen_random_uuid()"),
        ),

        sa.Column(
            "user_uuid",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.uuid", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),

        # ---- profile fields ----
        sa.Column("birthday", sa.Date),
        sa.Column("address", postgresql.JSONB),
        sa.Column("school", sa.String),
        sa.Column("employment", sa.String),
        sa.Column("job_title", sa.String),
        sa.Column("blood_type", sa.String),

        # ---- BaseModel flags ----
        sa.Column("is_active", sa.Boolean, server_default=sa.true(), nullable=False),
        sa.Column("is_deleted", sa.Boolean, server_default=sa.false(), nullable=False),

        # ---- timestamps ----
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True)),

        # ---- audit fields ----
        sa.Column("created_by", sa.String),
        sa.Column("updated_by", sa.String),
        sa.Column("deleted_by", sa.String),

        sa.Column("created_by_role", sa.String),
        sa.Column("updated_by_role", sa.String),
        sa.Column("deleted_by_role", sa.String),

        # ---- optimistic lock ----
        sa.Column("version", sa.Integer, nullable=False, server_default="1"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("user_profiles")
