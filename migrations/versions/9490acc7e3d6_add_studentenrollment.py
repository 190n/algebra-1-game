"""Add StudentEnrollment

Revision ID: 9490acc7e3d6
Revises: 94f158be822c
Create Date: 2019-05-20 17:22:09.147457

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9490acc7e3d6'
down_revision = '94f158be822c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('student_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('student_enrollment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.Column('section_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['section_id'], ['section.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['student_data.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('student_id', 'section_id', name='_student_section_uc')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('student_enrollment')
    op.drop_table('student_data')
    # ### end Alembic commands ###
