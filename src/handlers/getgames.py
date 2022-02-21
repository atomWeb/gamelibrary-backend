import json
import boto3
import os
from src.handlers.utils import jsonify

REGION = os.environ["REGION"]
GAMES_TABLE = os.environ["GAMES_TABLE"]

dynamo_resource = boto3.resource("dynamodb", region_name=REGION)
games_table = dynamo_resource.Table(GAMES_TABLE)

def handler(event, context):

    print(event)
    jresp = {"data": ""}
    status_code=200
    
    try:

        response = games_table.scan()
        items = response.get('Items', [])

    except Exception as e:
        msg_error = "An exception occurred " + str(e) + "."
        print(msg_error)
        jresp = {"error": msg_error}
        status_code = 500

    jresp = {'data': items}
    print(jresp)   
    return jsonify(jresp, status_code)
