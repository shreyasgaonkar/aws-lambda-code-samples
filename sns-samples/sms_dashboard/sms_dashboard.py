import os
from datetime import datetime
import gzip
from functools import lru_cache
import boto3
from prettytable import PrettyTable  # imported from Lambda layer

# PrettyTable
DASH_TABLE = PrettyTable(['Type', 'Count'])
COUNTRY_TABLE = PrettyTable(['Country', 'Number of Messages'])
PHONE_NUMBER_TABLE = PrettyTable(['Endpoint', 'Number of Messages'])

SMS_DASH = {}
MESSAGE_TYPE = {}
COUNTRIES_SMS = {}
PHONE_NUMBERS = {}
UTC_NOW = datetime.utcnow()

# ==================
# Defaults to the current month, and AWS region of the function
# Override any values required:

# REGION_NAME = 'us-east-1'
# YEAR = '2020'
# MONTH = '06'
# ==================

try:
    REGION_NAME
except NameError:
    REGION_NAME = os.environ['AWS_REGION']

# Set Year
try:
    if int(YEAR) > UTC_NOW.year:
        raise TypeError("Invalid year")
except (NameError, TypeError) as exp:
    print(f"INFO: `{exp}`. Switching to current year")
    YEAR = UTC_NOW.year
YEAR = str(YEAR)

# Set Month and format as MM
try:
    if type(MONTH) == int:
        MONTH = str(MONTH)
    if ((int(MONTH) > 12) or (int(MONTH) < 0)):
        raise TypeError("Invalid Month")
except (NameError, TypeError) as exp:
    print(f"INFO: `{exp}`. Switching to current month")
    MONTH = str(UTC_NOW.month)
if len(MONTH) == 1:
    MONTH = '0' + MONTH


SNS_CLIENT = boto3.client('sns', region_name=REGION_NAME)
S3_CLIENT = boto3.client('s3', region_name=REGION_NAME)
S3_RESOURCE = boto3.resource('s3')
PINPOINT_CLIENT = boto3.client('pinpoint')


@lru_cache(maxsize=128)
def country_code(phone_number):
    """Get Country Code from phone number"""
    response = PINPOINT_CLIENT.phone_number_validate(
        NumberValidateRequest={
            'PhoneNumber': phone_number
        }
    )
    return response['NumberValidateResponse']['CountryCodeIso2']


def parse_file(file):
    """Given the file, parse and SMS info"""
    with gzip.open(file, 'rb') as f_open:
        # print(f"Opening file:: {file}")
        # iterate each line to not overload memory
        for i, line in enumerate(f_open):
            # skip the header line in each file
            if i == 0:
                continue
            line = line.decode('utf-8')
            temp_data = line.split(",")
            # print(temp_data)
            SMS_DASH['total_parts'] = SMS_DASH.get('total_parts', 0) + int(temp_data[-1])
            SMS_DASH['total_price'] = SMS_DASH.get('total_price', 0) + float(temp_data[-3])
            MESSAGE_TYPE[temp_data[3]] = MESSAGE_TYPE.get(temp_data[3], 0) + 1
            PHONE_NUMBERS[temp_data[2]] = PHONE_NUMBERS.get(temp_data[2], 0) + 1
            country_code_parsed = country_code(temp_data[2])
            COUNTRIES_SMS[country_code_parsed] = COUNTRIES_SMS.get(country_code_parsed, 0) + 1
    return True


def download_files(s3_bucket):
    """Download and extract files from S3 into /tmp directory"""

    # Folder structure of S3's objects in the bucket:
    # /SMSUsageReports/<region>/<year>/<month>

    s3_bucket = S3_RESOURCE.Bucket(s3_bucket)
    s3_object = f"SMSUsageReports/{REGION_NAME}/{YEAR}/{MONTH}"

    ###
    for object_name in s3_bucket.objects.filter(Prefix=s3_object):
        if not os.path.exists(os.path.dirname('/tmp/' + object_name.key)):
            os.makedirs(os.path.dirname('/tmp/' + object_name.key))
        s3_bucket.download_file(object_name.key, '/tmp/'+object_name.key)

    for root, _dirs_, files in os.walk("/tmp", topdown=True):
        for file in files:
            parse_file(f"{root}/{file}")

    # S3_RESOURCE.meta.client.download_file(s3_bucket, s3_object, '/tmp/data')
    # print(f"/tmp: {os.listdir('/tmp')}")
    return True

# def downloadDirectoryFroms3(bucketName,remoteDirectoryName):
#     bucket = S3_RESOURCE.Bucket(bucketName)


def get_usage_report_bucket():
    """Check if this region contains usage reports"""
    response = SNS_CLIENT.get_sms_attributes()
    try:
        response['attributes']['UsageReportS3Bucket']
    except KeyError:
        return False
    else:
        return download_files(response['attributes']['UsageReportS3Bucket'])


def lambda_handler(event, context):
    """Main function"""
    body = 'See function logs for SMS Dashboard.'

    if not get_usage_report_bucket():
        body = 'Cannot determine SMS usage. SMS Usage Reports not enabled for this region.'
    else:
        total_messages = 0

        for i, j in MESSAGE_TYPE.items():
            total_messages += j
            DASH_TABLE.add_row([i, j])

        # Add SMS Dash data
        DASH_TABLE.add_row(['Total SMS', total_messages])
        DASH_TABLE.add_row(['Total Price', str(round(SMS_DASH['total_price'], 4))])
        DASH_TABLE.add_row(['Total Parts', SMS_DASH['total_parts']])

        # Add messages per Country
        for i, j in COUNTRIES_SMS.items():
            COUNTRY_TABLE.add_row([i, j])

        # Add messages per endpoint
        for i, j in PHONE_NUMBERS.items():
            PHONE_NUMBER_TABLE.add_row([i, j])

        # Print the Table!
        print(f"SMS Dashboard for {MONTH}/{YEAR}")
        print(DASH_TABLE)
        print("\n")
        print(COUNTRY_TABLE)
        print("\n")
        print(PHONE_NUMBER_TABLE)

    return {
        'statusCode': 200,
        'body': body
    }
