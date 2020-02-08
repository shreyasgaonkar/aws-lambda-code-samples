import json
import boto3
import random
import time
client = boto3.client('sns')


def lambda_handler(event, context):

    # Default limit in an account is 200 subscription filters. Need to interate this more if any numbers overlap
    for i in range(300):
        print(f"Called {i} times")

        # Generate random US phone endpoints to replicate random numbers
        phoneNumber = print(f"+1{random.randint(1000000000, 9999999999)}")

        # Filter Policy as per: https://docs.aws.amazon.com/sns/latest/dg/sns-subscription-filter-policies.html#policy-accepts-messages
        response = client.subscribe(
            TopicArn='<your-topic-arn>',
            Protocol='sms',
            Endpoint=phoneNumber,
            Attributes={
                "FilterPolicy": '{"first": ["1"], "second": ["2"]}'
            },
            ReturnSubscriptionArn=True
        )

        # Sleep to ensure we do not cross the API limit and get ourselves throttled
        time.sleep(0.5)
    return {
        'statusCode': 200,
        'body': json.dumps('Completed!')
    }
