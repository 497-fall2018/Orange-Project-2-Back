from datetime import datetime

from models.GymShadowModel import GymShadowModel 
from models.GymStampModel import GymStampModel

from utils.logger import Logger

import twilio

from twilio.twiml.voice_response import Gather, VoiceResponse, Say


class GymController():
    logger = Logger(__name__)

    @classmethod
    def call_gym(cls):

        from twilio.rest import Client

        # Your Account Sid and Auth Token from twilio.com/user/account
        account_sid = "AC001d428747f459acf98d736285ac1ba9"
        auth_token = "d61a7a610d338e673f0333b556fc4f63"
        client = Client(account_sid, auth_token)

        call = client.calls.create(
            to="+19143744449",
            from_="+16317063866",
            url="http://b41cb660.ngrok.io/v1/twilio/xml"
        )

        return '', 200, "calling gym"


    @classmethod
    def retrieve_xml(cls):

        response = VoiceResponse()
        gather = Gather(action='/v1/twilio/gather', method='POST', finishOnKey="#", input="dtmf")
        gather.say("Hello. This is Courts and Shorts. Please press 1 if courts are currntly open, 2 if full, and 3 if you want some ice cream")
        response.append(gather)
        response.say('We didn\'t receive any input. Goodbye!')

        return '', 200, str(response)

    @classmethod
    def get_all(cls):
        result = []
        for each in GymShadowModel.get_all():
            with_status = each.json()
            if each.status == "" and each.schedule:
                with_status['status'] = each.schedule[str(datetime.now().hour)]
            result.append(with_status)

        return '', 200, result

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
