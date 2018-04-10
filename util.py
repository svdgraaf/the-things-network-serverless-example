import decimal
import json


def dict_to_dynamo_item(raw):
    if type(raw) is dict:
        resp = {}
        for k, v in raw.items():
            if type(v) is str:
                resp[k] = v
            elif type(v) is float:
                resp[k] = decimal.Decimal(str(v))
            elif type(v) is int:
                resp[k] = v
            elif type(v) is dict:
                resp[k] = dict_to_dynamo_item(v)
            elif type(v) is list:
                resp[k] = []
                for i in v:
                    resp[k].append(dict_to_dynamo_item(i))

        return resp
    elif type(raw) is str:
        return str(raw)
    elif type(raw) is int:
        return str(raw)


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)
