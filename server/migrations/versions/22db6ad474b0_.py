"""empty message

Revision ID: 22db6ad474b0
Revises: 9de221e4a5d2
Create Date: 2024-02-09 11:26:24.907971

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22db6ad474b0'
down_revision = '9de221e4a5d2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('_password_hash',
               existing_type=sa.VARCHAR(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('_password_hash',
               existing_type=sa.VARCHAR(),
               nullable=False)

    # ### end Alembic commands ###
