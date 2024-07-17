import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel("INFO")

ALL_FUNCTIONS = set()

LAMBDA_CLIENT = boto3.client("lambda")
PAGINATOR = LAMBDA_CLIENT.get_paginator("list_functions")

# Make sure ALL versions are returned
OPERATION_PARAMETERS = {"FunctionVersion": "ALL"}
page_iterator = PAGINATOR.paginate(**OPERATION_PARAMETERS)

# Calling this from outside handler will significantly speed up the function (766 ms -> 39 ms)
for page in page_iterator:
    functions = page["Functions"]

    for function in functions:
        funct = {"Name": function["FunctionName"], "Version": function["Version"], "CodeSize": function["CodeSize"]}
        ALL_FUNCTIONS.add(json.dumps(funct))

def convert_bytes_to_mb(size, round_size=2):
    return round(size / 1024 / 1024, round_size)


def get_all_function_size() -> float:

    total_function_size = 0
    for function in sorted(ALL_FUNCTIONS):
        function = json.loads(function)
        logger.info(f"Function Name: {function["Name"]:48} Function Version: {function["Version"]:8} Code Size (MB): {convert_bytes_to_mb(function["CodeSize"], 4)}")
        total_function_size += function["CodeSize"]

    return convert_bytes_to_mb(total_function_size)


def lambda_handler(event, context):
    """Main Function"""

    total_function_size = get_all_function_size()

    data = f"Lambda code storage: {str(total_function_size)} MB"
    return {"statusCode": 200, "body": json.dumps(data)}
