from app import db
from sqlalchemy.sql import func
import bcrypt


class User(db.Model):

    __tablename__ = 'user'  # Set the table name

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Integer, db.ForeignKey('role.id', onupdate='CASCADE', ondelete='CASCADE'),
                     index=True, nullable=False)
    CreatedDate = db.Column(db.DateTime, nullable=False, default=func.current_timestamp())

    def __repr__(self):
        return f'{self.email}'

    @staticmethod
    def validate_password(user_obj, password):
        return bcrypt.checkpw(password.encode('utf-8'), user_obj.password_hash.encode('utf-8'))

