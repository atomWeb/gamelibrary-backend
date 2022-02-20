import json
import boto3
import os
import uuid
from src.handlers.utils import jsonify, get_str_timestamp

BUCKET = os.environ["GAMES_BUCKET"]
REGION = os.environ["REGION"]
GAMES_TABLE = os.environ["GAMES_TABLE"]

s3_client = boto3.client("s3", region_name=REGION)
dynamo_resource = boto3.resource("dynamodb", region_name=REGION)
games_table = dynamo_resource.Table(GAMES_TABLE)

def handler(event, context):

    print(event)
    jresp = {"data": ""}
    status_code=200
    
    try:
        # Datos de la ejecución
        data = json.loads(event["body"])
        platform = data["platform"]
        boughtAt = data["boughtAt"]
        name = data["name"]
        description = data["description"]        
        # Crear proceso que tome la imagen en base64 y escriba en el bucket
        base64Image = data ["base64Image"]
        imageBucketUrl = base64Image

        user_uid = str(uuid.uuid4())


        # Guarda en la DB el registro del usuario.
        response = games_table.put_item(
            Item={
                "id": user_uid,                
                "platform": platform,
                "boughtAt": boughtAt,
                "name": name,
                "description": description,
                "imageUrl": imageBucketUrl,
                "createAt": get_str_timestamp()
            }
        )
        print("Dynamo Response: ", response)        

    except Exception as e:
        msg_error = "An exception occurred " + str(e) + "."
        print(msg_error)
        jresp = {"error": msg_error}
        status_code = 500

    jresp = {"data": "New game tasks done!"}
    print(jresp)
    return jsonify(jresp, status_code)
