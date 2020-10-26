import datetime
import string
import random
import json
import boto3
from prettytable import PrettyTable  # imported from Lambda layer

# PrettyTable
TABLE = PrettyTable(['Region', 'MonthlySpendLimit ($)', 'SMSMonthToDateSpentUSD'])


TIME_DELTA = datetime.timedelta(hours=1)
TODAY = datetime.date.today()
YESTERDAY = datetime.datetime(TODAY.year, TODAY.month, TODAY.day) - TIME_DELTA
TODAY = datetime.datetime(TODAY.year, TODAY.month, TODAY.day)
REGIONS = ['us-east-2', 'us-east-1', 'us-west-1', 'us-west-2', 'ap-south-1', 'ap-southeast-1', 'ap-southeast-2', 'ap-northeast-1', 'ca-central-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'eu-west-3', 'eu-north-1', 'me-south-1', 'sa-east-1', 'us-gov-west-1']
# Regions from: https://docs.aws.amazon.com/sns/latest/dg/sns-supported-regions-countries.html


def get_sms_cost(region):
    """Get SMS Metrics"""

    # AWS SDK Clients
    cloudwatch_client = boto3.client('cloudwatch', region_name=region)
    sns_client = boto3.client('sns', region_name=region)

    cw_id = random.choice(string.ascii_lowercase) + random.choice(string.ascii_uppercase)
    try:
        cw_response = cloudwatch_client.get_metric_data(
            MetricDataQueries=[
                {
                    'Id': cw_id,
                    'MetricStat': {
                        'Metric': {
                            'Namespace': 'AWS/SNS',
                            'MetricName': 'SMSMonthToDateSpentUSD'
                        },
                        'Period': 300,
                        'Stat': 'Maximum'
                    },
                    'Label': 'SMSMonthToDateSpentUSD',
                    'ReturnData': True,
                },
            ],
            EndTime=TODAY,
            StartTime=YESTERDAY
        )
        cw_value = cw_response['MetricDataResults'][0]['Values'][0]
    except IndexError:
        cw_value = '0'
    except Exception as exp:
        cw_value = f'Account not configured for {region}'

    try:
        sns_response = sns_client.get_sms_attributes()
        sns_value = sns_response['attributes']['MonthlySpendLimit']
    except Exception as exp:
        if region == 'us-gov-west-1':
            sns_value = f'Account not configured for {region}'
        else:
            sns_value = 'Default: $1'

    TABLE.add_row([region, sns_value, cw_value])


def lambda_handler(event, context):
    """Main Function"""

    for region in REGIONS:
        get_sms_cost(region)

    print(TABLE)
    return {
        'statusCode': 200,
        'body': json.dumps('Check CloudWatch logs.')
    }
