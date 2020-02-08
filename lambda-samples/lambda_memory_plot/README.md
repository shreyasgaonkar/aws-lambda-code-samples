Since Lambda's function memory metric isn't logged under CloudWatch, you can use this sample code to get this working. Set a CloudWatch log trigger on this function, and let it create custom metrics under ```CloudWatch > Metrics > Lambda > MB ```

![Lambda Metrics](/tmp/images/AWSLambdaCloudWatchMetric.png)
