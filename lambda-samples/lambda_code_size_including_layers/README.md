[This script](lambda_code_size_including_layers.py) will return function size in  human readable file size inclusive of all attached layers. Currently, the deployment package size limit of the function including all of its layers should be [less than 250 MB unzipped](https://docs.aws.amazon.com/lambda/latest/dg/limits.html).

**Note:** Uses [PrettyTable](https://pypi.org/project/PrettyTable/) module importing from this [Lambda layer](/lambda-layer/prettyTable.zip).

Replace the function name variables:

```
FUNCTION_NAME = '<enter-function-name>'
QUALIFIER = '$LATEST'
```

Sample output:
```
Total function size for function: numpy:$LATEST version
+------------+------------+---------------------+
| Code Size  | Layer Size | Total function size |
+------------+------------+---------------------+
| 1012 bytes |  70.82 MB  |       70.82 MB      |
+------------+------------+---------------------+
```
