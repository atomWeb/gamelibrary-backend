import decimal
from datetime import datetime
import json


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 == 0:
                return int(o)
            else:
                return round(float(o), 12)
        return super(DecimalEncoder, self).default(o)


def now_str_timestamp():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S.%f")


def set_str_timestamp(objDate):
    return objDate.strftime("%Y-%m-%d %H:%M:%S.%f")


def create_presigned_urls(s3Client, bucket_name: str, key: str, expires_in: int):
    """Create presigned_urls
    Args:
        s3Client (s3 Class): boto3 S3 Class
        bucket_name
        key
        expires_in: The number of seconds the presigned URL is valid for.

    Returns:
        (string): presigned URL
    """
    presigned_url = s3Client.generate_presigned_url(
        ClientMethod="get_object",
        Params={
            "Bucket": bucket_name,
            "Key": key
        },
        ExpiresIn=expires_in
    )
    return presigned_url


def jsonify(obj, statusCode=200):
    return {
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
            'Content-Type': 'application/json',
        },
        'statusCode': statusCode,
        'body': json.dumps(obj, cls=DecimalEncoder)
    }
