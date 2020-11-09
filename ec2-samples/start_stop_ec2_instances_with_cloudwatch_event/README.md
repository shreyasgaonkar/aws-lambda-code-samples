### start_stop_ec2_instances_with_cloudwatch_event

```start_stop_ec2_instances_with_cloudwatch_event.py``` will toggle instance state (start/stop) when a certain tag is added, and depending upon the time of the day.

To tag the target instances, our script will look for the tage name: ```start-stop``` and it's value as ```yes```. Tag name and it's value can be changed by altering: 

```python
paginator = paginator.paginate(Filters=[{
    'Name': 'tag:start-stop',
    'Values': [
        'yes'
    ]
}])
```

The start-stop behavior will be triggered by a CloudWatch Event source (see below). Depending upon the time of the day, function will start the instances if the triggered before noon. Likewise, for a trigger after noon, a Lambda function will stop the targeted instance.

```BASH
0 8,18 * * ? *
```

This cron expression will trigger twice a day - once at 8:00 AM and the other at 6:00 PM. This can be used on a CloudWatch event trigger which will fire the Lambda function during the set times.

Feel free to play with the tag names and the time where the toggle should occur as per your use-case.

As with Lambda, this function will only list functions inside your account with the region in which this Lambda function resides. To retrieve all Lambda functions, you would need to make a [describe_regions](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_regions) API call before creating the client and update the client for every region iteratively.

Since SDK calls could be paginated, this uses the Boto3's [Paginator](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/paginators.html) using ```Filter``` on the instance tags.
