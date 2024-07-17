import datetime
import logging

import pytz  # Added as a Lambda layer
import boto3


logger = logging.getLogger()
logger.setLevel("INFO")

CW_CLIENT = boto3.client("cloudwatch")


def get_seconds(time, source) -> float:
    """Return the delay in seconds"""

    try:
        if source == "s3":
            t1 = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
        else:
            t1 = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as e:
        logger.error(f"Invalid input: 'time' parameter has an incorrect format. {e}")
        raise ValueError("'time' parameter has an incorrect format.") from e

    t2 = datetime.datetime.utcnow()
    return (t2 - t1).total_seconds()


def plot_metric(delay, context) -> None:
    """Plot custom CloudWatch Metric"""

    utc_now = datetime.datetime.now(pytz.utc)
    try:
        CW_CLIENT.put_metric_data(
            Namespace="AWS/Lambda",
            MetricData=[
                {
                    "MetricName": "Async Delay",
                    "Dimensions": [
                        {"Name": context.function_name, "Value": "Async Delay"},
                    ],
                    "Timestamp": utc_now,
                    "Value": delay,
                    "Unit": "Seconds",
                }
            ],
        )
    except Exception as exp:
        logging.error(f"Unknown exception: {exp}")
    else:
        logging.info("Successfully plotted sync metric")


def get_async_delay(event) -> float:
    """
    Return the async invocation delay in seconds

    # S3 payload: https://docs.aws.amazon.com/lambda/latest/dg/with-s3.html
    # CloudWatch Event payload:
    # https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/EventTypes.html#schedule_event_type

    # Each service would invoke the function with it's own payload containing
    # the timestamp when the record was added to the queue which can be used
    # to get the difference in processing times

    return float: delay in seconds
    """

    # For CloudWatch Events:
    try:
        delay = get_seconds(time=event["time"], source="cwe")
    # For S3:
    except KeyError as e:
        delay = get_seconds(time=event["Records"][0]["eventTime"], source="s3")
    return delay


def lambda_handler(event, context):

    delay = get_async_delay(event)
    logging.info(f"Current Async delay is: {delay} seconds")

    plot_metric(delay, context)

    return {"statusCode": 200, "body": f"Current Async delay is: {delay} seconds"}
