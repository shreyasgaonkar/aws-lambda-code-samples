## Get async invoke delay

Few AWS services will invoke AWS Lambda asynchronously. These events are added to a queue, which Lambda service will poll regularly. Since this **may** be shared with other services ([explained here](https://youtu.be/QNnMpoD4RHM?t=1736)), you might see some delays in there are few "bad" records in the queue, causing other functions to be delayed - often misinterpritted as **not invoked** rather than delayed.

[get_async_invoke_delay.py](get_async_invoke_delay.py) will help quickly figure out if there's any congestions in the queue causing other functions to be delayed using the difference between the current time and the time at which these messages were added by the respective service.

For Synchronous invocations this will not happen as the invoker will "wait" until Lambda responds back with success/failure message.
