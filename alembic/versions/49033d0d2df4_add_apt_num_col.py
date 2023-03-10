"""Add apt num col

Revision ID: 49033d0d2df4
Revises: 23a84af9c231
Create Date: 2022-12-29 17:49:20.064613

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49033d0d2df4'
down_revision = '23a84af9c231'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('address', sa.Column('apt num', sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column('address', 'apt_num')
