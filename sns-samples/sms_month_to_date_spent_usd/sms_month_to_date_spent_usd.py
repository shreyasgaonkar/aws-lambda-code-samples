import datetime
import string
import random
import json
import boto3
from prettytable import PrettyTable  # imported from Lambda layer

# PrettyTable
TABLE = PrettyTable(["Region", "MonthlySpendLimit ($)", "SMSMonthToDateSpentUSD"])


START_TIME = datetime.datetime.utcnow() - datetime.timedelta(hours=1)
END_TIME = datetime.datetime.utcnow()


REGIONS = [
    "us-east-2",
    "us-east-1",
    "us-west-1",
    "us-west-2",
    "af-south-1",
    "ap-south-1",
    "ap-northeast-3",
    "ap-southeast-1",
    "ap-southeast-2",
    "ap-northeast-1",
    "ca-central-1",
    "eu-central-1",
    "eu-west-1",
    "eu-west-2",
    "eu-west-3",
    "eu-south-1",
    "eu-north-1",
    "me-south-1",
    "sa-east-1",
    "us-gov-east-1",
    "us-gov-west-1",
]
# Hardcoded to include us-gov-west-1 region
# Regions from: https://docs.aws.amazon.com/sns/latest/dg/sns-supported-regions-countries.html


def check_monthly_spend_limits(region, sns_client, cw_value):
    # Check MonthlySpendLimit
    try:
        sns_response = sns_client.get_sms_attributes()
        sns_value = f"${sns_response['attributes']['MonthlySpendLimit']}"
    except Exception as exp:
        if region in ["us-gov-west-1", "me-south-1"]:
            sns_value = f"Account not configured for {region}"
        else:
            sns_value = "Default: $1"

    TABLE.add_row([region, sns_value, cw_value])


def get_sms_cost(region):
    """Get SMS Metrics"""

    # AWS SDK Clients
    cloudwatch_client = boto3.client("cloudwatch", region_name=region)
    sns_client = boto3.client("sns", region_name=region)

    cw_id = random.choice(string.ascii_lowercase) + random.choice(
        string.ascii_uppercase
    )
    try:
        cw_response = cloudwatch_client.get_metric_data(
            MetricDataQueries=[
                {
                    "Id": cw_id,
                    "MetricStat": {
                        "Metric": {
                            "Namespace": "AWS/SNS",
                            "MetricName": "SMSMonthToDateSpentUSD",
                        },
                        "Period": 300,
                        "Stat": "Maximum",
                    },
                    "Label": "SMSMonthToDateSpentUSD",
                    "ReturnData": True,
                },
            ],
            EndTime=END_TIME,
            StartTime=START_TIME,
        )
        cw_value = f"${cw_response['MetricDataResults'][0]['Values'][0]}"
    except IndexError:
        cw_value = "$0"
    except Exception as exp:
        cw_value = f"Account not configured for {region}"

    check_monthly_spend_limits(region, sns_client, cw_value)


def lambda_handler(event, context):
    """Main Function"""

    for region in REGIONS:
        get_sms_cost(region)

    print(TABLE)
    return {"statusCode": 200, "body": json.dumps("Check CloudWatch logs.")}
