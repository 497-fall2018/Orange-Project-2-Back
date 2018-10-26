from db import db

from models.basemodel import BaseModel
from utils.jsonencode import JsonEncodedDict
from tests.helper_tests import helper

class GymStampModel(db.Model, BaseModel):
    __tablename__ = "gymstamp"

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    gym_id = db.Column(db.Integer, db.ForeignKey('gymshadow.id'))
    schedule = db.Column(JsonEncodedDict)

    def __init__(self, gym_id, schedule):
        self.gym_id = gym_id
        self.schedule = schedule
        
    def json(self):
        return {
                "id": self.id,
                "date_created": self.date_created.strftime("%Y-%m-%d %H:%M:%S"),
                "gym_id": self.name,
                "schedule": helper.ordered(self.schedule),
                }
