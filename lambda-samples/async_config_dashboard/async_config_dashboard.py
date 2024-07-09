import json
import logging
import os

import boto3
from prettytable import PrettyTable  # Imported as a Lambda layer

# PrettyTable
TABLE = PrettyTable(
    [
        "Function Name",
        "Max Retry Attempts",
        "Maximum event age (seconds)",
        "On success destination",
        "On failure destination",
        "Last Modified",
    ]
)

LAMBDA_CLIENT = boto3.client("lambda")
PAGINATOR = LAMBDA_CLIENT.get_paginator("list_functions")
OPERATION_PARAMETERS = {"FunctionVersion": "ALL"}

logger = logging.getLogger()
logger.setLevel("INFO")


def get_destination_config(response):
    """Verify if destination configurations exists"""

    on_success = response["DestinationConfig"]["OnSuccess"].get("Destination", "NOT SET")
    on_failure = response["DestinationConfig"]["OnFailure"].get("Destination", "NOT SET")

    # Check if max age is set
    try:
        max_event_age = response.get("MaximumEventAgeInSeconds", 21600)
    except Exception as exp:
        logging.info(f"Error: {exp}")
        max_event_age = -1  # invalid state

    return on_success, on_failure, max_event_age


def log_function_details(function) -> None:
    """Get and log function details into pretty table"""

    logger.info(f"Getting configurations for function: {function['FunctionName']}")
    try:
        response = LAMBDA_CLIENT.get_function_event_invoke_config(
            FunctionName=function["FunctionName"], Qualifier=function["Version"]
        )

        on_success, on_failure, max_event_age = get_destination_config(response)

        # Check if max retry attempts are set
        try:
            if response["MaximumRetryAttempts"]:
                max_retry = response["MaximumRetryAttempts"]
        except KeyError:
            max_retry = 2  # Default retry is 2 for async invokes
        except Exception as exp:
            logging.info(f"Error: {exp}")

        TABLE.add_row(
            [
                function["FunctionName"],
                max_retry,
                max_event_age,
                on_success,
                on_failure,
                response["LastModified"],
            ]
        )

    except LAMBDA_CLIENT.exceptions.ResourceNotFoundException as exp:
        logger.info(f"Resource not found for {function['FunctionName']} - {exp}")
    except Exception as exp:
        print(f'{exp} for {function["FunctionName"]}')
        print(response)


def get_async_configs() -> None:
    """Retrieve async configurations for all functions and versions in a region"""

    page_iterator = PAGINATOR.paginate(**OPERATION_PARAMETERS)
    for page in page_iterator:
        functions = page["Functions"]
        for function in functions:
            log_function_details(function)

    print(TABLE)


def lambda_handler(event, context):
    """Main function"""

    logger.info(f"Starting request to find async configurations for all Lambda functions in {os.environ['AWS_REGION']}")
    get_async_configs()

    return {"statusCode": 200, "body": json.dumps("Check CloudWatch logs")}
