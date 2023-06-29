"""change len of role name

Revision ID: 4245ab668168
Revises: fc0b3fce1a83
Create Date: 2023-06-26 17:31:54.010430

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4245ab668168"
down_revision = "fc0b3fce1a83"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column("role", "role_name", type_=sa.String(128))


def downgrade() -> None:
    op.alter_column("role", "role_name", type_=sa.String(64))
