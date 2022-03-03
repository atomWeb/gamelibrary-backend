import json
import boto3
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
    
    try:

        gid = event.get('pathParameters', {}).get('gid')
        # KeyConditionExpression=Key('year').eq(year) & Key('title').between(title_range[0], title_range[1])
        response = games_table.query(
            KeyConditionExpression=Key("id").eq(gid),            
            ScanIndexForward=False,
            Limit=1
        )

        items = response.get('Items', [])

        j = 0
        for item in items:
            url_timg = item.get('timg')
            timgps = create_presigned_urls(s3_client, BUCKET, url_timg, 3600)
            items[j]["timg"] = timgps
            url_image = item.get('image')
            imageps = create_presigned_urls(s3_client, BUCKET, url_image, 3600)
            items[j]["image"] = imageps            
            j = j + 1


    except Exception as e:
        msg_error = "An exception occurred " + str(e) + "."
        print(msg_error)
        jresp = {"error": msg_error}
        status_code = 500

    jresp = {'data': items}
    print(jresp)   
    return jsonify(jresp, status_code)
