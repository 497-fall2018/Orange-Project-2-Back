from flask import request
from flask.views import MethodView
from controllers.GymController import GymController
from utils.parser import ReqParser

import json

class GymView(MethodView):

    @classmethod
    def call_gym(cls, name):
        error_message, status, response = GymController.call_gym(name)

        if error_message:
            return json.dumps({"error_message": error_message}), status
        return json.dumps({"response": response}), status

    @classmethod
    def retrieve_xml(cls, name):
        error_message, status, response = GymController.retrieve_xml(name)

        if error_message:
            return json.dumps({"error_message": error_message}), status

        return response
        #return json.dumps({"response": response}), status

    @classmethod
    def post_call_data(cls, name):
        user_response = request.values.get("Digits")
        if user_response:
            GymController.update_gym_status(name, user_response)

        error_message, status, response = GymController.thank_you_xml()

        return response

    @classmethod
    def get_gym(cls):
        error_message, status, response = GymController.get_all()

        if error_message:
            return json.dumps({"error_message": error_message}), status

        return json.dumps({"response": response}), status

    @classmethod
    def make_gym(cls):
        data = json.loads(request.data.decode("utf-8"))
        req_params = ['name', 'pic_url', 'phone']
        if not ReqParser.check_body(data, req_params):
            return json.dumps({"error_message": 'ill-formed request'}), 400

        error_message, status = GymController.make_gym(data)

        if error_message:
            return json.dumps({"error_message": error_message}), status

        return json.dumps({"response": "Success!"}), status


    @classmethod
    def make_job(cls):
        data = json.loads(request.data.decode("utf-8"))
        req_params = ['gym_name', 'phone_number']
        if not ReqParser.check_body(data, req_params):
            return json.dumps({"error_message": 'ill-formed request'}), 400

        error_message, status = GymController.make_job(data)

        if error_message:
            return json.dumps({"error_message": error_message}), status

        return json.dumps({"response": "Success!"}), status


    @classmethod
    def make_stamp_scrape(cls):
        data = json.loads(request.data.decode("utf-8"))
        req_params = ['schedule', 'name']
        if not ReqParser.check_body(data, req_params):
            return json.dumps({"error_message": 'ill-formed request'}), 400

        # this is temporary. make_stamp should only deal with internalized data types
        error_message, status = GymController.make_stamp(data['name'], data['schedule'])

        if error_message:
            return json.dumps({"error_message": error_message}), status
        
        return json.dumps({"response": "Success!"}), status
