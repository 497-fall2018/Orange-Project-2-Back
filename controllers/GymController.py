from datetime import datetime

from models.GymShadowModel import GymShadowModel 
from models.GymStampModel import GymStampModel
from models.JobModel import JobModel

from utils.logger import Logger
from utils.twilio import send_notification

from twilio.twiml.voice_response import Gather, VoiceResponse, Say
from twilio.rest import Client

class GymController():
    logger = Logger(__name__)

    @classmethod
    def call_gym(cls, name):

        # Your Account Sid and Auth Token from twilio.com/user/account
        account_sid = "AC001d428747f459acf98d736285ac1ba9"
        auth_token = "d61a7a610d338e673f0333b556fc4f63"
        client = Client(account_sid, auth_token)

        call = client.calls.create(
            to="+12033219249",
            from_="+16317063866",
            #NGROK URL
            url= "http://8d8c914a.ngrok.io" + "/v1/twilio/xml/" + name
        )

        return '', 200, "calling gym"


    @classmethod
    def retrieve_xml(cls, name):

        response = VoiceResponse()
        gather = Gather(action='/v1/twilio/gather/' + name, method='POST', finishOnKey="#", input="dtmf")
        gather.say("Hello. This is Courts and Shorts. Please press 1 if courts are empty, 2 if semi-full, and 3 if full")
        response.append(gather)
        response.say('We didn\'t receive any input. Goodbye!')

        return '', 200, str(response)

    @classmethod
    def thank_you_xml(cls):
        response = VoiceResponse()
        response.say('Thank you, and have a nice day!')

        return '', 200, str(response)

    @classmethod
    def update_gym_status(cls, name, user_response):

        # check if the gym's name is valid
        try:
            target = GymShadowModel.find_by_name(name)
        except:
            cls.logger.exception("Error fetching a gym model")

        if not target:
            cls.logger.exception("Attempted to update a gym without that name")

        status_dict = {"1":"Empty",
                       "2": "Semi-full",
                       "3": "Full"}

        status_string = status_dict.get(user_response)

        if not status_string:
            cls.logger.exception(f"Unexpected user response: {user_response}")
            status_string = "Unknown"

        if target.status == 'Full' and status_string == 'Empty':
            for each in JobModel.get_all():
                send_notification(each.phone)
                JobModel.delete_from_db(each)

        elif target.status == 'Full' and status_string == 'Semi-full':
            for each in JobModel.get_all():
                send_notification(each.phone)
                JobModel.delete_from_db(each)

        target.status = status_string
        target.save_to_db()

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
    def make_job(cls, data):
        try:
            gym_name = data['gym_name']
            phone_num = data['phone_number']

            if not JobModel.find_by_name(gym_name) and not JobModel.find_by_phone_num(phone_num):
                new_job = JobModel(gym_name, phone_num)
                new_job.save_to_db()

        except:
            cls.logger.exception("Error creating a job")
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
