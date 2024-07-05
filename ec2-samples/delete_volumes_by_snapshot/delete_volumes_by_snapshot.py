import json
import logging

import boto3
import botocore

DRY_RUN = True  # Set this to false when ready to delete
SNAPSHOT_ID = "snap-XXXXXXX"  # snapshot id of the volume
VOLUME_STATUS = "in-use"  # Use values from : 'creating'|'available'|'in-use'|'deleting'|'deleted'|'error'


EC2_CLIENT = boto3.client("ec2")
EC2_PAGINATOR = EC2_CLIENT.get_paginator("describe_volumes")

EC2_PAGINATOR = EC2_PAGINATOR.paginate(
    Filters=[
        {"Name": "status", "Values": [VOLUME_STATUS.lower()]},
        {"Name": "snapshot-id", "Values": [SNAPSHOT_ID]},
    ]
)

logger = logging.getLogger()
logger.setLevel("INFO")


def delete_volume(volume_id):
    """Deletes the volume by snapshot id. Sets dry run to true for accidental deletion."""

    logger.info(
        f"Attempting to delete volume {volume_id}, by snapshots using DRY_RUN flag as {DRY_RUN}"
    )

    try:
        EC2_CLIENT.delete_volume(VolumeId=volume_id, DryRun=DRY_RUN)
        logger.info(f"Deleted Volume: {volume_id}")
    except botocore.exceptions.ClientError as error:
        if error.response["Error"]["Code"] == "DryRunOperation":
            logger.info(
                f"Skipping Volume: {volume_id} as dry run flag is set. Unset this setting `DRY_RUN` to `False`"
            )
        else:
            raise error
    else:
        logger.info(f"Deleted volume id: {volume_id}")


def lambda_handler(event, context):
    """Main Lambda function handler"""

    logging.info(
        f"Attempting to delete snapshot: {SNAPSHOT_ID} with status: {VOLUME_STATUS} using DRY-RUN flag as {DRY_RUN}"
    )

    for page in EC2_PAGINATOR:
        for volume in page["Volumes"]:
            delete_volume(volume["VolumeId"])

    if not DRY_RUN:
        logger.info(
            f"Completed execution. Please verify through the AWS console for any orphaned volumes"
        )

    return {
        "statusCode": 200,
        "body": json.dumps("Completed execution. Check execution logs"),
    }
