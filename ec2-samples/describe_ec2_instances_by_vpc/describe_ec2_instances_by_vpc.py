import json
import boto3
from prettytable import PrettyTable  # imported as a Lambda Layer

VPC_ID = "vpc-XXXXX"

# Create EC2 and paginator client for the SDK calls
CLIENT = boto3.client("ec2")
PAGINATOR = CLIENT.get_paginator("describe_instances")
PAGINATOR = PAGINATOR.paginate(Filters=[{"Name": "vpc-id", "Values": [VPC_ID]}])

# PrettyTable
TABLE = PrettyTable(["Instance ID", "Security Group", "NACL"])


def get_instance_metadata(instance, vpc_id, client, table):
    """Get Instance info"""
    instance_data = instance["Instances"][0]
    network_data = instance_data["NetworkInterfaces"][0]

    if network_data["VpcId"] == vpc_id:
        instance_id = instance_data["InstanceId"]
        security_group_id = network_data["Groups"][0]["GroupId"]
        subnet_id = network_data["SubnetId"]

        response = client.describe_network_acls(
            Filters=[{"Name": "association.subnet-id", "Values": [subnet_id]}]
        )
        nacl_id = response["NetworkAcls"][0]["NetworkAclId"]
        table.add_row([instance_id, security_group_id, nacl_id])


def lambda_handler(event, context):
    for page in PAGINATOR:
        for instance in page["Reservations"]:
            get_instance_metadata(instance, VPC_ID, CLIENT, TABLE)

    if TABLE:
        print(f"Instances using {VPC_ID}:\n{TABLE}")

    return {"statusCode": 200, "body": json.dumps("Completed execution.")}
