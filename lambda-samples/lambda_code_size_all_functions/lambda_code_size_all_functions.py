import json
import boto3

# Use paginator from:
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/paginators.html#filtering-results
# to call recursively on the same API call if next token is returned.

LAMBDA_CLIENT = boto3.client('lambda')
PAGINATOR = LAMBDA_CLIENT.get_paginator('list_functions')

# Make sure ALL versions are returned
OPERATION_PARAMETERS = {'FunctionVersion': 'ALL'}

# Create an empty set to dump all the individual function's data
ALL_FUNCTIONS = set()


def lambda_handler(event, context):
    """Main Function"""
    page_iterator = PAGINATOR.paginate(**OPERATION_PARAMETERS)
    for page in page_iterator:
        functions = page['Functions']

        for function in functions:
            funct = {
                "Name": function['FunctionName'],
                "Version": function['Version'],
                "CodeSize": function['CodeSize']
            }

            funct = json.dumps(funct)
            ALL_FUNCTIONS.add(funct)

    total = 0
    for i in sorted(ALL_FUNCTIONS):
        i = json.loads(i)
        print("{function:48}:{version:8} {size:,.2f}".format(
            function=i['Name'], version=i['Version'], size=i['CodeSize']))
        total += i['CodeSize']

    # Convert bytes to MB
    total = total / 1024 / 1024

    data = "Lambda code storage: {}".format(str(total))
    print(data)
    return {
        'statusCode': 200,
        'body': json.dumps(data)
    }
