"""Fix User/TeacherData relationship

Revision ID: e62c33be0003
Revises: c29bcb8fbe94
Create Date: 2019-05-20 11:08:19.239900

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e62c33be0003'
down_revision = 'c29bcb8fbe94'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('user_teacher_data_id_fkey', 'user', type_='foreignkey')
    op.drop_column('user', 'teacher_data_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('teacher_data_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('user_teacher_data_id_fkey', 'user', 'teacher_data', ['teacher_data_id'], ['id'])
    # ### end Alembic commands ###
