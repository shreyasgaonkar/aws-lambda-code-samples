import json
import datetime
import base64
import boto3
import StringIO
import gzip
import re

# Create CloudWatch client for making SDK calls to log function's memory metric
client = boto3.client('cloudwatch')


def lambda_handler(event, context):

    MaxMem = ""
    Mem = ""

    data = event['awslogs']['data']
    data = base64.b64decode(data)
    striodata = StringIO.StringIO(data)
    with gzip.GzipFile(fileobj=striodata, mode='r') as f:
        data = json.loads(f.read())
        message = str(data['logEvents'][0]['message'])

        match = re.split(r'(Max Memory Used:)', message)
        temp = (match[-1])
        temp = temp.split(" ")
        MaxMem = int(temp[1])
        print("Max Memory Used: {}".format(MaxMem))

        match = re.split(r'(Memory Size:)', message)
        match = match[-1]
        match = match.split(" ")
        Mem = match[1]
        print("Total Memory: {}".format(Mem))

    todayDate = datetime.datetime.now()

    MaxMem = int(MaxMem)
    Mem = int(Mem)

    response = client.put_metric_data(
        Namespace='AWS/Lambda',
        MetricData=[
            {
                'MetricName': 'Memory Usage',
                'Dimensions': [
                    {
                        'Name': 'MB',
                        'Value': 'Max Memory used'
                    },
                ],
                'Timestamp': todayDate,
                'Value': MaxMem,
                'Unit': 'Megabytes'
            },
            {
                'MetricName': 'Memory Usage',
                'Dimensions': [
                    {
                        'Name': 'MB',
                        'Value': 'Function Memory'
                    },
                ],
                'Timestamp': todayDate,
                'Value': Mem,
                'Unit': 'Megabytes'
            }
        ]
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Completed execution')
    }
