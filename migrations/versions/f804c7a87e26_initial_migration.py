"""Initial migration

Revision ID: f804c7a87e26
Revises: 
Create Date: 2025-03-15 16:08:31.070330

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f804c7a87e26'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('about_section', schema=None) as batch_op:
        batch_op.alter_column('title',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.Text(),
               existing_nullable=False)
        batch_op.alter_column('title_mitgliedschaft',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.Text(),
               existing_nullable=False)
        batch_op.alter_column('title_location',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.Text(),
               existing_nullable=False)
        batch_op.alter_column('title_termin',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.Text(),
               existing_nullable=False)
        batch_op.alter_column('title_vorstand',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.Text(),
               existing_nullable=False)
        batch_op.alter_column('title_news',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.Text(),
               existing_nullable=False)
        batch_op.alter_column('title_kontakt',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.Text(),
               existing_nullable=False)
        batch_op.alter_column('title_training',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.Text(),
               existing_nullable=False)
        batch_op.alter_column('welcome_text_training',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.Text(),
               existing_nullable=False)
        batch_op.alter_column('text_training_1',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.Text(),
               existing_nullable=False)
        batch_op.alter_column('text_training_2',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.Text(),
               existing_nullable=False)
        batch_op.alter_column('text_training_3',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.Text(),
               existing_nullable=False)
        batch_op.alter_column('text_training_4',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.Text(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('about_section', schema=None) as batch_op:
        batch_op.alter_column('text_training_4',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)
        batch_op.alter_column('text_training_3',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)
        batch_op.alter_column('text_training_2',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)
        batch_op.alter_column('text_training_1',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)
        batch_op.alter_column('welcome_text_training',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)
        batch_op.alter_column('title_training',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)
        batch_op.alter_column('title_kontakt',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)
        batch_op.alter_column('title_news',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)
        batch_op.alter_column('title_vorstand',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)
        batch_op.alter_column('title_termin',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)
        batch_op.alter_column('title_location',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)
        batch_op.alter_column('title_mitgliedschaft',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)
        batch_op.alter_column('title',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)

    # ### end Alembic commands ###
