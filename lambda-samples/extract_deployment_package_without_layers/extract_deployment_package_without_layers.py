import os
import urllib.request
import filecmp
from zipfile import ZipFile
import logging
import boto3
from botocore.exceptions import ClientError

# Change this as required
LAMBDA_FUNCTION = 'my-function'
LAMBDA_REGION = 'us-west-2'
S3_BUCKET_NAME = 'my-bucket'
S3_OBJECT_NAME = 'lambda.zip'

# Create global variables
LAMBDA_CLIENT = boto3.client('lambda', region_name=LAMBDA_REGION)
S3_CLIENT = boto3.client('s3')

TMP_DEPLOYMENT_PACKAGE = '/tmp/deployment_package'
TMP_LAYER_PACKAGE = '/tmp/layer_package'

# Create empty dirs for downloading the packages
os.mkdir(TMP_DEPLOYMENT_PACKAGE)
os.mkdir(TMP_LAYER_PACKAGE)


def get_deploymentpackage(function_name):
    """Function to extract deployment package"""

    # 1. Get entire deployment package and extract it at /tmp/deployment_package
    response = LAMBDA_CLIENT.get_function(
        FunctionName=function_name
    )
    url = response['Code']['Location']

    # Create file name to be downloaded
    file = f"{TMP_DEPLOYMENT_PACKAGE}/deployment_package.zip"

    # Download and extract file at /tmp
    urllib.request.urlretrieve(url, file)
    with ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(TMP_DEPLOYMENT_PACKAGE)

    ##

    # 2. Get all layers package and extract it at /tmp/layer_package
    for layer in response['Configuration']['Layers']:
        layer_response = LAMBDA_CLIENT.get_layer_version(
            LayerName=':'.join(layer['Arn'].split(':')[:-1]),
            VersionNumber=int(layer['Arn'].split(':')[-1])
        )
        layer_url = layer_response['Content']['Location']

        # Create file name to be downloaded
        layer_file = f"{TMP_LAYER_PACKAGE}/layer_package.zip"

        # Download and extract file at /tmp
        urllib.request.urlretrieve(layer_url, layer_file)
        with ZipFile(layer_file, 'r') as zip_ref:
            zip_ref.extractall(TMP_LAYER_PACKAGE)

    # Layers are added under "python" directory: imp for the next step

    # 3. Compare for diff
    obj = filecmp.dircmp(TMP_DEPLOYMENT_PACKAGE, f'{TMP_LAYER_PACKAGE}/python')
    left_list = obj.left_list
    right_list = obj.right_list

    lambda_files = set(left_list) - set(right_list)
    lambda_files = list(lambda_files)

    # 4. Create zip
    zip_obj = ZipFile('/tmp/lambda.zip', 'w')

    # remove unwanted files
    for i in lambda_files:
        if ('.dist-info' not in i and i != "deployment_package.zip"):
            temp_file = f"{TMP_DEPLOYMENT_PACKAGE}/{i}"
            zip_obj.write(temp_file)

    # close the Zip File
    zip_obj.close()

    # 5. Upload and create presigned url
    with open("/tmp/lambda.zip", "rb") as f:
        S3_CLIENT.upload_fileobj(f, S3_BUCKET_NAME, S3_OBJECT_NAME)

    return create_presigned_url(S3_BUCKET_NAME, S3_OBJECT_NAME)


def create_presigned_url(bucket_name, object_name, expiration=300):
    """Generate a presigned URL for the S3 object"""
    # From https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-presigned-urls.html
    try:
        response = S3_CLIENT.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket_name,
                'Key': object_name
            },
            ExpiresIn=expiration
        )
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response


def lambda_handler(event, context):
    """Main Lambda function"""

    pre_signed_url = get_deploymentpackage(LAMBDA_FUNCTION)

    return {
        'statusCode': 200,
        'body': pre_signed_url
    }
