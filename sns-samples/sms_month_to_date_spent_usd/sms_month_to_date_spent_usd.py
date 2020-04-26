import json
import boto3
import datetime
import string
import random
from prettytable import PrettyTable  # imported from Lambda layer

# PrettyTable
TABLE = PrettyTable(['Metric', 'Value ($)'])

# AWS SDK Clients
CLOUDWATCH = boto3.client('cloudwatch')
SNS = boto3.client('sns')

TIME_DELTA = datetime.timedelta(hours=1)
TODAY = datetime.date.today()
YESTERDAY = datetime.datetime(TODAY.year, TODAY.month, TODAY.day) - TIME_DELTA
TODAY = datetime.datetime(TODAY.year, TODAY.month, TODAY.day)


def get_sms_cost():
    """Get CloudWatch Metric"""
    id = random.choice(string.ascii_lowercase) + random.choice(string.ascii_uppercase)
    cw_response = CLOUDWATCH.get_metric_data(
        MetricDataQueries=[
            {
                'Id': id,
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
    sns_response = SNS.get_sms_attributes()
    TABLE.add_row(['MonthlySpendLimit', sns_response['attributes']['MonthlySpendLimit']])
    TABLE.add_row(['SMSMonthToDateSpentUSD', cw_response['MetricDataResults'][0]['Values'][0]])
    print(TABLE)


def lambda_handler(event, context):
    get_sms_cost()
    return {
        'statusCode': 200,
        'body': json.dumps('Check CloudWatch logs.')
    }
