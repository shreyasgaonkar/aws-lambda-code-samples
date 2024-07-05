import json
import boto3
from prettytable import PrettyTable  # imported as a Lambda Layer


VPC_ID = "vpc-28ba2f4e"

# PrettyTable
TABLE = PrettyTable(["Instance ID", "Security Group", "NACL"])

# Create EC2 and paginator EC2_CLIENT for the SDK calls
EC2_CLIENT = boto3.EC2_CLIENT("ec2")
PAGINATOR = EC2_CLIENT.get_paginator("describe_instances")
PAGINATOR = PAGINATOR.paginate(
    Filters=[
        {"Name": "vpc-id", "Values": [VPC_ID]},
    ]
)

# Function defination outside the handler for faster function execution
# This will get all the required metadata - instance id, associated subnet
# and the NACL id for the target VPC.


def instance_metadata(result):
    """Get Instance info"""
    try:
        instance = result["Instances"][0]
        instance_id = instance["InstanceId"]
        network_interface = instance["NetworkInterfaces"][0]
        security_group_id = network_interface["Groups"][0]["GroupId"]
        subnet_id = network_interface["SubnetId"]

        response = EC2_CLIENT.describe_network_acls(
            Filters=[{"Name": "association.subnet-id", "Values": [subnet_id]}]
        )
        nac_id = response["NetworkAcls"][0]["NetworkAclId"]

        TABLE.add_row([instance_id, security_group_id, nac_id])

    except (IndexError, KeyError) as e:
        print(f"Error retrieving instance metadata: {e}")


def lambda_handler(event, context):

    for page in PAGINATOR:
        for instance in page["Reservations"]:
            instance_metadata(instance)

    print(TABLE)

    return {"statusCode": 200, "body": json.dumps("Completed execution.")}
