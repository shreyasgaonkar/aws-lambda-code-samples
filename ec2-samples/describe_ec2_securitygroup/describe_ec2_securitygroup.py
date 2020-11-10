import json
import boto3
from prettytable import PrettyTable  # imported as a Lambda Layer


# PrettyTable
TABLE = PrettyTable(['Instance ID', 'Security Group', 'NACL'])

# Create EC2 and paginator client for the SDK calls
CLIENT = boto3.client('ec2')
PAGINATOR = CLIENT.get_paginator('describe_instances')


VPC_ID = 'vpc-28ba2f4e'

PAGINATOR = PAGINATOR.paginate(Filters=[{
    'Name': 'vpc-id',
    'Values': [VPC_ID]
}])

# Function defination outside the handler for faster function execution
# This will get all the required metadata - instance id, associated subnet
# and the NACL id for the target VPC.


def instance_metadata(result):
    """Get Instance info"""
    # Check if the instance is in the Target VPC:
    data = result['Instances'][0]['NetworkInterfaces'][0]
    if(data['VpcId'] == VPC_ID):
        instance_id = result['Instances'][0]['InstanceId']
        security_group_id = data['Groups'][0]['GroupId']
        subnet_id = data['SubnetId']

        response = CLIENT.describe_network_acls(
            Filters=[
                {
                    'Name': 'association.subnet-id',
                    'Values': [subnet_id]
                }
            ]
        )
        nac_id = response['NetworkAcls'][0]["NetworkAclId"]
        TABLE.add_row([instance_id, security_group_id, nac_id])


def lambda_handler(event, context):

    for page in PAGINATOR:
        for instance in page['Reservations']:
            instance_metadata(instance)

    print(TABLE)

    return {
        'statusCode': 200,
        'body': json.dumps("Completed execution.")
    }
