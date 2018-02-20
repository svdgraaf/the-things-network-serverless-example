import json
import os
from base64 import b64decode
import pprint
import codecs
import uuid
import boto3
from binascii import b2a_base64
from botocore.vendored import requests
pp = pprint.PrettyPrinter(indent=4)


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
key = os.environ.get('TTN_KEY', '')


def uplink(event, context):
    body = json.loads(event['body'])
    print(body)
    item = {
        'id': str(uuid.uuid1()),
        'payload': b64decode(body['payload_raw']).decode('utf-8').strip(),
        'device_id': body['dev_id'],
        'createdAt': body['metadata']['time']
    }
    table.put_item(Item=item)

    return {
        "statusCode": 200,
        "body": json.dumps("OK")
    }


def downlink(event, context):
    payload = codecs.encode(json.loads(event['body'])['payload'])
    print(event['body'])
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


def log(event, context):
    data = []
    response = table.scan()
    data = response['Items']
    while response.get('LastEvaluatedKey'):
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])

    data = sorted(data, key=lambda k: k['createdAt'], reverse=True)

    response = {
        "headers": {
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Origin": "*"
        },
        "statusCode": 200,
        "body": json.dumps(data)
    }
    return response



# Local testing...
# if __name__ == "__main__":
#     # pp.pprint(log({}, {}))
#     # temps = [b'18.1',b'18.2',b'18.0',b'18.3',b'18.4',b'18.7',b'18.8',b'18.9',b'19.1',b'19.3',b'19.7',b'20.1',b'20.3',b'20.1']
#     # for temp in temps:
#     #     pp.pprint(uplink({
#     #         'body': json.dumps({
#     #             "payload": "foobar",
#     #             "payload_raw": b2a_base64(temp).decode('utf-8').strip(),
#     #             "dev_id": "my-test-device",
#     #             "metadata": {
#     #                 "time": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
#     #             }
#     #         }),
#     #         'pathParameters': {
#     #             'device_id': 'my-test-device'
#     #         }
#     #     }, {}))
#     pass
