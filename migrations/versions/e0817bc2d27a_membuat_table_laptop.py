"""membuat table laptop

Revision ID: e0817bc2d27a
Revises: 383f7a081f44
Create Date: 2023-11-13 06:50:03.325271

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e0817bc2d27a'
down_revision = '383f7a081f44'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('laptop',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('storage', sa.Integer(), nullable=False),
    sa.Column('display', sa.Integer(), nullable=False),
    sa.Column('cpu', sa.String(length=100), nullable=False),
    sa.Column('gpu', sa.String(length=100), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('laptop')
    # ### end Alembic commands ###
