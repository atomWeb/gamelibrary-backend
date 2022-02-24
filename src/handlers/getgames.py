import json
import boto3
import os
from src.handlers.utils import jsonify

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
    
    try:
        scan_kwargs = {            
            'ProjectionExpression': "platform, gname, description, timg"            
        }
        response = games_table.scan(**scan_kwargs)
        items = response.get('Items', [])

        j = 0
        for item in items:
            url_item = item.get('timg')
            url = s3_client.generate_presigned_url(
                ClientMethod='get_object',
                Params={
                    'Bucket': BUCKET,
                    'Key': url_item
                }
            )
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
