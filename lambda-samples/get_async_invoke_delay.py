import datetime


def lambda_handler(event, context):
    """Main Function"""

    # Event as per: https://docs.aws.amazon.com/lambda/latest/dg/with-s3.html

    # Each service would invoke the function with it's own payload containing
    # the timestamp when the record was added to the queue which can be used
    # to get the difference in processing times

    return {
        'statusCode': 200,
        'body': f"Delay is {getSeconds(event['Records'][0]['eventTime'])} seconds"
    }


def getSeconds(time):
    t1 = (datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%fZ'))
    t2 = (datetime.datetime.utcnow())
    return((t2-t1).total_seconds())
