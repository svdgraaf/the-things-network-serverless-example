import json
import os
from base64 import b64decode
import pprint
import codecs
import uuid
import boto3
from util import dict_to_dynamo_item, DecimalEncoder
from binascii import b2a_base64
from botocore.vendored import requests
from boto3.dynamodb.conditions import Key
pp = pprint.PrettyPrinter(indent=4)


dynamodb = boto3.resource('dynamodb')
client = boto3.client('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
key = os.environ.get('TTN_KEY', '')


def uplink(event, context):
    # parse request body and log it
    body = json.loads(event['body'])
    print(body)

    # build a dynamo item
    item = {
        'id': str(uuid.uuid1()),
        'createdAt': body['metadata']['time'],
    }
    # add the whole request body
    item.update(dict_to_dynamo_item(body))

    # If we don't have specific payload fields, store the whole payload
    if 'payload_fields' not in body:
        try:
            payload = b64decode(body['payload_raw']).decode('utf-8').strip()
            item.update({'payload': payload})
        except Exception as e:
            return {
                "statusCode": 500,
                "body": str(e)
            }

    # Store item in dynamo table
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
    dev_id = event['pathParameters']['device_id']
    response = table.query(
        KeyConditionExpression=Key('dev_id').eq(dev_id) & Key('counter').gt(0),
        ScanIndexForward=False,
        Limit=100
    )
    data = response['Items']
    data = sorted(data, key=lambda k: k['createdAt'], reverse=True)

    response = {
        "headers": {
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Origin": "*"
        },
        "statusCode": 200,
        "body": json.dumps(data, cls=DecimalEncoder)
    }
    return response
