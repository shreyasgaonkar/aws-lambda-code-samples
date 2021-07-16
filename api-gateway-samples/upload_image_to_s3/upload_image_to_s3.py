import json
import base64
import uuid
import boto3

S3_CLIENT = boto3.client('s3')
S3_BUCKET_NAME = '<S3-bucket-name>'


def parse_image_from_event(event, context):
    """ Parse event and context to prepare upload """

    """
    Assuming raw image is uploaded through API's POST request
    Optionally set the image/object name with header: `filename: MyFile.png`
    """

    try:
        filename = event['headers']['filename']
    except KeyError:
        # Sample filename with random alpha suffix
        temp = str(uuid.uuid4()).split("-")[-1]
        filename = f"sample_file_{temp}.png"

    try:
        image_content = event['body'].encode('utf-8')

        with open(f"/tmp/{filename}", "wb") as file:
            file.write(base64.b64decode(image_content))

        with open(f"/tmp/{filename}", "rb") as file:
            S3_CLIENT.upload_fileobj(file, S3_BUCKET_NAME, filename)

    except Exception as exp:
        print(exp)
        raise Exception(
            f"Unknown error occured. Check CloudWatch Logs under /aws/lambda/{context.function_name}")


def lambda_handler(event, context):
    """ Main Lambda function """

    parse_image_from_event(event, context)

    return {
        'statusCode': 200,
        'body': json.dumps('Success!')
    }
