import re
import json
import boto3


client = boto3.client('lambda')
list_layer_paginator = client.get_paginator('list_layers')
list_layer_versions_paginator = client.get_paginator('list_layer_versions')

all_layers = []


def lambda_handler(event, context):
    """ Main function to return Lambda Layer information """

    response_iterator = list_layer_paginator.paginate()
    for layers_value in response_iterator:
        layers = layers_value['Layers']

    for layer in layers:
        response_iterator = list_layer_versions_paginator.paginate(
            LayerName=layer['LayerArn']
        )
        for layer_value in response_iterator:
            response = layer_value

        for i in response['LayerVersions']:

            layer_arn = re.split(r':', i['LayerVersionArn'])
            layer_arn = ":".join(layer_arn[:-1])

            response = client.get_layer_version(
                LayerName=layer_arn,
                VersionNumber=i['Version']
            )
            temp = {
                'LayerArn': response['LayerArn'],
                'Version': response['Version'],
                'CodeSize': response['Content']['CodeSize'],
                'Compatible Runtimes': response['CompatibleRuntimes']
            }
            all_layers.append(json.dumps(temp))

    for layer_info in all_layers:
        print(layer_info)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
