import datetime
import concurrent.futures  # for multithreading
import boto3
import botocore


# Set this to false when ready to delete the snapshots
DRY_RUN = True

STS_CLIENT = boto3.client("sts")
EC2_CLIENT = boto3.client("ec2")

# Get account id from Lambda. Optionally, override this for describing snapshots
# from other account(s)
ACCOUNT_ID = STS_CLIENT.get_caller_identity()["Account"]

EC2_PAGINATOR = EC2_CLIENT.get_paginator("describe_snapshots")
EC2_PAGINATOR = EC2_PAGINATOR.paginate(
    Filters=[{"Name": "owner-id", "Values": [ACCOUNT_ID]}]
)

# Change the days to change the offset day from where the snapshots will be deleted
RETENTION_DATE = datetime.datetime.utcnow() - datetime.timedelta(days=7)


def get_snapshots(snapshot, dry_run):
    """Get snapshots to be deleted if the start time is before the retention threadhold"""

    if RETENTION_DATE.isoformat() > snapshot["StartTime"].isoformat():
        delete_snapshot(
            snapshot_id=snapshot["SnapshotId"],
            creation_date=(snapshot["StartTime"]).isoformat(),
            dry_run_flag=dry_run,
        )


def list_and_delete_snapshot(dry_run):
    """Iterator through the paginator to list snapshots to be deleted"""

    for page in EC2_PAGINATOR:
        # Start multithreading to get snapshots and delete them
        with concurrent.futures.ThreadPoolExecutor() as executor:
            _ = [
                executor.submit(get_snapshots, snapshot, dry_run)
                for snapshot in page["Snapshots"]
            ]


def delete_snapshot(snapshot_id, creation_date, dry_run_flag=True):
    """Delete the snapshot by id, skip if in-use or dry run flag is set"""

    try:
        EC2_CLIENT.delete_snapshot(SnapshotId=snapshot_id, DryRun=dry_run_flag)
        print(f"Deleted snapshot: {snapshot_id}, created on {creation_date}")

    except botocore.exceptions.ClientError as error:
        if error.response["Error"]["Code"] == "InvalidSnapshot.InUse":
            print(f"Snapshot: {snapshot_id} is in use. Skipping. {error}")
        elif error.response["Error"]["Code"] == "DryRunOperation":
            print(
                f"Skipping snapshot: {snapshot_id}, created on {creation_date} as dry run flag is set. Unset this by calling `delete_snapshot()` with dry_run_flag=False"
            )
        else:
            raise error


def lambda_handler(event, context):
    """Main Lambda function"""

    list_and_delete_snapshot(dry_run=DRY_RUN)

    return {"statusCode": 200, "body": "Completed execution. Check CloudWatch logs"}
