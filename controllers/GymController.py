from models.GymShadowModel import GymShadowModel 

from utils.logger import Logger

class GymController():
    logger = Logger(__name__)

    @classmethod
    def get_all(cls):
        return GymShadowModel.get_all()

    @classmethod
    def make_gym(cls, data):
        pass
