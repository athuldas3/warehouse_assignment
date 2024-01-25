from app import db
from sqlalchemy.sql import func


class SellerMeta(db.Model):

    __tablename__ = 'seller_meta'  # Set the table name

    sellerID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sellerName = db.Column(db.String(255), nullable=False)
    sellerGST = db.Column(db.String(15), nullable=False)
    registrationDate = db.Column(db.DateTime, nullable=False, default=func.current_timestamp())

    def __repr__(self):
        return f'<SellerMeta {self.sellerName}>'
