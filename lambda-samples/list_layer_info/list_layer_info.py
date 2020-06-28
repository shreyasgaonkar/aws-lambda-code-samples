import re
import json
import boto3
from prettytable import PrettyTable

# PrettyTable
TABLE = PrettyTable(['LayerARN', 'Version', 'CodeSize (MB)',
                     'Compatible Runtimes'])

LAMBDA_CLIENT = boto3.client('lambda')
LIST_LAYER_PAGINATOR = LAMBDA_CLIENT.get_paginator('list_layers')
LIST_LAYER_VERSIONS_PAGINATOR = LAMBDA_CLIENT.get_paginator('list_layer_versions')

ALL_LAYERS = []


def lambda_handler(event, context):
    """ Main function to return Lambda Layer information """

    response_iterator = LIST_LAYER_PAGINATOR.paginate()
    for layers_value in response_iterator:
        layers = layers_value['Layers']

    for layer in layers:
        response_iterator = LIST_LAYER_VERSIONS_PAGINATOR.paginate(
            LayerName=layer['LayerArn']
        )
        for layer_value in response_iterator:
            response = layer_value

        for i in response['LayerVersions']:

            layer_arn = re.split(r':', i['LayerVersionArn'])
            layer_arn = ":".join(layer_arn[:-1])

            response = LAMBDA_CLIENT.get_layer_version(
                LayerName=layer_arn,
                VersionNumber=i['Version']
            )
            temp = {
                'LayerArn': response['LayerArn'],
                'Version': response['Version'],
                'CodeSize': str(round(float(response['Content']['CodeSize']) / 1024 / 1024, 2)),
                'Compatible Runtimes': response['CompatibleRuntimes']
            }
            TABLE.add_row([temp['LayerArn'], temp['Version'],
                           temp['CodeSize'], temp['Compatible Runtimes']])
            ALL_LAYERS.append(json.dumps(temp))

    # Print PrettyTable
    print(TABLE)

    return {
        'statusCode': 200,
        'body': json.dumps('See function logs')
    }
