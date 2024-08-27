"""ubah susunan tabel

Revision ID: 4b15ba648c1d
Revises: aaf9437b731c
Create Date: 2024-07-21 18:50:36.082306

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b15ba648c1d'
down_revision = 'aaf9437b731c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('berita', schema=None) as batch_op:
        batch_op.add_column(sa.Column('link', sa.String(length=200), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('berita', schema=None) as batch_op:
        batch_op.drop_column('link')

    # ### end Alembic commands ###
