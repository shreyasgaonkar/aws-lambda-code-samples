import datetime
import concurrent.futures  # for multithreading
import logging

import boto3
import botocore


logger = logging.getLogger()
logger.setLevel("INFO")

DRY_RUN = True  # Set this to false when ready to delete
DELETE_SNAPSHOT_OLDER_THAN_DAYS = 7  # Change to snapshot older than these many days

STS_CLIENT = boto3.client("sts")
EC2_CLIENT = boto3.client("ec2")


# Set Account ID of this function
ACCOUNT_ID = STS_CLIENT.get_caller_identity().get("Account")

# Create paginator for EC2 client
EC2_PAGINATOR = EC2_CLIENT.get_paginator("describe_snapshots")
EC2_PAGINATOR = EC2_PAGINATOR.paginate(
    Filters=[{"Name": "owner-id", "Values": [ACCOUNT_ID]}]
)

# Change the days to change the offset day from where the snapshots will be deleted
RETENTION_DATE = datetime.datetime.utcnow() - datetime.timedelta(
    days=DELETE_SNAPSHOT_OLDER_THAN_DAYS
)


def get_snapshots(snapshot) -> None:
    """Get snapshots to be deleted if the start time is before the retention threadhold"""

    snapshot_id, volume_id, volume_size = (
        snapshot["SnapshotId"],
        snapshot["VolumeId"],
        snapshot["VolumeSize"],
    )

    logger.info(
        f"Checking snapshot: {snapshot_id} with volume id: {volume_id} of size: {volume_size} GiB"
    )

    if RETENTION_DATE.isoformat() > snapshot["StartTime"].isoformat():
        delete_snapshot(
            snapshot_id=snapshot["SnapshotId"],
            creation_date=(snapshot["StartTime"]).isoformat(),
            dry_run_flag=DRY_RUN,
        )


def list_and_delete_snapshot() -> None:
    """Iterator through the paginator to list snapshots to be deleted"""

    for page in EC2_PAGINATOR:
        # Start multithreading to get snapshots and delete them
        with concurrent.futures.ThreadPoolExecutor() as executor:
            _ = [
                executor.submit(get_snapshots, snapshot)
                for snapshot in page["Snapshots"]
            ]


def delete_snapshot(snapshot_id, creation_date, dry_run_flag=True) -> None:
    """Delete the snapshot by id, skip if in-use or dry run flag is set"""

    try:
        EC2_CLIENT.delete_snapshot(SnapshotId=snapshot_id, DryRun=dry_run_flag)
        print(f"Deleted snapshot: {snapshot_id}, created on {creation_date}")

    except botocore.exceptions.ClientError as error:
        if error.response["Error"]["Code"] == "InvalidSnapshot.InUse":
            print(f"Snapshot: {snapshot_id} is in use. Skipping. {error}")
        elif error.response["Error"]["Code"] == "DryRunOperation":
            print(
                f"Skipping snapshot: {snapshot_id}, created on {creation_date} as dry run flag is set. Unset this by updating `DRY_RUN` to `True`"
            )
        else:
            raise error


def lambda_handler(event, context):
    """Main Lambda function"""

    list_and_delete_snapshot()

    return {
        "statusCode": 200,
        "body": "Completed execution. Check function execution logs",
    }
