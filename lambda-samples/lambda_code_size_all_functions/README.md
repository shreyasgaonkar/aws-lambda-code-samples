# Get Lambda code storage size across all functions

This will iterate through all functions in a region (defaults to where Lambda resides) to return the total size in MBs used by Lambda. The [ListFunction](https://docs.aws.amazon.com/lambda/latest/dg/API_ListFunctions.html) API call is paginated if you have several Lambda functions, and will return ```NextToken``` value if it's paginated. This means that we need to make successive calls on the ListFunctions API to get the next batch of functions. Boto3's [Paginator](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/paginators.html) handles this for us - just like what the CLI does in the backend.

The default code storage limit per region is 75 GB as per the [documentation](https://docs.aws.amazon.com/lambda/latest/dg/limits.html):

```bash
+----------------------------+---------------+
|          Resource          | Default Limit |
+----------------------------+---------------+
| Concurrent executions      | 1,000         |
| Function and layer storage | 75 GB         |
+----------------------------+---------------+
```
