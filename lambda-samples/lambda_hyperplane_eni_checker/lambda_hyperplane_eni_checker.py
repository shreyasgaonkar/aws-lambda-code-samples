import json
import boto3


region = 'us-west-2'
eni_name = 'eni-XXXXXXXXXXXXXXXXX'

ec2 = boto3.client('ec2', region_name=region)
client = boto3.client('lambda', region_name=region)
paginator = client.get_paginator('list_functions')

# Make sure ALL versions are returned
operation_parameters = {'FunctionVersion': 'ALL'}

# Create an empty set to dump all the individual function's data
allFunctions = set()


def find_eni(eni_id):
    response = ec2.describe_network_interfaces(
        Filters=[
            {
                'Name': 'network-interface-id',
                'Values': [eni_id]
            }
        ]
    )
    return response


def find_functions(eni_response):
    """ Find all functions using that ENI """

    # Functions should be using the exact SGs as that of ENI
    # ENI's subnet must be a part of Lambda's subnet group

    # SDK calls are paginated, they can be unpacked with paginators
    page_iterator = paginator.paginate(**operation_parameters)
    for page in page_iterator:
        functions = page['Functions']

        for function in functions:
            try:
                # is this function in VPC?
                if function['VpcConfig']['VpcId']:

                    # Does the SG match?
                    if len(function['VpcConfig']['SecurityGroupIds']) == len(eni_response['Groups']):

                        # Sort and check if they match
                        eni_security_groups = [i['GroupId'] for i in eni_response['Groups']]
                        if eni_security_groups.sort() == function['VpcConfig']['SecurityGroupIds'].sort():

                            # is Lambda's subnet a part of ENI's subnet?
                            if eni_response['SubnetId'] in function['VpcConfig']['SubnetIds']:
                                funct = json.dumps(function)
                                allFunctions.add(funct)

            except Exception as e:
                print(e)


def format_function(allFunctions, eni_response):
    print("\n")
    print(f"Lambda function(s) using ENI: {eni_response['NetworkInterfaceId']}:\n")
    for function in allFunctions:
        functionData = json.loads(function)
        print(functionData['FunctionArn'])
    print("\n")


def lambda_handler(event, context):

    eni_response = find_eni(eni_name)
    eni_response = eni_response['NetworkInterfaces']

    # ENI exists?
    if len(eni_response) > 0:
        eni_response = eni_response[0]

        # Find and format function associated to this ENI
        find_functions(eni_response)
        format_function(allFunctions, eni_response)

    else:
        return {
            'statusCode': 200,
            'body': f"ENI: {eni_name} not found in {region}"
        }

    return {
        'statusCode': 200,
        'body': "See function logs"
    }
