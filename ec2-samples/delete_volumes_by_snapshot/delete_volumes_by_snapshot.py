import json
import boto3
import botocore
import os


# The snapshot from which the volume was created
SNAPSHOT_ID = "<snapshot-id>"

# Can be one of - creating | available | in-use | deleting | deleted | error
SNAPSHOT_STATUS = "<snapshot-status>"

# Change this to `False` when you are ready to delete the volumes
DRY_RUN = True

REGION = os.environ["AWS_REGION"]
EC2_CLIENT = boto3.client("ec2", region_name=REGION)
EC2_PAGINATOR = EC2_CLIENT.get_paginator("describe_volumes")


EC2_PAGINATOR = EC2_PAGINATOR.paginate(
    Filters=[
        {"Name": "status", "Values": [SNAPSHOT_STATUS.lower()]},
        {"Name": "snapshot-id", "Values": [SNAPSHOT_ID]},
    ]
)


def delete_volume(volume_id, dry_run=True):
    """Deletes the volume by snapshot id"""

    if dry_run:
        print(
            f"Skipping Volume: {volume_id} as dry run flag is set. Unset this by calling `DRY_RUN = False`"
        )
        return
    try:
        EC2_CLIENT.delete_volume(VolumeId=volume_id)
        print(f"Deleted Volume: {volume_id}")
    except botocore.exceptions.ClientError as error:
        print(
            f"Something went wrong while deleting {volume_id}. Skipping this volume id"
        )


def delete_volume(volume_id, dry_run=True):
    """Deletes the volume by snapshot id"""

    if dry_run:
        print(
            f"Skipping Volume: {volume_id} as dry run flag is set. Unset this by calling `DRY_RUN = False`"
        )
        return
    try:
        EC2_CLIENT.delete_volume(VolumeId=volume_id)
        print(f"Deleted Volume: {volume_id}")
    except botocore.exceptions.ClientError as error:
        print(
            f"Something went wrong while deleting {volume_id}. Skipping this volume id"
        )


def lambda_handler(event, context):
    """Main Lambda function handler"""

    for page in EC2_PAGINATOR:
        for volume in page["Volumes"]:
            delete_volume(volume["VolumeId"], dry_run=DRY_RUN)

    return {
        "statusCode": 200,
        "body": json.dumps("Completed execution. Check CloudWatch logs"),
    }
