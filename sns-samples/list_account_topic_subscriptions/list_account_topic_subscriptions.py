import json
import concurrent.futures  # for multithreading
import boto3
from prettytable import PrettyTable  # Imported as a Lambda layer

# PrettyTable
TABLE = PrettyTable(['SubscriptionArn', 'Owner', 'Endpoint',
                     'TopicArn', 'Region'])

# Crete EC2 client to list all regions
EC2_CLIENT = boto3.client('ec2')
EC2_RESPONSE = EC2_CLIENT.describe_regions()
REGIONS = [region['RegionName'] for region in EC2_RESPONSE['Regions']]


all_topics = []
result = []


def get_region_from_arn(arn):
    """ Get region from ARN provided """

    return arn.split(":")[3]


def print_subscriptions(subs):
    """ Print subs in PrettyTable """

    for sub in subs:
        TABLE.add_row([sub['SubscriptionArn'], sub['Owner'], sub['Endpoint'],
                      sub['TopicArn'], get_region_from_arn(sub['SubscriptionArn'])])


def list_subscription(region):
    """ List all subscriptions through boto3 pagination """

    sns_client = boto3.client('sns', region_name=region)

    # Paginator to iterate through all results
    list_subscriptions_paginator = sns_client.get_paginator('list_subscriptions')
    response_iterator = list_subscriptions_paginator.paginate()

    for response in response_iterator:
        if response['Subscriptions']:
            print_subscriptions(response['Subscriptions'])


# Start multithreading on individual urls
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = [executor.submit(list_subscription, region) for region in REGIONS]


def lambda_handler(event, context):
    """Main function to return subscriptions under all topics for an account"""

    print("Account Subscriptions")
    print(TABLE)

    return {
        'statusCode': 200,
        'body': json.dumps('Completed execution, check CloudWatch logs')
    }
