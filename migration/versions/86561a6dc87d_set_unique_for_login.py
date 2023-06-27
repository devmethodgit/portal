"""set unique for login

Revision ID: 86561a6dc87d
Revises: a6965959e724
Create Date: 2023-06-26 09:13:40.794491

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "86561a6dc87d"
down_revision = "a6965959e724"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_unique_constraint("uq_login", "users", ["login"])


def downgrade() -> None:
    op.drop_constraint("uq_login", "users", type_="unique")
