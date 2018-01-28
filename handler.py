import json
import os
import base64
import codecs
from binascii import b2a_base64
from botocore.vendored import requests

key = os.environ.get('TTN_KEY', '')


def uplink(event, context):
    print(event)
    body = json.loads(event['body'])
    print(base64.b64decode(body['payload_raw']))
    return {
        "statusCode": 200,
        "body": json.dumps("OK")
    }


def downlink(event, context):
    print(event)
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


# if __name__ == "__main__":
#     print (downlink({
#         'body': json.dumps({
#             "payload": "foobar"
#         }),
#         'pathParameters': {
#             'device_id': 'my-test-device'
#         }
#     }, {}))
