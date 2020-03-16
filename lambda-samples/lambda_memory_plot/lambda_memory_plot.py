import json
import datetime
import boto3
import base64
import StringIO
import gzip
import re

client = boto3.client('cloudwatch')


def lambda_handler(event, context):

    MaxMem = ""
    Mem = ""

    data = event['awslogs']['data']
    data = base64.b64decode(data)
    striodata = StringIO.StringIO(data)
    with gzip.GzipFile(fileobj=striodata, mode='r') as f:
        data = json.loads(f.read())

        # Get function name from the CloudWatch group
        function_name = re.split(r'(/aws/lambda/)', data['logGroup'])
        function_name = function_name[-1]

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

    MaxMem = int(MaxMem)
    Mem = int(Mem)

    client.put_metric_data(
        Namespace='AWS/Lambda',
        MetricData=[
            {
                'MetricName': 'Memory Usage',
                'Dimensions': [
                    {
                        'Name': 'Memory Usage',
                        'Value': function_name + ': Max Memory used'
                    },
                ],
                'Timestamp': datetime.datetime.now(),
                'Value': MaxMem,
                'Unit': 'Megabytes'
            },
            {
                'MetricName': 'Memory Usage',
                'Dimensions': [
                    {
                        'Name': 'Memory Usage',
                        'Value': function_name + ': Function Memory'
                    },
                ],
                'Timestamp': datetime.datetime.now(),
                'Value': Mem,
                'Unit': 'Megabytes'
            }
        ]
    )
