# run.py
from app import app, Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

if __name__ == '__main__':
    app.run(debug=True)

app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
