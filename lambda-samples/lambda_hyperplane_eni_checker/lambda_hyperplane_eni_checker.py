import json
import boto3


REGION_NAME = 'us-west-2'
ENI_ID = 'eni-XXXXXXXXXXXXXXXXX'

EC2_CLIENT = boto3.client('ec2', region_name=REGION_NAME)
LAMBDA_CLIENT = boto3.client('lambda', region_name=REGION_NAME)
PAGINATOR = LAMBDA_CLIENT.get_paginator('list_functions')

# Make sure ALL versions are returned
OPERATION_PARAMETERS = {'FunctionVersion': 'ALL'}

# Create an empty set to dump all the individual function's data
ALL_FUNCTIONS = set()


def find_eni(eni_id):
    """Find ENI metadata"""
    response = EC2_CLIENT.describe_network_interfaces(
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
    page_iterator = PAGINATOR.paginate(**OPERATION_PARAMETERS)
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
                                ALL_FUNCTIONS.add(funct)

            except Exception as e:
                pass


def format_function(all_functions, eni_response):
    """Format function data"""
    print(f"Lambda function(s) using ENI: {eni_response['NetworkInterfaceId']}:\n")
    for function in all_functions:
        function_data = json.loads(function)
        print(function_data['FunctionArn'])
    print("")


def lambda_handler(event, context):
    """Main function"""
    eni_response = find_eni(ENI_ID)
    eni_response = eni_response['NetworkInterfaces']

    # ENI exists?
    if eni_response:
        eni_response = eni_response[0]

        # Find and format function associated to this ENI
        find_functions(eni_response)
        format_function(ALL_FUNCTIONS, eni_response)

    else:
        return {
            'statusCode': 200,
            'body': f"ENI: {ENI_ID} not found in {REGION_NAME}"
        }

    return {
        'statusCode': 200,
        'body': "See function logs"
    }
