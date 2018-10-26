from datetime import datetime

from models.GymShadowModel import GymShadowModel 
from models.GymStampModel import GymStampModel

from utils.logger import Logger

class GymController():
    logger = Logger(__name__)

    @classmethod
    def get_all(cls):
        return '', 200, GymShadowModel.get_all()

    @classmethod
    def make_gym(cls, data):
        try:
            new_gym = GymShadowModel(data['name'], data['pic_url'], data['phone'])
            new_gym.save_to_db()
        except:
            cls.logger.exception("Error creating a gym model")
            return 'Internal Server Error', 500
        return '', 201

    @classmethod
    def make_stamp(cls, name, schedule):
        
        # check if the gym's name is valid
        try:
            target = GymShadowModel.find_by_name(name)
        except:
            cls.logger.exception("Error fetching a gym model")
            return 'Internal Server Error', 500

        if not target:
            cls.logger.exception("Attempted to update a gym without that name")
            return 'Ill-formed Request', 400
        if target.date_updated < datetime.now():
            try:
                new_stamp = GymStampModel(target.id, schedule)
                new_stamp.save_to_db()
            except:
                cls.logger.exception("Error creating and saving a new stamp object")
                return "Internal Server Error", 500
            target.schedule = new_stamp.schedule
            target.date_updated = datetime.now()
            target.save_to_db()
            return '', 201
        else:
            cls.logger.exception("Received an old update")
            return "Not the most recent", 400
