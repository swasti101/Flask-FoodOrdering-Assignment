"""Add user_id to menu_item

Revision ID: fa20c9c7f97d
Revises: 
Create Date: 2025-03-31 18:38:13.381703

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa20c9c7f97d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    
    with op.batch_alter_table('menu_item', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_user_menu', 'user', ['user_id'], ['id'])

    op.execute("UPDATE menu_item SET user_id = 1 WHERE user_id IS NULL")

    with op.batch_alter_table('menu_item', schema=None) as batch_op:
        batch_op.alter_column('user_id', nullable=False)


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('menu_item', schema=None) as batch_op:
        batch_op.drop_constraint('fk_user_menu', type_='foreignkey')
        batch_op.drop_column('user_id')

    op.create_table('_alembic_tmp_menu_item',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=100), nullable=False),
    sa.Column('quantity', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='fk_user_menu'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
