# Clean Orphaned Event Source Mappings

This script (`clean_orphaned_event_source_mappings.py`) helps iterate through all Lambda functions in a specific AWS region to identify orphaned Event Source Mappings (ESMs). Orphaned ESMs are Event Source Mappings that are tied to a Lambda function that no longer exists.

If any orphaned ESMs are found, the script will attempt to delete them and log the deleted Event Source Mapping's UUID and the associated Lambda function ARN.

## Features

- Iterates through all Lambda functions in the specified AWS region.
- Retrieves all Event Source Mappings (ESMs) associated with Lambda functions.
- Identifies orphaned ESMs where the associated Lambda function no longer exists.
- Attempts to delete orphaned ESMs.
- Logs the UUID of deleted ESMs and the associated Lambda ARN.

## How It Works

1. **Get Lambda Function ARNs**: The script fetches all Lambda function ARNs in the region.
1. **List Event Source Mappings**: It then retrieves all Event Source Mappings, checking if the Lambda function ARN is still valid.
1. **Find Orphaned ESMs**: If an Event Source Mapping is associated with a non-existent Lambda function, it is flagged as orphaned.
1. **Delete Orphaned ESMs**: The script attempts to delete any orphaned Event Source Mappings found.

## Example Output

```bash
Deleted ESM for UUID: 7760c1ee-980d-4e8e-980d-38b09d8b70c7 associated with arn:aws:lambda:us-east-1:XXXXXXXXXXXX:function:invalid_esm
```

## Configuration

The script uses the `AWS_REGION` environment variable to determine the region. You can either:

1. Set the region in your environment variables (e.g., `AWS_REGION=us-west-2`).
1. Override the region in the script by defining the `REGION_NAME` variable.