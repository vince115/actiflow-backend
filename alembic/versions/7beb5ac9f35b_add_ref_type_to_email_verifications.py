"""add ref_type to email_verifications

Revision ID: 7beb5ac9f35b
Revises: 1cc11faa3981
Create Date: 2025-12-24 19:40:00.244956

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7beb5ac9f35b'
down_revision: Union[str, Sequence[str], None] = '1cc11faa3981'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1️⃣ 先加 nullable=True
    op.add_column(
        "email_verifications",
        sa.Column(
            "ref_type",
            sa.String(length=50),
            nullable=True,
            comment="驗證對象類型：submission / user / password_reset",
        ),
    )

    # 2️⃣ 補既有資料（若目前沒有資料，這步不會影響）
    op.execute(
        "UPDATE email_verifications SET ref_type = 'submission' WHERE ref_type IS NULL"
    )

    # 3️⃣ 改成 NOT NULL
    op.alter_column(
        "email_verifications",
        "ref_type",
        nullable=False,
    )

    # 4️⃣ 建 index
    op.create_index(
        "ix_email_verifications_ref_type",
        "email_verifications",
        ["ref_type"],
    )




def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        "ix_email_verifications_ref_type",
        table_name="email_verifications",
    )
    op.drop_column("email_verifications", "ref_type")
