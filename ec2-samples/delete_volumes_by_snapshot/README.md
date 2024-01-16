If you are looking to delete EBS Volume(s) with specific snapshot status and snapshot id, you can use [delete_volumes_by_snapshot.py](delete_volumes_by_snapshot.py) and replace -

To ensure you do not accidentally delete the volume without verification, `DRY_RUN = TRUE` flag is set. When you are ready to delete the Volume, set this to `False` and re-run the function.

```
# Change this to `False` when you are ready to delete the volumes
DRY_RUN = True
```

```
# The snapshot from which the volume was created
SNAPSHOT_ID = "<snapshot-id>"

# Can be one of - creating | available | in-use | deleting | deleted | error
SNAPSHOT_STATUS = "<snapshot-status>"
```

By default, this function will run in the region in which the Lambda function resides. You can override this by changing the value of 

```
REGION = os.environ["AWS_REGION"]
```

to one of the AWS region names like `us-east-1`.

### Output:

#### Success:
```
Deleted Volume: vol-XXXX1
Deleted Volume: vol-XXXX2
```

#### Dry Run:
```
Skipping Volume: vol-XXXX as dry run flag is set. Unset this by setting `DRY_RUN = FALSE`
```