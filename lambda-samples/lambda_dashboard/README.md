[lambda_dashboard.py](lambda_dashboard.py) will return regional metrics across all AWS regions including number of Lambda functions, Code Storage, Full Account Concurrency and unreserved account concurrency in one place.

Uses [PrettyTable](https://pypi.org/project/PrettyTable/) module imported as a [Lambda layer](/lambda-layer/prettyTable.zip).


Sample output:
```
+----------------+--------------------+--------------+----------------------+------------------------+
|     Region     | Lambda function(s) | Code Storage | Regional Concurrency | Unreserved Concurrency |
+----------------+--------------------+--------------+----------------------+------------------------+
|   eu-north-1   |         1          |  299 bytes   |         1000         |          1000          |
|   ap-south-1   |         0          |   0 bytes    |         1000         |          1000          |
|   eu-west-3    |         0          |   0 bytes    |         1000         |          1000          |
|   eu-west-2    |         0          |   0 bytes    |         1000         |          1000          |
|   eu-west-1    |         5          |  904 bytes   |         1000         |          1000          |
| ap-northeast-2 |         0          |   0 bytes    |         1000         |          1000          |
| ap-northeast-1 |         1          |  237 bytes   |         1000         |          1000          |
|   sa-east-1    |         0          |   0 bytes    |         1000         |          1000          |
|  ca-central-1  |         0          |   0 bytes    |         1000         |          1000          |
| ap-southeast-1 |         0          |   0 bytes    |         1000         |          1000          |
| ap-southeast-2 |         0          |   0 bytes    |         1000         |          1000          |
|  eu-central-1  |         0          |   0 bytes    |         1000         |          1000          |
|   us-east-1    |         99         |  101.29 MB   |         1000         |          2000          |
|   us-east-2    |         1          |  201.44 KB   |         1000         |          1000          |
|   us-west-1    |         1          |  614 bytes   |         1000         |          1000          |
|   us-west-2    |        300         |   951.5 MB   |         1000         |           900          |
+----------------+--------------------+--------------+----------------------+------------------------+
```

Once the table has been created, you can [sort using field](https://github.com/jazzband/prettytable#sorting-your-table-by-a-field) while printing:

``` print(TABLE.get_string(sortby="Code Storage", reversesort=True)) ```
