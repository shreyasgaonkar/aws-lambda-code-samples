[This script](clean_orphaned_event_source_mappings.py) will help to iterate through all functions in a region to find any orphaned ENIs tied to a function which doesn't exist. If there exists any such Event Source Mappings, it will attempt to delete them and print the deleted UUID associated with the already deleted function.

```
Deleted ESM for UUID: 7760c1ee-980d-4e8e-980d-38b09d8b70c7 associated with arn:aws:lambda:us-east-1:XXXXXXXXXXXX:function:invalid_esm
```
