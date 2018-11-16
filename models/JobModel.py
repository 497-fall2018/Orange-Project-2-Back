from db import db
from datetime import datetime

from models.basemodel import BaseModel
from utils.jsonencode import JsonEncodedDict
from tests.helper_tests import helper


class JobModel(db.Model, BaseModel):
    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime)

    name = db.Column(db.String(100))
    phone = db.Column(db.String(200))

    def __init__(self, name, phone):
        self.name = name
        self.phone = phone
        self.date_created = datetime.now()


    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "date_created": self.date_created.strftime("%Y-%m-%d %H:%M:%S"),
            "phone": self.phone,
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).all()

