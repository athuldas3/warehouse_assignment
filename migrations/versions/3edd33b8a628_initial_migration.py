"""Initial migration

Revision ID: 3edd33b8a628
Revises: 
Create Date: 2024-01-23 22:31:32.336120

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Enum as SQLAlchemyEnum
import uuid
from enum import Enum


# revision identifiers, used by Alembic.
revision = '3edd33b8a628'
down_revision = None
branch_labels = None
depends_on = None

Base = declarative_base()


class ProductCategory(Enum):
    FOOD = 'food'
    APPAREL = 'apparel'
    ELECTRONICS = 'electronics'
    # Add more categories as needed


class RoleMapping(Base):
    __tablename__ = 'role'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    role = sa.Column(sa.String(50), nullable=False)
    CreatedDate = sa.Column(sa.DateTime, nullable=False, default=func.current_timestamp())

    def __repr__(self):
        return f'{self.role}'


class SellerMeta(Base):
    __tablename__ = 'seller_meta'

    sellerID = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    sellerName = sa.Column(sa.String(255), nullable=False)
    sellerGST = sa.Column(sa.String(15), nullable=False)
    registrationDate = sa.Column(sa.DateTime, nullable=False, default=func.current_timestamp())

    def __repr__(self):
        return f'{self.sellerName}'


class User(Base):
    __tablename__ = 'user'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    username = sa.Column(sa.String(80), unique=True, nullable=False)
    email = sa.Column(sa.String(255), unique=True, nullable=False)
    password_hash = sa.Column(sa.String(255), nullable=False)
    role = sa.Column(sa.Integer, sa.ForeignKey('role.id', onupdate='CASCADE', ondelete='CASCADE'), index=True, nullable=False)
    CreatedDate = sa.Column(sa.DateTime, nullable=False, default=func.current_timestamp())

    def __repr__(self):
        return f'{self.email}'


class ProductMeta(Base):
    __tablename__ = 'product_meta'

    productID = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    productName = sa.Column(sa.String(255), nullable=False)
    onboardInventoryDate = sa.Column(sa.DateTime, nullable=False, default=func.current_timestamp())
    sellerID = sa.Column(sa.Integer, sa.ForeignKey('seller_meta.sellerID', onupdate='CASCADE', ondelete='CASCADE'), index=True, nullable=False)

    def __repr__(self):
        return f'{self.productName}'


class InventoryLog(Base):
    __tablename__ = 'inventory_log'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    productID = sa.Column(sa.Integer, sa.ForeignKey('product_meta.productID', onupdate='CASCADE', ondelete='CASCADE'), index=True, nullable=False)
    warehouseID = sa.Column(sa.String(50), nullable=False)
    quantity = sa.Column(sa.Integer, nullable=False)
    category = sa.Column(SQLAlchemyEnum(ProductCategory, name='product_categories'), nullable=False)
    addInventoryDate = sa.Column(sa.DateTime, nullable=False, default=func.current_timestamp())

    def __repr__(self):
        return f'{self.id}'


def upgrade():
    # Create role table
    op.create_table('role',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('role', sa.String(50), nullable=False),
        sa.Column('CreatedDate', sa.DateTime(), nullable=False)
    )

    # Create seller_meta table
    op.create_table('seller_meta',
        sa.Column('sellerID', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('sellerName', sa.String(255), nullable=False),
        sa.Column('sellerGST', sa.String(15), nullable=False),
        sa.Column('registrationDate', sa.DateTime(), nullable=False)
    )

    # Create user table
    op.create_table('user',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('username', sa.String(80), unique=True, nullable=False),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('role', sa.Integer, sa.ForeignKey('role.id', onupdate='CASCADE', ondelete='CASCADE'), index=True, nullable=False),
        sa.Column('CreatedDate', sa.DateTime(), nullable=False)
    )

    # Create product_meta table
    op.create_table('product_meta',
        sa.Column('productID', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('productName', sa.String(255), nullable=False),
        sa.Column('onboardInventoryDate', sa.DateTime(), nullable=False),
        sa.Column('sellerID', sa.Integer, sa.ForeignKey('seller_meta.sellerID', onupdate='CASCADE', ondelete='CASCADE'), index=True, nullable=False)
    )

    # Create inventory_log table
    op.create_table('inventory_log',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('productID', sa.Integer, sa.ForeignKey('product_meta.productID', onupdate='CASCADE', ondelete='CASCADE'), index=True, nullable=False),
        sa.Column('warehouseID', sa.String(50), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('category', sa.String(50), nullable=False),
        sa.Column('addInventoryDate', sa.DateTime(), nullable=False)
    )


def downgrade():
    # Drop tables in reverse order
    op.drop_table('inventory_log')
    op.drop_table('product_meta')
    op.drop_table('user')
    op.drop_table('seller_meta')
    op.drop_table('role')
