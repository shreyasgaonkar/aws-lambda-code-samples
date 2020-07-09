[reserved_concurrency.py](reserved_concurrency.py) will iterate through all functions in a region (defaults to where Lambda resides) to return the function name where ```Reserve concurrency``` is set - easier to find functions which might be using up the [Unreserved account concurrency](https://aws.amazon.com/about-aws/whats-new/2017/11/set-concurrency-limits-on-individual-aws-lambda-functions/).

[Newly introduced](https://aws.amazon.com/about-aws/whats-new/2019/12/aws-lambda-announces-provisioned-concurrency/) provisioned concurrency can also contribute towards reducing the Unreserved account concurrency count as seen on the dashboard. ```get_provisioned_concurrency_config()``` can be used to extract the reserved concurrency information off a version or alias.

Uses [PrettyTable](https://pypi.org/project/PrettyTable/) module imported as a Lambda layer from [here](/lambda-layer/prettyTable.zip).

**Note**:```client.get_provisioned_concurrency_config & client.get_function_concurrency()``` might require a newer boto3 version client. I have used boto3 v1.10.42, and you can check that using ```boto3.__version__```.


**Output**

```
Total reserved concurrency in us-west-2 region is 5
+---------------+----------------------+
| Function Name | Reserved Concurrency |
+---------------+----------------------+
| my_function_1 |                    0 |
| my_function_2 |                    5 |
+---------------+----------------------+


=====================

Per qualifier Provisioned concurrency:

Total provisioned concurrency in us-west-2 region is 65
+--------------------------------------------------------------+-----------+-----------+-----------+--------+--------------------------+
|                         FunctionArn                          | Requested | Available | Allocated | Status |      Last Modified       |
+--------------------------------------------------------------+-----------+-----------+-----------+--------+--------------------------+
| arn:aws:lambda:us-west-2:XXXXXXXXXXXX:function:nVersions:10  |     10    |     10    |     10    | READY  | 2020-01-01T00:00:00+0000 |
| arn:aws:lambda:us-west-2:XXXXXXXXXXXX:function:nVersions:20  |     5     |     5     |     5     | READY  | 2020-01-01T00:00:00+0000 |
| arn:aws:lambda:us-west-2:XXXXXXXXXXXX:function:nVersions:dev |     50    |     50    |     50    | READY  | 2020-01-01T00:00:00+0000 |
+--------------------------------------------------------------+-----------+-----------+-----------+--------+--------------------------+
```
