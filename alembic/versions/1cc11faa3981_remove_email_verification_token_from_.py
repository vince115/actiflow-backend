"""remove email_verification_token from users

Revision ID: 1cc11faa3981
Revises: ef744128e685
Create Date: 2025-12-24 17:47:23.135443

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1cc11faa3981'
down_revision: Union[str, Sequence[str], None] = 'ef744128e685'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema.
    說明：
    - email_verification_token 為舊式設計
    - Email 驗證流程已全面遷移至 email_verifications table
    - User 僅保留驗證狀態（is_email_verified）
    """

    # 若欄位存在才刪，避免不同環境爆炸
    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_column("email_verification_token")


def downgrade() -> None:
    """Downgrade schema.
    ⚠️ 僅為回滾用途
    ⚠️ 新系統不應再使用此欄位
    """

    with op.batch_alter_table("users") as batch_op:
        batch_op.add_column(
            sa.Column(
                "email_verification_token",
                sa.String(),
                nullable=True,
                comment="(deprecated) legacy email verification token",
            )
        )