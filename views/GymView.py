from flask import request
from flask.views import MethodView
from controllers.GymController import GymController
from utils.parser import ReqParser

import json

class GymView(MethodView):

    # @classmethod
    # def make_gym(cls):
    #     data = json.loads(request.data.decode("utf-8"))
    #     req_params = ['howmany', 'discount', 'deadline', 'keyword']
    #     if not ReqParser.check_body(data, req_params):
    #         return json.dumps({"error_message": "ill-formed request"}), 400
        
    #     error_message, status = PromoController.make_promo(int(data['howmany']), int(data['discount']), data['deadline'], data['keyword'])

    #     if error_message:
    #         return json.dumps({"error_message": error_message}), status

    #     return json.dumps({"response": "Success!"}), 201

    @classmethod
    def get_gym(cls):
        error_message, status, response = GymController.get_all_gyms()

        if error_message:
            return json.dumps({"error_message": error_message}), status

        return json.dumps({"response": list(map(lambda x : x.json() if x else None, response))}), status
