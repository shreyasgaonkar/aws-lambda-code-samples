If you are looking to list all subscriptions tied to all SNS topics, this script will iterate through all regions, and topics to return a list of topic-subscription combination. Depending upon the number of resources in your account, it may take a while, but consider Lambda's maximum timeout of ```15 minutes```.

```ec2.describe_regions()``` will list all regions which will be used to create new SDK clients tied to the region for checking for topics/subscriptions. This will be followed by two paginator calls for ```list_topics``` and ```list_subscriptions_by_topic``` to return the result.

## Output:

```
('arn:aws:sns:us-east-1:XXXXXXXXXXXX:topic-name', ['arn:aws:sns:us-east-1:XXXXXXXXXXXX:topic-name:<subscription-id>'])
('arn:aws:sns:us-west-2:XXXXXXXXXXXX:dlq', ['arn:aws:sns:us-west-2:XXXXXXXXXXXX:dlq:<subscription-id>'])
('arn:aws:sns:eu-west-1:XXXXXXXXXXXX:sns', ['arn:aws:sns:eu-west-1:XXXXXXXXXXXX:sns:<subscription-id>'])
```
