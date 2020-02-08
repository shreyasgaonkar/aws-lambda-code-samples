import json
import boto3

# Use paginator from:
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/paginators.html#filtering-results
# to call recursively on the same API call if next token is returned.

client = boto3.client('lambda')
paginator = client.get_paginator('list_functions')

# Make sure ALL versions are returned
operation_parameters = {'FunctionVersion': 'ALL'}

# Create an empty set to dump all the individual function's data
allFunctions = set()


def lambda_handler(event, context):

    page_iterator = paginator.paginate(**operation_parameters)
    for page in page_iterator:
        functions = page['Functions']

        for function in functions:
            funct = {
                "Name": function['FunctionName'],
                "Version": function['Version'],
                "CodeSize": function['CodeSize']
            }

            funct = json.dumps(funct)
            allFunctions.add(funct)

    total = 0
    for i in sorted(allFunctions):
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
