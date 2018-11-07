from db import db
from datetime import datetime

from models.basemodel import BaseModel
from utils.jsonencode import JsonEncodedDict
from tests.helper_tests import helper

class GymShadowModel(db.Model, BaseModel):
    __tablename__ = "gymshadow"

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_updated = db.Column(db.DateTime)

    name = db.Column(db.String(100))
    phone = db.Column(db.String(200))
    pic_url = db.Column(db.String(255))
    status = db.Column(db.String(200))
    schedule = db.Column(JsonEncodedDict)

    def __init__(self, name, pic_url, phone):
        self.name = name
        self.pic_url = pic_url
        self.phone = phone
        self.date_created = datetime.now()
        self.date_updated = datetime.now()
        self.status = ""
        
    def json(self):
        return {
                "id": self.id,
                "name": self.name,
                "pic_url": self.pic_url,
                "date_created": self.date_created.strftime("%Y-%m-%d %H:%M:%S"),
                "date_updated": self.date_updated.strftime("%Y-%m-%d %H:%M:%S"),
                "schedule": self.schedule,
                "phone": self.phone,
                "status": self.status,
                }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
