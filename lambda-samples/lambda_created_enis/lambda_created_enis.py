import boto3
import logging

from prettytable import PrettyTable  # PrettyTable from Lambda Layer

logger = logging.getLogger()
logger.setLevel("INFO")

TABLE = PrettyTable(["ENI ID", "Status", "VPC ID", "Subnet Id", "Security Groups"])

EC2 = boto3.client("ec2")
PAGINATOR = EC2.get_paginator("describe_network_interfaces")
PAGE_ITERATOR = PAGINATOR.paginate()
FILTERED_ITERATOR = PAGE_ITERATOR.search(
    "NetworkInterfaces[?Status!=`null`] | [?contains(Description, `AWS Lambda VPC ENI`)] | [?contains(Attachment.AttachmentId, `ela-attach`)]"
)


def print_table(enis) -> None:
    """helper function"""

    for value in enis:
        security_groups = []
        for i in value["Groups"]:
            security_groups.append(i["GroupId"])

        TABLE.add_row(
            [value["NetworkInterfaceId"], value["Status"], value["VpcId"], value["SubnetId"], security_groups]
        )

    print(TABLE)


def lambda_handler(event, context):
    """Main function"""

    print_table(FILTERED_ITERATOR)
    return {"statusCode": 200, "body": "See function logs"}
