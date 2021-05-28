If you are looking to list all subscriptions tied to all SNS topics, this script will iterate through all regions, and topics to return a list of all subscriptions in your Account in a tabular dashboard using PrettyTable (can be added as a Lambda layer from [here](/lambda-layer/)). Depending upon the number of resources in your account, it may take a while. Here I am using the Lambda's init duration of max 10 seconds to leverage full CPU power, if your account has a lot of subscriptions then this will overflow the init duration and you will be charged for the entire duration including init.

I am using `ec2.describe_regions()` to get the list of all AWS regions and iterate through it to create new SNS client, which in turn will return the list of all subscriptions.


## Output:

```
+--------------------------------------------------------------------------------------------------------+--------------+-----------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------+-----------+
|                                            SubscriptionArn                                             |    Owner     |                                                     Endpoint                                                    |                              TopicArn                             |   Region  |
+--------------------------------------------------------------------------------------------------------+--------------+-----------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------+-----------+
|              arn:aws:sns:eu-west-1:XXXXXXXXXXXX:SMS:XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX               | XXXXXXXXXXXX |                                                  +353XXXXXXXXX                                                  |               arn:aws:sns:eu-west-1:XXXXXXXXXXXX:SMS              | eu-west-1 |
|     arn:aws:sns:us-east-2:XXXXXXXXXXXX:IOTSNSemailXXXXXXXXXX:XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX      | XXXXXXXXXXXX |                                                test@example.com                                                 |      arn:aws:sns:us-east-2:XXXXXXXXXXXX:IOTSNSemailXXXXXXXXXX     | us-east-2 |
|       arn:aws:sns:us-west-2:XXXXXXXXXXXX:DeploymentProject:XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX        | XXXXXXXXXXXX |                         arn:aws:lambda:us-west-2:XXXXXXXXXXXX:function:deploymentProject                        |        arn:aws:sns:us-west-2:XXXXXXXXXXXX:DeploymentProject       | us-west-2 |
+--------------------------------------------------------------------------------------------------------+--------------+-----------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------+-----------+
```
