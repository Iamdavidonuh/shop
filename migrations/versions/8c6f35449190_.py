"""empty message

Revision ID: 8c6f35449190
Revises: 
Create Date: 2018-12-04 13:55:16.268911

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c6f35449190'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('category_name', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_categories_category_name'), 'categories', ['category_name'], unique=True)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('firstname', sa.String(length=24), nullable=True),
    sa.Column('lastname', sa.String(length=24), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.Column('phonenumber', sa.String(length=18), nullable=True),
    sa.Column('address1', sa.String(length=200), nullable=True),
    sa.Column('address2', sa.String(length=200), nullable=True),
    sa.Column('postcode', sa.String(length=12), nullable=True),
    sa.Column('city', sa.String(length=24), nullable=True),
    sa.Column('state', sa.String(length=24), nullable=True),
    sa.Column('country', sa.String(length=24), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_address1'), 'user', ['address1'], unique=True)
    op.create_index(op.f('ix_user_address2'), 'user', ['address2'], unique=True)
    op.create_index(op.f('ix_user_city'), 'user', ['city'], unique=False)
    op.create_index(op.f('ix_user_country'), 'user', ['country'], unique=False)
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_firstname'), 'user', ['firstname'], unique=True)
    op.create_index(op.f('ix_user_lastname'), 'user', ['lastname'], unique=True)
    op.create_index(op.f('ix_user_phonenumber'), 'user', ['phonenumber'], unique=True)
    op.create_index(op.f('ix_user_postcode'), 'user', ['postcode'], unique=False)
    op.create_index(op.f('ix_user_state'), 'user', ['state'], unique=False)
    op.create_table('kart',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_order_quantity'), 'order', ['quantity'], unique=False)
    op.create_index(op.f('ix_order_timestamp'), 'order', ['timestamp'], unique=False)
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_name', sa.String(length=100), nullable=True),
    sa.Column('product_price', sa.Numeric(precision=7), nullable=True),
    sa.Column('product_image', sa.String(length=120), nullable=True),
    sa.Column('product_stock', sa.String(length=3), nullable=True),
    sa.Column('categories_id', sa.Integer(), nullable=True),
    sa.Column('kart_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['categories_id'], ['categories.id'], ),
    sa.ForeignKeyConstraint(['kart_id'], ['kart.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_product_product_image'), 'product', ['product_image'], unique=True)
    op.create_index(op.f('ix_product_product_name'), 'product', ['product_name'], unique=True)
    op.create_index(op.f('ix_product_product_price'), 'product', ['product_price'], unique=False)
    op.create_index(op.f('ix_product_product_stock'), 'product', ['product_stock'], unique=False)
    op.create_table('association',
    sa.Column('product', sa.Integer(), nullable=True),
    sa.Column('order', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['order'], ['order.id'], ),
    sa.ForeignKeyConstraint(['product'], ['product.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('association')
    op.drop_index(op.f('ix_product_product_stock'), table_name='product')
    op.drop_index(op.f('ix_product_product_price'), table_name='product')
    op.drop_index(op.f('ix_product_product_name'), table_name='product')
    op.drop_index(op.f('ix_product_product_image'), table_name='product')
    op.drop_table('product')
    op.drop_index(op.f('ix_order_timestamp'), table_name='order')
    op.drop_index(op.f('ix_order_quantity'), table_name='order')
    op.drop_table('order')
    op.drop_table('kart')
    op.drop_index(op.f('ix_user_state'), table_name='user')
    op.drop_index(op.f('ix_user_postcode'), table_name='user')
    op.drop_index(op.f('ix_user_phonenumber'), table_name='user')
    op.drop_index(op.f('ix_user_lastname'), table_name='user')
    op.drop_index(op.f('ix_user_firstname'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_index(op.f('ix_user_country'), table_name='user')
    op.drop_index(op.f('ix_user_city'), table_name='user')
    op.drop_index(op.f('ix_user_address2'), table_name='user')
    op.drop_index(op.f('ix_user_address1'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_categories_category_name'), table_name='categories')
    op.drop_table('categories')
    # ### end Alembic commands ###
