"""change phone len

Revision ID: a6965959e724
Revises: cea7c3e4547c
Create Date: 2023-06-22 16:27:04.747505

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a6965959e724"
down_revision = "cea7c3e4547c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column("users_additional_info", "phone", type_=sa.String(64))


def downgrade() -> None:
    op.alter_column("users_additional_info", "phone", type_=sa.String(length=16))
