from app import db
from sqlalchemy.sql import func


class ProductMeta(db.Model):

    __tablename__ = 'product_meta'  # Set the table name

    productID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    productName = db.Column(db.String(255), nullable=False)
    onboardInventoryDate = db.Column(db.DateTime, nullable=False, default=func.current_timestamp())
    sellerID = db.Column(db.Integer, db.ForeignKey('seller_meta.sellerID', onupdate='CASCADE',
                                                   ondelete='CASCADE'), index=True, nullable=False)

    def __repr__(self):
        return f'<ProductMeta {self.productName}>'
