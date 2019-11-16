# AWS Lambda sample codes

A  few of the sample AWS Lambda function codes:

EC2
===

1. Start/Stop EC2 instances using CloudWatch Event Trigger  - [start_stop_ec2_instances_with_cloudwatch_event.py](ec2-samples/start_stop_ec2_instances_with_cloudwatch_event.py)

2. Describe EC2's metadata in a region - Associated subnets, Instance ID & NACL-ID for a target VPC - [describe_ec2_securitygroup.py](ec2-samples/describe_ec2_securitygroup.py)

3. Describe all AMIs for your account across all regions - [describe_ami.py](ec2-samples/describe_ami.py)


Lambda
===

1. Get underlying Lambda's CPU hardware, /tmp storage, os-release and it's contents  - [get_cpu_info.py](lambda-samples/get_cpu_info.py)

2. Create "Memory Used" Metrics for your Lambda functions - [lambda_memory_plot.py](lambda-samples/lambda_memory_plot.py)

3. Test HTTP connection for your Lambda function inside VPC - [http_connection_test.py](misc/http_connection_test.py)

4. List code storage for all Lambda functions in a region - [lambda_code_size.py](lambda-samples/lambda_code_size.py)


SNS
===

1. Programmatically create subscription filters for SNS  - [set_subscription_filters.py](sns-samples/set_subscription_filters.py)

2. Programmatically set SenderID while sending SMS text messages  - [sender_id.py](sns-samples/sender_id.py)

---
Refer to the individual .md files for additional information.

```
$ tree
.
├── LICENSE
├── README.md
├── ec2-samples
│   ├── describe_ami.md
│   ├── describe_ami.py
│   ├── describe_ec2_securitygroup.md
│   ├── describe_ec2_securitygroup.py
│   ├── start_stop_ec2_instances_with_cloudwatch_event.md
│   └── start_stop_ec2_instances_with_cloudwatch_event.py
├── lambda-layer
│   ├── README.md
│   ├── boto3.zip
│   ├── pandasnumpy.zip
│   ├── psycopg2.zip
│   └── requests.zip
├── lambda-samples
│   ├── get_cpu_info.md
│   ├── get_cpu_info.py
│   ├── lambda_code_size.md
│   ├── lambda_code_size.py
│   ├── lambda_memory_plot.md
│   └── lambda_memory_plot.py
├── misc
│   ├── http_connection_test.md
│   └── http_connection_test.py
├── sns-samples
│   ├── sender_id.md
│   ├── sender_id.py
│   ├── set_subscription_filters.md
│   └── set_subscription_filters.py
└── tmp
    └── images
        └── AWSLambdaCloudWatchMetric.png
```
