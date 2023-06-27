"""change users_to_lpu table name

Revision ID: fc0b3fce1a83
Revises: 7cb4beab6cc4
Create Date: 2023-06-26 12:48:20.626057

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "fc0b3fce1a83"
down_revision = "3d1d51883782"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.rename_table("user_to_lpu", "users_to_lpu")


def downgrade() -> None:
    op.rename_table("users_to_lpu", "user_to_lpu")
