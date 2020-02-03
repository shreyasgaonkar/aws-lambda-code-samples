import datetime
import boto3
client = boto3.client('cloudwatch')


def lambda_handler(event, context):
    """Main Function"""

    # Event as per: https://docs.aws.amazon.com/lambda/latest/dg/with-s3.html

    # Each service would invoke the function with it's own payload containing
    # the timestamp when the record was added to the queue which can be used
    # to get the difference in processing times

    delay = getSeconds(event['Records'][0]['eventTime'])
    print(f"Current Async delay is: {delay} seconds")
    plotMetric(delay)

    return {
        'statusCode': 200,
        'body': f"Current Async delay is: {delay} seconds"
    }


def getSeconds(time):
    t1 = (datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%fZ'))
    t2 = (datetime.datetime.utcnow())
    return((t2-t1).total_seconds())


def plotMetric(delay):
    client.put_metric_data(
        Namespace='AWS/Lambda',
        MetricData=[
            {
                'MetricName': 'Async Delay',
                'Dimensions': [
                    {
                        'Name': 'Async Delay',
                        'Value': 'Async Delay'
                    },
                ],
                'Timestamp': datetime.datetime.now(),
                'Value': delay,
                'Unit': 'Seconds'
            }
        ]
    )
