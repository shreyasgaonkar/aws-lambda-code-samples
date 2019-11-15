import json
import boto3

# Create EC2 and paginator client for the SDK calls
client = boto3.client('ec2')
paginator = client.get_paginator('describe_instances')

target_vpc_id = 'vpc-28ba2f4e'

# Create an array to store the instance id's to loop over later
all_instances = []

# Function defination outside the handler for faster function execution
# This will get all the required metadata - instance id, associated subnet
# and the NACL id for the target VPC.


def instance_metadata(result):
    # Check if the instance is in the Target VPC:
    data = result['Instances'][0]['NetworkInterfaces'][0]
    if(data['VpcId'] == target_vpc_id):
        instance_id = result['Instances'][0]['InstanceId']
        security_group_id = data['Groups'][0]['GroupId']
        subnet_id = data['SubnetId']

        response = client.describe_network_acls(
            Filters=[
                {
                    'Name': 'association.subnet-id',
                    'Values': [subnet_id]
                }
            ]
        )
        nac_id = response['NetworkAcls'][0]["NetworkAclId"]
        all_instances.append(("Instance id: " + instance_id,
                              "Security Group ID: " + security_group_id, "NACL id: " + nac_id))


def lambda_handler(event, context):

    # Describe all instances in this region
    page_iterator = paginator.paginate()
    result = []

    for instance in page_iterator:
        # print(instance)
        result.append(instance['Reservations'])

    for i in range(len(result[0])):
        instance_metadata(result[0][i])

    # Print all the required data from the variable
    for i in all_instances:
        print(i)

    return {
        'statusCode': 200,
        'body': json.dumps("Completed execution.")
    }
