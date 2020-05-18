import boto3

# PrettyTable for output
from prettytable import PrettyTable

TABLE = PrettyTable(['ENI ID', 'Status', 'VPC ID',
                     'Subnet Id', 'Security Groups'])

EC2 = boto3.client('ec2')
PAGINATOR = EC2.get_paginator('describe_network_interfaces')
PAGE_ITERATOR = PAGINATOR.paginate()
FILTERED_ITERATOR = PAGE_ITERATOR.search(
    "NetworkInterfaces[?Status!=`null`] | [?contains(Description, `AWS Lambda VPC ENI`)] | [?contains(Attachment.AttachmentId, `ela-attach`)]")


def print_table(enis):
    """ helper function """
    for value in enis:
        security_groups = []
        for i in value['Groups']:
            security_groups.append(i['GroupId'])

        TABLE.add_row([value['NetworkInterfaceId'], value['Status'],
                       value['VpcId'], value['SubnetId'], security_groups])

    print(TABLE)
    return True


def lambda_handler(event, context):
    """ Main function """

    print_table(FILTERED_ITERATOR)
    return {
        'statusCode': 200,
        'body': "See function logs"
    }
