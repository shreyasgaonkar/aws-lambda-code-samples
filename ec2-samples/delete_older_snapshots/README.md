This code describes AMIs available to you across all regions. Replace the AccountId or add multiple AccountIds under `Values`:

```
EC2_PAGINATOR = EC2_PAGINATOR.paginate(Filters=[{
    'Name': 'owner-id',
    'Values': ['<Enter Account ID>']
}])
```

Any snapshots older than 7 days will be tagged by default. You can change this by updating the time delta from:

```
RETENTION_DATE = datetime.datetime.utcnow() - datetime.timedelta(days=7)
```

⚠️ This script runs in Dry mode by default. You can change this to delete the snapshot once you are ready, by changing calling `delete_snapshot()` with `dry_run_flag=False`


Function output:

```bash
Skipping snapshot: snap-0b3c3672358db8339, created on 2019-04-24T17:09:59.247000+00:00 as dry run flag is set. Unset this by calling `delete_snapshot()` with dry_run_flag=False
```
