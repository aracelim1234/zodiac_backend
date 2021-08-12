"""empty message

Revision ID: b52b2771c843
Revises: 06a2cfbabe07
Create Date: 2021-08-11 22:44:51.939093

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b52b2771c843'
down_revision = '06a2cfbabe07'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('birthday', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'birthday')
    # ### end Alembic commands ###