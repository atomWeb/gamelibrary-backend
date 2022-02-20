import json
import boto3
import os
from src.handlers.utils import jsonify


def handler(event, context):

    print(event)
    jresp = {'data': 'Get multiple games'}
    print(jresp)
    return jsonify(jresp)
