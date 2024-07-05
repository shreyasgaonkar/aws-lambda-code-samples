# Delete old Snapshots in an account

This function deletes older snapshots. By default snapshots older than 7 days will be deleted once you set the `DRY_RUN` flag to `False`. You can change both of these values by updating the below variables:

```python
DRY_RUN = True  # Set this to false when ready to delete
DELETE_SNAPSHOT_OLDER_THAN_DAYS = 7  # Change to snapshot older than these many days
```

Function output:

```bash
Skipping snapshot: snap-0b3c3672358db8339, created on 2019-04-24T17:09:59.247000+00:00 as dry run flag is set. Unset this by updating `DRY_RUN` to `True`
```
