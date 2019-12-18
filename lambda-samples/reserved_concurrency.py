import json
import boto3

# Use paginator from:
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/paginators.html#filtering-results
# to call recursively on the same API call if next token is returned.

client = boto3.client('lambda')
paginator = client.get_paginator('list_functions')

# Create an empty set to dump all the individual function's data
reserved_concurrency = set()


def lambda_handler(event, context):
    """ Main function to retrieve reserved concurrency """

    page_iterator = paginator.paginate()
    for page in page_iterator:
        functions = page['Functions']

        for function in functions:
            response = client.get_function_concurrency(
                FunctionName=function['FunctionName']
            )

            try:
                funct = {
                    "Name": function['FunctionName'],
                    "Concurrency": response['ReservedConcurrentExecutions']
                }
                funct = json.dumps(funct)
                reserved_concurrency.add(funct)

            except:
                pass

    for i in sorted(reserved_concurrency):
        i = json.loads(i)
        print(f"{i['Name']}: {i['Concurrency']}")

    return {
        'statusCode': 200,
        'body': json.dumps('Completed execution')
    }
