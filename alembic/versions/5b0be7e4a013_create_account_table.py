"""create account table

Revision ID: 5b0be7e4a013
Revises: 
Create Date: 2019-12-05 15:03:02.330897

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b0be7e4a013'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'account',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.Unicode(200)),
    )

def downgrade():
    op.drop_table('account')
