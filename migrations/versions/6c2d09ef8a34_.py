"""empty message

Revision ID: 6c2d09ef8a34
Revises: 3387b4dac9cc
Create Date: 2025-04-05 12:09:14.131126

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6c2d09ef8a34'
down_revision = '3387b4dac9cc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('news', schema=None) as batch_op:
        batch_op.add_column(sa.Column('full_text', sa.Text(), nullable=True))
        batch_op.drop_column('content')
        batch_op.drop_column('updated_at')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('news', schema=None) as batch_op:
        batch_op.add_column(sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('content', sa.TEXT(), autoincrement=False, nullable=False))
        batch_op.drop_column('full_text')

    # ### end Alembic commands ###
