import json

class helper():
    @classmethod
    def print_error(cls, resp, status):
        if resp.status_code != status:
            resp_json = json.loads(resp.data.decode())
            print(resp_json)

    @classmethod 
    def ordered(cls, obj):
        if isinstance(obj, dict):
            return sorted((k, cls.ordered(v)) for k, v in obj.items())
        elif isinstance(obj, list):
            return sorted(cls.ordered(x) for x in obj)
        else:
            return obj
