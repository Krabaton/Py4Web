"""add contacts person

Revision ID: d48f81a5632e
Revises: 3f420b1200b6
Create Date: 2022-03-31 21:14:52.079613

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'd48f81a5632e'
down_revision = '3f420b1200b6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contact_persons',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('first_name', sa.String(length=120), nullable=False),
                    sa.Column('last_name', sa.String(length=120), nullable=False),
                    sa.Column('email', sa.String(length=100), nullable=False),
                    sa.Column('cell_phone', sa.String(length=100), nullable=False),
                    sa.Column('address', sa.String(length=100), nullable=True),
                    sa.Column('student_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('contact_persons')
    # ### end Alembic commands ###