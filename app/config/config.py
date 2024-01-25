import secrets
import os
from dotenv import load_dotenv


class Config:

    # Load environment variables from .env file
    load_dotenv()

    # SECRET_KEY = secrets.token_hex(16)
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(16)
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/warehouse_db'
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.environ.get('DB_USER')}:" \
                              f"{os.environ.get('DB_PASSWORD')}@" \
                              f"localhost/{os.environ.get('DB_NAME')}"
    # SECURITY_PASSWORD_SALT = secrets.token_hex(16)
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT') or secrets.token_hex(16)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
