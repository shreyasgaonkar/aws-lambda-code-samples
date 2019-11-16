### start_stop_ec2_instances_with_cloudwatch_event

```start_stop_ec2_instances_with_cloudwatch_event.py``` will toggle instance state (start/stop) when a certain tag is added, and depending upon the time of the day.

Here, we are using the Tag name as ```start-stop``` and it's value as ```yes```. The start-stop behavior will be triggered by a CloudWatch Event source (Needs to be added separately once this is created). Depending upon the time of the day, function will start the instances if the trigger occurs before noon. Likewise, for Lambda triggers after the noon, Lambda will stop the instance.

Feel free to play with the tag names and the time where the toggle should occur as per your use-case.

As with Lambda, this function will only list functions inside your account with the region in which this Lambda function resides. To retrieve all Lambda functions, you would need to make a [describe_regions](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_regions) API call before creating the client and update the client for every region iteratively.

Since SDK calls could be paginated, this uses the Boto3's [Paginator](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/paginators.html) using ```Filter``` on the instance tags.
