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


def get_str_timestamp():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S.%f")


def jsonify(obj, statusCode=200):
    return {
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'statusCode': statusCode,
        'body': json.dumps(obj, cls=DecimalEncoder)
    }
