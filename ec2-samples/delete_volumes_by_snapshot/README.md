If you are looking to delete EBS Volume(s) with specific snapshot status and snapshot id, you can use [delete_volumes_by_snapshot.py](delete_volumes_by_snapshot.py) and replace -

```
SNAPSHOT_ID = '<snapshot-id>'
SNAPSHOT_STATUS = '<snapshot-status>'
```

You can override region from all the SDK clients by passing `region_name=region_name` param during the client creation. To ensure you do not accidentally delete the volume without verification, a dry run flag is set on the API call: `delete_volume(volume['VolumeId'], dry_run=True)`. Once you are sure the required EBS volumes will be delete, you can set this value to False.


### Output:

#### Success:
```
Deleted Volume: vol-XXXX1
Deleted Volume: vol-XXXX2
```

#### Dry Run:
```
Skipping Volume: vol-XXXX as dry run flag is set. Unset this by calling `delete_volume(volume_id, dry_run=False)``

```
