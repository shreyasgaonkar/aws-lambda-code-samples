# AWS Lambda sample codes

A  few of the sample AWS Lambda function codes for common use-cases with [Amazon EC2](https://github.com/shreyasgaonkar/aws-lambda-code-samples#ec2), [AWS Lambda](https://github.com/shreyasgaonkar/aws-lambda-code-samples#lambda) & [Amazon SNS](https://github.com/shreyasgaonkar/aws-lambda-code-samples#sns).

## EC2

1. Start/Stop EC2 instances using CloudWatch Event Trigger  - [start_stop_ec2_instances_with_cloudwatch_event.py](ec2-samples/start_stop_ec2_instances_with_cloudwatch_event.py)

2. Describe EC2's metadata in a region - Associated subnets, Instance ID & NACL-ID for a target VPC - [describe_ec2_securitygroup.py](ec2-samples/describe_ec2_securitygroup.py)

3. Describe all AMIs for your account across all regions - [describe_ami.py](ec2-samples/describe_ami.py)


## Lambda

1. Get underlying Lambda's CPU hardware, /tmp storage, os-release and it's contents  - [get_cpu_info.py](lambda-samples/get_cpu_info.py)

2. Create "Memory Used" Metrics for your Lambda functions - [lambda_memory_plot.py](lambda-samples/lambda_memory_plot.py)

3. Test HTTP connection for your Lambda function inside VPC - [http_connection_test.py](misc/http_connection_test.py)

4. List code storage for all Lambda functions in a region - [lambda_code_size.py](lambda-samples/lambda_code_size.py)


## SNS

1. Programmatically create subscription filters for SNS  - [set_subscription_filters.py](sns-samples/set_subscription_filters.py)

2. Programmatically set SenderID while sending SMS text messages  - [sender_id.py](sns-samples/sender_id.py)

## Additional Information

- Refer to the individual .md files for additional information.

## Built with
- [Python3](https://www.python.org/downloads/)
- [AWS](https://aws.amazon.com/)
- [Boto3 SDK](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

## Missing Info / Bugs

- :cold_sweat: Something broken? [Open an issue](https://github.com/shreyasgaonkar/aws-lambda-code-samples/issues) with a few sample inputs where it breaks. Screenshots help!

- More additional services/use-cases, [open a new issue](https://github.com/shreyasgaonkar/aws-lambda-code-samples/issues)

## Contributing

This is an iterative repository, I'll keep adding more sample codes for more use-cases as I come across them. I have tested all scripts using ```Python3.6``` runtime inside Lambda under ```us-west-2``` region, and most of this should work for all Python runtimes (Python 2.7 EOL: :dizzy_face:).

- Fork repo
- Set runtime as ```Python3```
- Send your awesome :raised_hands: [Pull Request](https://github.com/shreyasgaonkar/aws-lambda-code-samples/pulls) with code/.md changes
    - Follow Python's [PEP8](https://www.python.org/dev/peps/pep-0008/) coding standards.
    - Commit repo using the [Seven Rules](https://chris.beams.io/posts/git-commit/#seven-rules)
- Your PR gets merged :white_check_mark: and a shoutout :loudspeaker:


#### Repo structure:

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
