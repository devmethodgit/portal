"""add indexes

Revision ID: 3dfe06bf8c02
Revises: 0d15acf775f7
Create Date: 2023-07-07 15:09:20.008784

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3dfe06bf8c02"
down_revision = "d3cc108dce35"
branch_labels = None
depends_on = None


def upgrade():
    op.create_index("idx_role", "role", ["role_id"])
    op.create_index("idx_lpus", "lpus", ["id"])
    op.create_index("idx_specialities", "specialities", ["spec_code"])
    op.create_index("idx_users_additional_info", "users_additional_info", ["user_id"])
    op.create_index("idx_users_to_role", "users_to_role", ["users_id", "role_id"])
    op.create_index(
        "idx_users_to_specialisation",
        "users_to_specialisation",
        ["users_id", "spec_id"],
    )
    op.create_index("idx_users_to_lpu", "users_to_lpu", ["users_id", "lpu_id"])
    op.create_index("idx_lpus_to_mo", "lpus_to_mo", ["mo_id", "lpu_id"])
    op.create_index("idx_users", "users", ["id", "login"])


def downgrade():
    op.drop_index("idx_role", table_name="role")
    op.drop_index("idx_lpus", table_name="lpus")
    op.drop_index("idx_specialities", table_name="specialities")
    op.drop_index("idx_users_additional_info", table_name="users_additional_info")
    op.drop_index("idx_users_to_role", table_name="users_to_role")
    op.drop_index("idx_users_to_specialisation", table_name="users_to_specialisation")
    op.drop_index("idx_users_to_lpu", table_name="users_to_lpu")
    op.drop_index("idx_lpus_to_mo", table_name="lpus_to_mo")
    op.drop_index("idx_users", table_name="users")
