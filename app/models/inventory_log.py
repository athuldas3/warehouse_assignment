from enum import Enum
from sqlalchemy import Enum as SQLAlchemyEnum
from app import db
from sqlalchemy.sql import func


class ProductCategory(Enum):
    FOOD = 'food'
    APPAREL = 'apparel'
    ELECTRONICS = 'electronics'
    # Add more categories as needed


def get_category_by_key(key):
    try:
        return ProductCategory[key.upper()]
    except KeyError:
        return None


class InventoryLog(db.Model):

    __tablename__ = 'inventory_log'  # Set the table name

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    productID = db.Column(db.Integer, db.ForeignKey('product_meta.productID', onupdate='CASCADE',
                                                    ondelete='CASCADE'), index=True, nullable=False)
    warehouseID = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    category = db.Column(SQLAlchemyEnum(ProductCategory, name='product_categories'), nullable=False)
    addInventoryDate = db.Column(db.DateTime, nullable=False, default=func.current_timestamp())

    def __repr__(self):
        return f'{self.id}'
