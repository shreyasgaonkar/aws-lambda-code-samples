import json
import boto3
from prettytable import PrettyTable  # Imported as a Lambda layer

# PrettyTable
TABLE = PrettyTable(['Function Name', 'Max Retry Attempts', 'Maximum event age (seconds)',
                     'On success destination', 'On failure destination', 'Last Modified'])

LAMBDA_CLIENT = boto3.client('lambda')
PAGINATOR = LAMBDA_CLIENT.get_paginator('list_functions')
OPERATION_PARAMETERS = {'FunctionVersion': 'ALL'}


def get_async_configs():
    """Retrieve async configurations for all functions and versions in a region"""
    page_iterator = PAGINATOR.paginate(**OPERATION_PARAMETERS)
    for page in page_iterator:
        functions = page['Functions']
        for function in functions:
            try:
                response = LAMBDA_CLIENT.get_function_event_invoke_config(
                    FunctionName=function['FunctionName'],
                    Qualifier=function['Version']
                )

                # Check if Destination configs are set
                if len(response['DestinationConfig']['OnSuccess']) == 0:
                    on_success = 'NOT SET'
                else:
                    on_success = response['DestinationConfig']['OnSuccess']['Destination']
                if len(response['DestinationConfig']['OnFailure']) == 0:
                    on_failure = 'NOT SET'
                else:
                    on_failure = response['DestinationConfig']['OnFailure']['Destination']

                # Check if max age is set
                try:
                    if response['MaximumEventAgeInSeconds']:
                        max_event_age = response['MaximumEventAgeInSeconds']
                except KeyError:
                    max_event_age = 21600  # 6 hours
                except Exception as exp:
                    print(f'Error: {exp}')

                # Check if max retry attempts are set
                try:
                    if response['MaximumRetryAttempts']:
                        max_retry = response['MaximumRetryAttempts']
                except KeyError:
                    max_retry = 2  # Default retry is 2 for async invokes
                except Exception as exp:
                    print(f'Error: {exp}')

                TABLE.add_row([function['FunctionName'], max_retry, max_event_age,
                               on_success, on_failure, response['LastModified']])

            except LAMBDA_CLIENT.exceptions.ResourceNotFoundException:
                pass
            except Exception as exp:
                print(f'{exp} for {function["FunctionName"]}')
                print(response)


def lambda_handler(event, context):
    """Main function"""

    get_async_configs()
    print(TABLE)

    return {
        'statusCode': 200,
        'body': json.dumps('Check CloudWatch logs')
    }
