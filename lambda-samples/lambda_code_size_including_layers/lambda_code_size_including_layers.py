import json
import boto3

# imported from Lambda layer
from prettytable import PrettyTable

CLIENT = boto3.client('lambda')

# Update the Function name and the Qualier (Version/Alias)

FUNCTION_NAME = '<enter-function-name>'
QUALIFIER = '$LATEST'

# PrettyTable
TABLE = PrettyTable()


def format_size(size):
    """ Format into byes, KB, MB & GB """

    power = 2**10
    i = 0
    power_labels = {0: 'bytes', 1: 'KB', 2: 'MB', 3: 'GB'}
    while size > power:
        size /= power
        i += 1
    return f"{round(size, 2)} {power_labels[i]}"


def total_function_size(function_name, qualifier):
    """ Get function metadata """
    total_size = 0
    layer_size = 0

    response = CLIENT.get_function(
        FunctionName=function_name,
        Qualifier=qualifier
    )

    total_size += response['Configuration']['CodeSize']
    TABLE.add_column("Code Size", [format_size(total_size)])

    try:
        for i in response['Configuration']['Layers']:
            layer_size += i['CodeSize']
        TABLE.add_column("Layer Size", [format_size(layer_size)])
        total_size += layer_size
    except Exception as e:
        print(e)

    return total_size


def lambda_handler(event, context):
    """ Main function """

    total_size = total_function_size(FUNCTION_NAME, QUALIFIER)

    TABLE.add_column("Total function size", [format_size(total_size)])
    print(f"Total function size for function: {FUNCTION_NAME}:{QUALIFIER} version")

    print(TABLE)

    total_size = round(total_size / 1024 / 1024, 2)
    return {
        'statusCode': 200,
        'body': json.dumps(f'Total function size for function: {FUNCTION_NAME} including layers: {total_size} MB')
    }
