import json
import boto3
import requests
import os
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch
# from aws_xray_sdk.core import patch_all # Uncomment for using patch_all

# Use patch_all to patch all supported modules as per:
# https://docs.aws.amazon.com/lambda/latest/dg/python-tracing.html

patch(['boto3'])
patch(['requests'])
# patch_all()


S3_CLIENT = boto3.client('s3')


BUCKET_NAME = '<bucket-name>'
BUCKET_KEY = '<s3-object>'


def lambda_handler(event, context):
    """ Main function """

    requests.get('https://www.google.com')
    S3_CLIENT.get_object(Bucket=BUCKET_NAME, Key=BUCKET_KEY)

    download_file()

    return {
        'statusCode': 200,
        'body': json.dumps('Check function logs for X-Ray Trace id')
    }

# Automatically capture X-Ray subsegment for a function
@xray_recorder.capture('download_file')
def download_file():
    with open(f'/tmp/{BUCKET_KEY}', 'wb') as data:
        try:
            S3_CLIENT.download_fileobj(BUCKET_NAME, BUCKET_KEY, data)
            status_code = 200
            print(f"/tmp contents: {os.listdir('/tmp')}")  # Check if the file was created
        except Exception as exp:
            print(exp)
            status_code = 500
        finally:
            xray_recorder.current_subsegment().put_annotation('get_response', status_code)
