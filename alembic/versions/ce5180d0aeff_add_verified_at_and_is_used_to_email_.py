"""add verified_at and is_used to email_verifications

Revision ID: ce5180d0aeff
Revises: 88ee19eec54b
Create Date: 2025-12-24 19:50:47.964588

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ce5180d0aeff'
down_revision: Union[str, Sequence[str], None] = '88ee19eec54b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.add_column(
        "email_verifications",
        sa.Column(
            "verified_at",
            sa.DateTime(timezone=True),
            nullable=True,
            comment="驗證完成時間",
        ),
    )

    op.add_column(
        "email_verifications",
        sa.Column(
            "is_used",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
            comment="token 是否已使用",
        ),
    )


def downgrade() -> None:
    op.drop_column("email_verifications", "is_used")
    op.drop_column("email_verifications", "verified_at")