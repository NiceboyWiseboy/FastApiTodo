"""Create address table

Revision ID: 51ce148d11c6
Revises: 7771e956dbee
Create Date: 2022-12-29 15:22:39.456619

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '51ce148d11c6'
down_revision = '7771e956dbee'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('address',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('address1', sa.String(), nullable=False),
                    sa.Column('address2', sa.String(), nullable=False),
                    sa.Column('city', sa.String(), nullable=False),
                    sa.Column('state', sa.String(), nullable=False),
                    sa.Column('state', sa.String(), nullable=False),
                    sa.Column('country', sa.String(), nullable=False),
                    sa.Column('postal_code', sa.String(), nullable=False),
                    )


def downgrade() -> None:
    op.drop_table('address')
