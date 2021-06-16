import json
import boto3
import botocore

SNAPSHOT_ID = '<snapshot-id>'
SNAPSHOT_STATUS = '<snapshot-status>'

EC2_CLIENT = boto3.client("ec2")
EC2_PAGINATOR = EC2_CLIENT.get_paginator('describe_volumes')

EC2_PAGINATOR = EC2_PAGINATOR.paginate(Filters=[{
    'Name': 'status',
    'Values': [SNAPSHOT_STATUS.lower()]
}, {
    'Name': 'snapshot-id',
    'Values': [SNAPSHOT_ID]
}])


def delete_volume(volume_id, dry_run=True):
    """Deletes the volume by snapshot id. Sets dry run to true for accidental deletion"""
    print(volume_id)
    try:
        EC2_CLIENT.delete_volume(
            VolumeId=volume_id,
            DryRun=dry_run
        )
        print(f'Deleted Volume: {volume_id}')
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'DryRunOperation':
            print(
                f"Skipping Volume: {volume_id} as dry run flag is set. Unset this by calling `delete_volume(volume_id, dry_run=False)``")
        else:
            raise error


def lambda_handler(event, context):
    """Main Lambda function handler"""

    for page in EC2_PAGINATOR:
        for volume in page['Volumes']:
            delete_volume(volume['VolumeId'], dry_run=True)

    return {
        'statusCode': 200,
        'body': json.dumps("Completed execution. Check CloudWatch logs")
    }
