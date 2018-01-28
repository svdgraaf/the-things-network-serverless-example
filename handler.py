import json
import os
import base64
import pprint
import codecs
from binascii import b2a_base64
from botocore.vendored import requests

key = os.environ.get('TTN_KEY', '')
pp = pprint.PrettyPrinter(indent=4)


def uplink(event, context):
    pp.pprint(event)
    body = json.loads(event['body'])
    pp.pprint(base64.b64decode(body['payload_raw']))
    return {
        "statusCode": 200,
        "body": json.dumps("OK")
    }


def downlink(event, context):
    pp.pprint(event)
    payload = codecs.encode(json.loads(event['body'])['payload'])

    url = 'https://integrations.thethingsnetwork.org/ttn-eu/api/v2/down/my-svdgraaf-application/my-http-integration'  # noqa
    params = {
        'key': key
    }

    data = {
        "dev_id": event['pathParameters']['device_id'],
        "port": 1,
        "confirmed": False,
        "payload_raw": b2a_base64(payload).decode('utf-8').strip()
    }
    ttn_response = requests.post(url, params=params, data=json.dumps(data))

    response = {
        "statusCode": ttn_response.status_code,
        "body": json.dumps("ack")
    }

    return response


if __name__ == "__main__":
    pp.pprint(downlink({
        'body': json.dumps({
            "payload": "foobar"
        }),
        'pathParameters': {
            'device_id': 'my-test-device'
        }
    }, {}))
