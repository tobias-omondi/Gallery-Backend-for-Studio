"""Initial migration

Revision ID: cc68cbd36f76
Revises: c3ed6a192f54
Create Date: 2024-11-18 15:57:50.970221

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc68cbd36f76'
down_revision = 'c3ed6a192f54'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('podcasts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('Image_url', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('podcasts', schema=None) as batch_op:
        batch_op.drop_column('Image_url')

    # ### end Alembic commands ###
