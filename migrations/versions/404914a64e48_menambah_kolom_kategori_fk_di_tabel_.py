"""menambah kolom kategori_fk di tabel kriteria

Revision ID: 404914a64e48
Revises: 95c5645d1af7
Create Date: 2023-07-01 19:12:40.998865

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '404914a64e48'
down_revision = '95c5645d1af7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('kriteria', schema=None) as batch_op:
        batch_op.add_column(sa.Column('kategori_fk', sa.BigInteger(), nullable=False))
        batch_op.create_foreign_key(None, 'kategori', ['kategori_fk'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('kriteria', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('kategori_fk')

    # ### end Alembic commands ###
