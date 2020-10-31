[async_config_dashboard.py](async_config_dashboard.py) will return all async configurations - max retry attempts, max event age and destination configuration for all functions in a region. Replace the region at ```LAMBDA_CLIENT = boto3.client('lambda', region_name='us-east-1')``` to run in a different AWS region

Uses [PrettyTable](https://pypi.org/project/PrettyTable/) module imported as a [Lambda layer](/lambda-layer/prettyTable.zip).


Sample output:
```
+---------------------+--------------------+-----------------------------+--------------------------------------------------------------+--------------------------------------------------------------+----------------------------------+
|    Function Name    | Max Retry Attempts | Maximum event age (seconds) |                    On success destination                    |                    On failure destination                    |          Last Modified           |
+---------------------+--------------------+-----------------------------+--------------------------------------------------------------+--------------------------------------------------------------+----------------------------------+
|    destination_1    |         2          |            21600            | arn:aws:lambda:us-west-2:XXXXXXXXXXXX:function:destination_2 | arn:aws:lambda:us-west-2:XXXXXXXXXXXX:function:destination_2 | 2019-12-24 11:21:56.224000+00:00 |
|   lambda_dashboard  |         2          |            21600            |                           NOT SET                            |       arn:aws:sns:us-west-2:XXXXXXXXXXXX:HTTPEndpoint        | 2019-11-29 11:03:19.273000+00:00 |
| async_delay_checker |         2          |            21600            |                           NOT SET                            |                           NOT SET                            | 2020-07-09 15:08:51.409000+00:00 |
|     print_event     |         2          |            21600            |                           NOT SET                            |                           NOT SET                            | 2020-04-08 15:02:02.641000+00:00 |
| boto3versionchecker |         2          |              60             |                           NOT SET                            |                           NOT SET                            | 2020-02-20 16:20:14.158000+00:00 |
|      nVersions      |         1          |            10800            |                           NOT SET                            |                           NOT SET                            | 2019-12-09 11:01:14.326000+00:00 |
+---------------------+--------------------+-----------------------------+--------------------------------------------------------------+--------------------------------------------------------------+----------------------------------+
```
