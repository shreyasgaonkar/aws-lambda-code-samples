This function will help you get started with X-Ray tracing on your Lambda function. Using the [X-Ray SDK](/lambda-layer) and [Requests](/lambda-layer) module as layers.

Using ```aws_xray_sdk.core``` we can manually patch each subsegment of the downstream API calls made from your function; or let the SDK handle it Automatically for you using ```aws_xray_sdk.core.patch()```. Alternatively, you can set it to patch all supported modules from the SDK using ```aws_xray_sdk.core.patch_all()``` outside the handler to Automatically generate subsegments for all these modules:

- botocore
- boto3
- requests
- sqlite3
- mysql
- pymysql

If any of the downstream supports X-Ray tracing passthrough, those traces will also populate for one of the requests hitting Lambda.

#### Sample X-ray trace:

![Lambda Metrics](/tmp/images/AWSLambdaX-Ray.PNG)
