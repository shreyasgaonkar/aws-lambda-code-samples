# Delete EBS Volumes by Snapshots

This repository provides a Python script, [delete_volumes_by_snapshot.py](delete_volumes_by_snapshot.py), designed to delete EBS volumes based on specific snapshot criteria.

## Usage

To use the script:

1. Open [delete_volumes_by_snapshot.py](delete_volumes_by_snapshot.py) and replace the following placeholders with your specific values:
  
```python
SNAPSHOT_ID = '<snapshot-id>'
SNAPSHOT_STATUS = '<snapshot-status>'
```

1. Override the default region for all SDK clients by passing `region_name=your_region_name` parameter during client creation.

1. To prevent accidental deletions, the script uses a dry run flag (`dry_run=True`) in the API call:

```python
delete_volume(volume['VolumeId'], dry_run=True)
```

Once you are confident that the correct EBS volumes will be deleted, set `dry_run=False` to perform the actual deletion.

## Output Examples

### Successful Deletions

```bash
Deleted Volume: vol-XXXX1
Deleted Volume: vol-XXXX2
```

### Dry Run Mode

```bash
Skipping Volume: vol-XXXX as dry run flag is set. Unset this by calling `delete_volume(volume_id, dry_run=False)`
```

Replace placeholders with actual values and ensure careful verification before setting `dry_run=False` to execute deletions. This ensures the script operates safely according to your requirements.