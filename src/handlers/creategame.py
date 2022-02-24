import json
import base64
import boto3
import os
import uuid
from src.handlers.utils import jsonify, get_str_timestamp

BUCKET = os.environ["GAMES_BUCKET"]
REGION = os.environ["REGION"]
GAMES_TABLE = os.environ["GAMES_TABLE"]

s3 = boto3.resource('s3', region_name=REGION)
s3_client = boto3.client("s3", region_name=REGION)
dynamo_resource = boto3.resource("dynamodb", region_name=REGION)
games_table = dynamo_resource.Table(GAMES_TABLE)


def handler(event, context):

    print(event)
    jresp = {"data": ""}
    status_code = 200
    file_name = ""

    try:
        # Datos de la ejecución
        data = json.loads(event["body"])
        platform = data["platform"]
        boughtAt = data["boughtAt"]
        name = data["name"]
        description = data["description"]
        image_base64 = data["base64Image"]

        game_id = str(uuid.uuid4())

        comachar = ','
        idx = image_base64.index(comachar)
        imageextension = image_base64[:idx]
        idxa = imageextension.index('/')
        idxb = imageextension.index(';')
        extension = imageextension[idxa+1:idxb]
        file_name = game_id + "." + extension
        timg = "timg/" + game_id + "_timg.png"

        string_image = image_base64[idx+1:]
        obj = s3.Object(BUCKET, file_name)
        obj.put(Body=base64.b64decode(string_image))

        # Guarda en la DB el registro del usuario.
        response = games_table.put_item(
            Item={
                "id": game_id,
                "platform": platform,
                "boughtAt": boughtAt,
                "gname": name,
                "description": description,
                "image": file_name,
                "timg": timg,
                "createAt": get_str_timestamp()
            }
        )
        print("Dynamo Response: ", response)

    except Exception as e:
        msg_error = "An exception occurred " + str(e) + "."
        print(msg_error)
        jresp = {"error": msg_error}
        status_code = 500

    jresp = {"data": file_name}
    print(jresp)
    return jsonify(jresp, status_code)
