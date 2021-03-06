import os

from db import db
from flask import Flask, request, redirect, Response
from flask_cors import CORS
from flask_migrate import Migrate, MigrateCommand
from flask_admin import Admin
from flask_admin.contrib import sqla
from flask_basicauth import BasicAuth
from werkzeug.exceptions import HTTPException

from views.GymView import GymView

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///localdata.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['BASIC_AUTH_USERNAME'] = 'orange'
app.config['BASIC_AUTH_PASSWORD'] = 'oranges'
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
migrate = Migrate(app, db)
basic_auth = BasicAuth(app)
admin = Admin(app, name='Orange', template_mode='bootstrap3')

if __name__ == '__main__':
    CORS(app)
else:
    CORS(app)

@app.route('/')
def hello_world():
    return "running!"

@app.route('/v1/subscribe', methods=['POST'])
def make_job():
    if request.method == 'POST':
        return GymView.make_job()

@app.route('/v1/gyms', methods=['GET', 'POST'])
def gym_info():
    if request.method == 'GET':
        return GymView.get_gym()
    elif request.method == 'POST':
        return GymView.make_gym()

@app.route('/v1/update/<string:name>', methods=['GET', 'POST'])
def gym_update(name):
    if request.method == 'GET':
        return GymView.call_gym(name)
    elif request.method == 'POST':
        return GymView.make_stamp_scrape()


@app.route('/v1/twilio/xml/<string:name>', methods=['POST'])
def get_xml(name):
    if request.method == 'POST':
        return GymView.retrieve_xml(name)


@app.route('/v1/twilio/gather/<string:name>', methods=['POST'])
def post_call_data(name):
    if request.method == 'POST':
        return GymView.post_call_data(name)


from models.GymShadowModel import GymShadowModel
from models.JobModel import JobModel

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

class GymShadowAdminView(ModelView):
    column_list = ['id', 'name', 'phone', 'date_updated', 'schedule', 'date_created', 'pic_url']
    column_searchable_list = ['name']
    column_filters = ['id', 'name', 'date_updated', 'date_created']
    column_default_sort = ('name', True)


class JobAdminView(ModelView):
    column_list = ['id', 'name', 'phone', 'date_created']
    column_searchable_list = ['name']
    column_filters = ['id', 'name', 'date_created']
    column_default_sort = ('name', True)

admin.add_view(GymShadowAdminView(GymShadowModel, db.session))
admin.add_view(JobAdminView(JobModel, db.session))

if __name__ == '__main__':
    db.init_app(app)
    @app.before_first_request
    def create_tables():
        db.create_all()

    app.run()
