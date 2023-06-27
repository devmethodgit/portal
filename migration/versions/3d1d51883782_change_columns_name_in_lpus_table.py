"""change columns name in lpus table

Revision ID: 3d1d51883782
Revises: 86561a6dc87d
Create Date: 2023-06-26 12:25:25.428103

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3d1d51883782"
down_revision = "86561a6dc87d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column("lpus", "lpus_name", new_column_name="lpu_name")
    op.alter_column("lpus_to_mo", "lpus_id", new_column_name="lpu_id")
    op.alter_column("user_to_lpu", "lpus_id", new_column_name="lpu_id")


def downgrade() -> None:
    op.alter_column("lpus", "lpu_name", new_column_name="lpus_name")
    op.alter_column("lpus_to_mo", "lpu_id", new_column_name="lpus_id")
    op.alter_column("user_to_lpu", "lpu_id", new_column_name="lpus_id")
