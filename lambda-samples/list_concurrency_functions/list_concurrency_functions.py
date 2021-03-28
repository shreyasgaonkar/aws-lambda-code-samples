import json
import os
import time
import collections
import boto3
from prettytable import PrettyTable

# Use paginator from:
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/paginators.html#filtering-results
# to call recursively on the same API call if next token is returned.

# ==================
# Override AWS Region below, otherwise will use Lambda function's region

# REGION_NAME = 'us-east-1'
# ==================

try:
    REGION_NAME
except NameError:
    REGION_NAME = os.environ['AWS_REGION']

LAMBDA_CLIENT = boto3.client('lambda', region_name=REGION_NAME)
PAGINATOR = LAMBDA_CLIENT.get_paginator('list_functions')

# Make sure ALL versions are returned for provisioned concurrency
OPERATION_PARAMETERS = {'FunctionVersion': 'ALL'}

# Create an empty set to dump all the individual function's data
RESERVED_CONCURRENCY = set()
PROVISIONED_CONCURRENCY = {}

# PrettyTable
PROVISIONED_CONCURRENCY_TABLE = PrettyTable(['FunctionArn', 'Requested', 'Available',
                                             'Allocated', 'Status', 'Last Modified'])
RESERVED_CONCURRENCY_TABLE = PrettyTable(['Function Name', 'Reserved Concurrency'])


def list_provisioned_concurrency():
    """Helper function to determine Provisioned Concurrency"""

    # List all functions
    page_iterator = PAGINATOR.paginate()
    for page in page_iterator:
        functions = page['Functions']

        for function in functions:
            response = LAMBDA_CLIENT.list_provisioned_concurrency_configs(
                FunctionName=function['FunctionName']
            )

            if response['ProvisionedConcurrencyConfigs']:
                for i in response['ProvisionedConcurrencyConfigs']:
                    PROVISIONED_CONCURRENCY[i['FunctionArn']] = [
                        i['RequestedProvisionedConcurrentExecutions'], i['AvailableProvisionedConcurrentExecutions'], i['AllocatedProvisionedConcurrentExecutions'], i['Status'], i['LastModified']]
            else:
                time.sleep(0.1)

            # Check for Reserved Concurrency
            list_reserved_concurrency(function['FunctionName'])

    # print(PROVISIONED_CONCURRENCY)


def list_reserved_concurrency(function_name):
    response = LAMBDA_CLIENT.get_function_concurrency(
        FunctionName=function_name
    )
    try:
        funct = {
            "Name": function_name,
            "Reserved Concurrency": response['ReservedConcurrentExecutions']
        }
        funct = json.dumps(funct)
        RESERVED_CONCURRENCY.add(funct)

    except Exception:
        pass

    return True


def print_function():
    """Print function data"""
    print("Per function Reserved concurrency:\n")
    count = 0
    for i in sorted(RESERVED_CONCURRENCY):
        i = json.loads(i)
        # print(f"{i['Name']} - {i['Reserved Concurrency']}")
        count += i['Reserved Concurrency']
        RESERVED_CONCURRENCY_TABLE.add_row([i['Name'], i['Reserved Concurrency']])
    print(f"Total reserved concurrency in {os.environ['AWS_REGION']} region is {count}")
    print(RESERVED_CONCURRENCY_TABLE)
    print("\n=====================\n")

    print("Per qualifier Provisioned concurrency:\n")
    count = 0
    sorted_pc = collections.OrderedDict(sorted(PROVISIONED_CONCURRENCY.items()))
    for key, value in sorted_pc.items():
        PROVISIONED_CONCURRENCY_TABLE.add_row(
            [key, value[0], value[1], value[2], value[3], value[4]])
        count += value[0]
    print(f"Total provisioned concurrency in {os.environ['AWS_REGION']} region is {count}")
    print(PROVISIONED_CONCURRENCY_TABLE)


def lambda_handler(event, context):
    """ Main function to retrieve reserved concurrency """

    list_provisioned_concurrency()
    print_function()

    return {
        'statusCode': 200,
        'body': json.dumps('Completed execution, see function logs.')
    }
