import json
import boto3
from prettytable import PrettyTable

# PrettyTable
TABLE = PrettyTable(['Region', 'Lambda function(s)', 'Code Storage',
                     'Regional Concurrency', 'Unreserved Concurrency'])

# AWS Clients for SDK
EC2_CLIENT = boto3.client('ec2')
AWS_REGIONS = EC2_CLIENT.describe_regions()['Regions']

# Lists to store data
ALL_REGIONS = []
FUNCTION_COUNT = []
CODE_STORAGE = []
CONCURRENCY = []
UNRESERVED_CONCURRENCY = []


def format_size(size):
    """ Format into byes, KB, MB & GB """
    power = 2**10
    i = 0
    power_labels = {0: 'bytes', 1: 'KB', 2: 'MB', 3: 'GB'}
    while size > power:
        size /= power
        i += 1
    return f"{round(size, 2)} {power_labels[i]}"


def function_metadata():
    """ return function metadata """

    # Iterate through all regions to find the function's config
    for region_name in AWS_REGIONS:
        try:
            region_name = region_name['RegionName']
            lambda_client = boto3.client('lambda', region_name=region_name)
            response = lambda_client.get_account_settings()
            CODE_STORAGE.append(format_size(response['AccountUsage']['TotalCodeSize']))
            CONCURRENCY.append(response['AccountLimit']['ConcurrentExecutions'])
            UNRESERVED_CONCURRENCY.append(
                response['AccountLimit']['UnreservedConcurrentExecutions'])
            FUNCTION_COUNT.append(response['AccountUsage']['FunctionCount'])
            ALL_REGIONS.append(region_name)
        except Exception as e:
            print(e)


def lambda_handler(event, context):
    """ Main Lambda function """

    function_metadata()
    for i, j in enumerate(ALL_REGIONS):
        TABLE.add_row([ALL_REGIONS[i], FUNCTION_COUNT[i], CODE_STORAGE[i],
                       CONCURRENCY[i], UNRESERVED_CONCURRENCY[i]])
    print(TABLE)

    # Print by sorting a field from the table with optional reversesort flag:
    # print(TABLE.get_string(sortby="Code Storage", reversesort=True))

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
