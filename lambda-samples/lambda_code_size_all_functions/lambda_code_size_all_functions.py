import json
import boto3

client = boto3.client('lambda')


def total_function_size(function_name, qualifier):

    total_size = 0
    layer_size = 0

    response = client.get_function(
        FunctionName='numpy',
        Qualifier='$LATEST'
    )

    total_size += response['Configuration']['CodeSize']
    print(f"Total code size: {total_size} bytes")

    try:
        for i in response['Configuration']['Layers']:
            layer_size += i['CodeSize']
        print(f"Total layer size: {layer_size} bytes")
        total_size += layer_size
    except:
        pass

    return (round(total_size/1024, 2))


def lambda_handler(event, context):

    function_name = 'numpy'
    qualifier = '$LATEST'

    output = total_function_size(function_name, qualifier)

    print(f"Total function size including layers: {output} MB")

    return {
        'statusCode': 200,
        'body': json.dumps(f'Total function size for function: {function_name} including layers: {output} MB')
    }
