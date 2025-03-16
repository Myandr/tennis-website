"""Initial migration

Revision ID: 708f9e14bdf5
Revises: 
Create Date: 2025-03-16 11:55:01.330384

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '708f9e14bdf5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('about_section', schema=None) as batch_op:
        batch_op.add_column(sa.Column('location_card1_title', sa.String(length=255), nullable=False))
        batch_op.add_column(sa.Column('location_card1_subtitle', sa.Text(), nullable=False))
        batch_op.add_column(sa.Column('location_card1_address', sa.Text(), nullable=False))
        batch_op.add_column(sa.Column('location_card1_image', sa.String(length=255), nullable=False))
        batch_op.add_column(sa.Column('location_card2_title', sa.String(length=255), nullable=False))
        batch_op.add_column(sa.Column('location_card2_subtitle', sa.Text(), nullable=False))
        batch_op.add_column(sa.Column('location_card2_address', sa.Text(), nullable=False))
        batch_op.add_column(sa.Column('location_card2_image', sa.String(length=255), nullable=False))
        batch_op.add_column(sa.Column('location_card3_title', sa.String(length=255), nullable=False))
        batch_op.add_column(sa.Column('location_card3_subtitle', sa.Text(), nullable=False))
        batch_op.add_column(sa.Column('location_card3_address', sa.Text(), nullable=False))
        batch_op.add_column(sa.Column('location_card3_image', sa.String(length=255), nullable=False))
        batch_op.add_column(sa.Column('location_card4_title', sa.String(length=255), nullable=False))
        batch_op.add_column(sa.Column('location_card4_subtitle', sa.Text(), nullable=False))
        batch_op.add_column(sa.Column('location_card4_address', sa.Text(), nullable=False))
        batch_op.add_column(sa.Column('location_card4_image', sa.String(length=255), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('about_section', schema=None) as batch_op:
        batch_op.drop_column('location_card4_image')
        batch_op.drop_column('location_card4_address')
        batch_op.drop_column('location_card4_subtitle')
        batch_op.drop_column('location_card4_title')
        batch_op.drop_column('location_card3_image')
        batch_op.drop_column('location_card3_address')
        batch_op.drop_column('location_card3_subtitle')
        batch_op.drop_column('location_card3_title')
        batch_op.drop_column('location_card2_image')
        batch_op.drop_column('location_card2_address')
        batch_op.drop_column('location_card2_subtitle')
        batch_op.drop_column('location_card2_title')
        batch_op.drop_column('location_card1_image')
        batch_op.drop_column('location_card1_address')
        batch_op.drop_column('location_card1_subtitle')
        batch_op.drop_column('location_card1_title')

    # ### end Alembic commands ###
