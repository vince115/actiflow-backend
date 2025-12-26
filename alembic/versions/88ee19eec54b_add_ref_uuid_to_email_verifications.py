"""add ref_uuid to email_verifications

Revision ID: 88ee19eec54b
Revises: 7beb5ac9f35b
Create Date: 2025-12-24 19:44:56.229053

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '88ee19eec54b'
down_revision: Union[str, Sequence[str], None] = '7beb5ac9f35b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1️⃣ 先加 nullable=True（避免既有資料爆炸）
    op.add_column(
        "email_verifications",
        sa.Column(
            "ref_uuid",
            postgresql.UUID(as_uuid=True),
            nullable=True,
            comment="對應資料 UUID（submission / user / password_reset）",
        ),
    )

    # 2️⃣ 若已有資料，可補預設值（依你實際狀況）
    # 如果目前只用在 submission，可以先補 dummy 或之後人工清
    # op.execute("UPDATE email_verifications SET ref_uuid = uuid WHERE ref_uuid IS NULL")

    # 3️⃣ 收緊成 NOT NULL（如果你確定每筆都應該有 ref_uuid）
    op.alter_column(
        "email_verifications",
        "ref_uuid",
        nullable=False,
    )

    # 4️⃣ 建 index（你一定會用到）
    op.create_index(
        "ix_email_verifications_ref_uuid",
        "email_verifications",
        ["ref_uuid"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        "ix_email_verifications_ref_uuid",
        table_name="email_verifications",
    )
    op.drop_column("email_verifications", "ref_uuid")

