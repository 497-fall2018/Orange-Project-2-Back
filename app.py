import os

from db import db
from flask import Flask, request, redirect, Response
from flask_cors import CORS
from flask_migrate import Migrate, MigrateCommand
from flask_admin import Admin
from flask_admin.contrib import sqla
from flask_basicauth import BasicAuth
from werkzeug.exceptions import HTTPException



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///localdata.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['BASIC_AUTH_USERNAME'] = 'orange'
app.config['BASIC_AUTH_PASSWORD'] = 'orange'
migrate = Migrate(app, db)
basic_auth = BasicAuth(app)
admin = Admin(app, name='perf', template_mode='bootstrap3')

if __name__ == '__main__':
    CORS(app)
else:
    CORS(app, resources={r"/*": {"origins": ["front"]}})

@app.route('/')
def hello_world():
    return "running!"


class ModelView(sqla.ModelView):
    def is_accessible(self):
        if not basic_auth.authenticate():
            raise AuthException('Not authenticated.')
        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())

class AuthException(HTTPException):
    def __init__(self, message):
        super().__init__(message, Response(
            "You could not be authenticated. Please refresh the page.", 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'}
        ))


if __name__ == '__main__':
    db.init_app(app)
    @app.before_first_request
    def create_tables():
        db.create_all()

    app.run()