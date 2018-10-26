class ReqParser(object):
    @classmethod
    def check_body(cls, req, params):
        for param in params:
            if param not in req:
                return False
        return True
