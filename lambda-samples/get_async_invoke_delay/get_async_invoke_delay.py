import datetime
import boto3
client = boto3.client('cloudwatch')


def lambda_handler(event, context):
    """Main Function"""

    # S3 payload: https://docs.aws.amazon.com/lambda/latest/dg/with-s3.html
    # CloudWatch Event payload:
    # https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/EventTypes.html#schedule_event_type

    # Each service would invoke the function with it's own payload containing
    # the timestamp when the record was added to the queue which can be used
    # to get the difference in processing times

    # For CloudWatch Events:
    try:
        source = 'cwe'
        delay = getSeconds(event['time'], source)
    except KeyError as e:
        # Key not a part of the payload
        print(e)
        # For S3:
        source = 's3'
        delay = getSeconds(event['Records'][0]['eventTime'], source)

    # 'source' variable determines how the datetime object is disassembled in
    # getSeconds() function

    print(f"Current Async delay is: {delay} seconds")
    plotMetric(delay, context)

    return {
        'statusCode': 200,
        'body': f"Current Async delay is: {delay} seconds"
    }


def getSeconds(time, source):

    if(source == 's3'):
        t1 = (datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ'))
    else:
        t1 = (datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%fZ'))

    t2 = (datetime.datetime.utcnow())
    return((t2-t1).total_seconds())


def plotMetric(delay, context):
    client.put_metric_data(
        Namespace='AWS/Lambda',
        MetricData=[
            {
                'MetricName': 'Async Delay',
                'Dimensions': [
                    {
                        'Name': context.function_name,
                        'Value': 'Async Delay'
                    },
                ],
                'Timestamp': datetime.datetime.now(),
                'Value': delay,
                'Unit': 'Seconds'
            }
        ]
    )
