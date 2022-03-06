import json
import boto3
# from boto3.dynamodb.conditions import Key, Attr
from boto3.dynamodb.conditions import Key
import os
from src.handlers.utils import jsonify, create_presigned_urls

BUCKET = os.environ["GAMES_BUCKET"]
REGION = os.environ["REGION"]
GAMES_TABLE = os.environ["GAMES_TABLE"]

dynamo_resource = boto3.resource("dynamodb", region_name=REGION)
games_table = dynamo_resource.Table(GAMES_TABLE)
s3_client = boto3.client("s3", region_name=REGION)

def handler(event, context):

    print(event)
    jresp = {"data": ""}
    status_code=200
    items = []

    try:

        uid = event.get('pathParameters', {}).get('uid')
        # fe = Attr('uid').eq(uid);
        fe = Key('uid').eq(uid);
        pe = "id, platform, gname, description, timg"

        response = games_table.scan(
            FilterExpression=fe,
            ProjectionExpression=pe
        )

        items = response.get('Items', [])
        if items:
            j = 0
            for item in items:
                url_timg = item.get('timg')
                url = create_presigned_urls(s3_client, BUCKET, url_timg, 3600)
                items[j]["timg"] = url
                j = j + 1

    except Exception as e:
        msg_error = "An exception occurred " + str(e) + "."
        print(msg_error)
        jresp = {"error": msg_error}
        status_code = 500

    jresp = {'data': items}
    print(jresp)   
    return jsonify(jresp, status_code)
