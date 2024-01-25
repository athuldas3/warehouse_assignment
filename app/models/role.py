from app import db
from sqlalchemy.sql import func


class RoleMapping(db.Model):

    __tablename__ = 'role'  # Set the table name

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role = db.Column(db.String(50), nullable=False)
    CreatedDate = db.Column(db.DateTime, nullable=False, default=func.current_timestamp())

    def __repr__(self):
        return f'{self.role}'
