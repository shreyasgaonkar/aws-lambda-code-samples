# Get *true* async invoke delay

A few AWS services will invoke AWS Lambda asynchronously. These events are added to a queue, which Lambda service will poll regularly. Since this **may** be shared with other services ([explained here](https://youtu.be/QNnMpoD4RHM?t=1736)), you might see some delays in there are few *bad* records in the queue, causing other functions to be delayed - often misinterpritted as **not invoked** rather than delayed.

[get_async_invoke_delay.py](get_async_invoke_delay.py) will help quickly figure out if there's any congestions in the queue causing other functions to be delayed using the difference between the current time and the time at which these messages were added by the respective service.

For Synchronous invocations this will not happen as the invoker will "wait" until Lambda responds back with success/failure message.

Since this metric isn't listed out of the box, we can write a custom CloudWatch Metric for it by dumping the values which we received and check the delay plotted over time. You should use AWS X-Ray to review how long your request spent in the service queue by checking the “dwell time” segment.

![Lambda Metrics](/tmp/images/AWSLambdaCloudWatchAsyncDelay.png)

---

You can also get this value from CloudWatch Insights using this query, against the Lambda function's log group and the time range -

```bash
fields @type = "REPORT"
| stats max(@memorySize) as Memory_Provisioned, min(@maxMemoryUsed) as Min_Memory_Used, max(@maxMemoryUsed) as Max_Memory_Used, avg(@maxMemoryUsed) as Avg_Memory_Used
by bin(1m)
```

![Lambda Metrics](/tmp/images/AWSLambdaAsyncDelayCloudWatchInsights.png)
