from app import app
from db import db
from flask_migrate import Migrate

migrate = Migrate(app, db)
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()
