import boto3
import logging
from typing import List, Dict, Any, Iterator
from prettytable import PrettyTable # PrettyTable from Lambda Layer
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

EC2_CLIENT = boto3.client("ec2")

def get_filtered_network_interfaces() -> Iterator[Dict[str, Any]]:
    """
    Retrieve and filter network interfaces associated with AWS Lambda VPC ENIs.
    """
    try:
        paginator = EC2_CLIENT.get_paginator("describe_network_interfaces")
        page_iterator = paginator.paginate()
        return page_iterator.search(
            "NetworkInterfaces[?Status!=`null`] | "
            "[?contains(Description, `AWS Lambda VPC ENI`)] | "
            "[?contains(Attachment.AttachmentId, `ela-attach`)]"
        )
    except ClientError as e:
        logger.error(f"Error retrieving network interfaces: {e}", exc_info=True)
        raise

def format_security_groups(groups: List[Dict[str, str]]) -> str:
    """
    Format the security groups into a comma-separated string.
    """
    return ", ".join(group["GroupId"] for group in groups)

def create_eni_table(enis: List[Dict[str, Any]]) -> PrettyTable:
    """
    Create and return a PrettyTable with ENI details.
    """
    table = PrettyTable(["ENI ID", "Status", "VPC ID", "Subnet Id", "Security Groups"])
    for eni in enis:
        security_groups = format_security_groups(eni.get("Groups", []))
        table.add_row([
            eni["NetworkInterfaceId"],
            eni["Status"],
            eni["VpcId"],
            eni["SubnetId"],
            security_groups
        ])
    return table

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Retrieves network interfaces, filters them, and returns the results.
    """
    try:
        eni_generator = get_filtered_network_interfaces()
        enis = list(eni_generator)  # Convert generator to list

        if not enis:
            logger.info("No matching network interfaces found.")
            return {"statusCode": 200, "body": "No matching ENIs found."}

        table = create_eni_table(enis)
        logger.info("ENI details:\n%s", table)

        return {
            "statusCode": 200,
            "body": f"Found {len(enis)} matching ENIs. See function logs for details."
        }

    except Exception as e:
        logger.error(f"Error in lambda_handler: {e}", exc_info=True)
        return {"statusCode": 500, "body": "Internal server error."}
