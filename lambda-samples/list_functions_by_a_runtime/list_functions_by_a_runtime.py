import json
import boto3
from prettytable import PrettyTable  # imported as a Lambda Layer


# PrettyTable
TABLE = PrettyTable(['Function Arn', 'Function Name', 'Runtime'])

REGION_NAME = 'us-east-1'
LAMBDA_CLIENT = boto3.client('lambda', region_name=REGION_NAME.lower())
PAGINATOR = LAMBDA_CLIENT.get_paginator('list_functions')
OPERATION_PARAMETERS = {'FunctionVersion': 'ALL'}

RUNTIMES_TO_LIST = 'python2.7'


def lambda_handler(event, context):
    """Main function"""
    count = 0
    page_iterator = PAGINATOR.paginate(**OPERATION_PARAMETERS)
    for page in page_iterator:
        functions = page['Functions']
        for function in functions:
            try:
                if function['Runtime'] == RUNTIMES_TO_LIST.lower():
                    TABLE.add_row([function['FunctionArn'],
                                   function['FunctionName'], function['Runtime']])
                    count += 1
            except KeyError:
                pass
    print(TABLE)
    print(f'Total Lambda function versions using {RUNTIMES_TO_LIST} Runtime: {count}')

    return {
        'statusCode': 200,
        'body': json.dumps('Check CloudWatch logs')
    }
