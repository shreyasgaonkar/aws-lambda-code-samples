# AWS Lambda sample codes [![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/shreyasgaonkar/aws-lambda-code-samples.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/shreyasgaonkar/aws-lambda-code-samples/context:python)

A few of the sample AWS Lambda function codes for common use-cases with [Amazon EC2](https://github.com/shreyasgaonkar/aws-lambda-code-samples#ec2), [AWS Lambda](https://github.com/shreyasgaonkar/aws-lambda-code-samples#lambda) & [Amazon SNS](https://github.com/shreyasgaonkar/aws-lambda-code-samples#sns).

## EC2

1. Start/Stop EC2 instances using CloudWatch Event Trigger  - [start_stop_ec2_instances_with_cloudwatch_event.py](ec2-samples/start_stop_ec2_instances_with_cloudwatch_event/)

2. Describe EC2's metadata in a region - Associated subnets, Instance ID & NACL-ID for a target VPC - [describe_ec2_securitygroup.py](ec2-samples/describe_ec2_securitygroup)

3. Describe all AMIs for your account across all regions - [describe_ami.py](ec2-samples/describe_ami/)


## Lambda

1. Get underlying Lambda's CPU hardware, /tmp storage, os-release and it's contents  - [get_cpu_info.py](lambda-samples/get_cpu_info/)

2. Create "Memory Used" Metrics for your Lambda functions - [lambda_memory_plot.py](lambda-samples/lambda_memory_plot/)

3. List all Lambda layers and it's info  - [list_layer_info.py](lambda-samples/list_layer_info/)

4. List code storage for a function including all attached layers - [lambda_code_size_including_layers.py](lambda-samples/lambda_code_size_all_functions/)

5. List code storage for all Lambda functions in a region - [lambda_code_size_all_functions.py](lambda-samples/lambda_code_size_including_layers/)

6. Get all functions using reserved or provisional concurrency in a region - [reserved_concurrency.py](lambda-samples/reserved_concurrency/)

7. Test HTTP connection for your Lambda function inside VPC - [http_connection_test.py](lambda-samples/http_connection_test/)

8. Check Async queue congestions and delays in processing async events - [get_async_invoke_delay.py](lambda-samples/get_async_invoke_delay/)

9. List Lambda function version(s) using an ENI - [lambda_hyperplane_eni_checker.py](lambda-samples/lambda_hyperplane_eni_checker/)

10. List all ENIs created by Lambda functions(s) - [lambda_created_enis.py](lambda-samples/lambda_created_enis/)

11. Get Lambda dashboard metrics across all regions - [lambda_dashboard.py](lambda-samples/lambda_dashboard/)

12. Lambda X-Ray examples - [lambda_dashboard.py](lambda-samples/x_ray_sample/)

12. Delete orphaned Event Source Mappings - [clean_orphaned_event_source_mappings.py](lambda-samples/clean_orphaned_event_source_mappings/)

## SNS

1. List all subscriptions tied to a topic in an account  - [list_account_topic_subscriptions.py](sns-samples/list_account_topic_subscriptions/)

2. Programmatically create subscription filters for SNS  - [set_subscription_filters.py](sns-samples/set_subscription_filters/)

3. Programmatically set SenderID while sending SMS text messages  - [sender_id.py](sns-samples/sender_id/)

4. Programmatically set max price while sending SMS text messages - [set_max_price.py](sns-samples/set_max_price_sms/)

5. Get SMS month to date spend in USD - [sms_month_to_date_spent_usd.py](sns-samples/sms_month_to_date_spent_usd/)

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

This is an iterative repository, I'll keep adding more sample codes for more use-cases as I come across them. I have tested all scripts using ```Python3.6``` runtime inside Lambda under ```us-west-2``` region, and most of this should work for all ```Python3``` runtimes (Python 2.7 EOL: :dizzy_face:).

- Fork repo
- Set runtime as ```Python3``` (```Python3.6``` preferred)
- Send your awesome :raised_hands: [Pull Request](https://github.com/shreyasgaonkar/aws-lambda-code-samples/pulls) with code/.md changes
    - Follow Python's [PEP8](https://www.python.org/dev/peps/pep-0008/) coding standards.
    - Commit repo using the [Seven Rules](https://chris.beams.io/posts/git-commit/#seven-rules)
- Your PR gets merged :white_check_mark: and a shoutout :loudspeaker:

## Looking for CLI samples?
- Head to https://github.com/shreyasgaonkar/aws-cli-code-samples

#### Repo structure:

```bash
$ tree
.
├── CODE_OF_CONDUCT.md
├── LICENSE
├── README.md
├── ec2-samples
│   ├── describe_ami
│   │   ├── README.md
│   │   └── describe_ami.py
│   ├── describe_ec2_securitygroup
│   │   ├── README.md
│   │   └── describe_ec2_securitygroup.py
│   └── start_stop_ec2_instances_with_cloudwatch_event
│       ├── README.md
│       └── start_stop_ec2_instances_with_cloudwatch_event.py
├── lambda-layer
│   ├── README.md
│   ├── boto3.zip
│   ├── pandasnumpy.zip
│   ├── prettyTable.zip
│   ├── psycopg2.zip
│   ├── requests.zip
│   └── x-ray.zip
├── lambda-samples
│   ├── get_async_invoke_delay
│   │   ├── README.md
│   │   └── get_async_invoke_delay.py
│   ├── get_cpu_info
│   │   ├── README.md
│   │   └── get_cpu_info.py
│   ├── http_connection_test
│   │   ├── README.md
│   │   └── http_connection_test.py
│   ├── lambda_code_size_all_functions
│   │   ├── README.md
│   │   └── lambda_code_size_all_functions.py
│   ├── lambda_code_size_including_layers
│   │   ├── README.md
│   │   └── lambda_code_size_including_layers.py
│   ├── lambda_created_enis
│   │   ├── README.md
│   │   └── lambda_created_enis.py
│   ├── lambda_dashboard
│   │   ├── README.md
│   │   └── lambda_dashboard.py
│   ├── lambda_hyperplane_eni_checker
│   │   ├── README.md
│   │   └── lambda_hyperplane_eni_checker.py
│   ├── lambda_memory_plot
│   │   ├── README.md
│   │   └── lambda_memory_plot.py
│   ├── list_layer_info
│   │   ├── README.md
│   │   └── list_layer_info.py
│   ├── reserved_concurrency
│   │   ├── README.md
│   │   └── reserved_concurrency.py
│   └── x_ray_sample
│       ├── README.md
│       └── x_ray_sample.py
├── sns-samples
│   ├── list_account_topic_subscriptions
│   │   ├── README.md
│   │   └── list_account_topic_subscriptions.py
│   ├── sender_id
│   │   ├── README.md
│   │   └── sender_id.py
│   ├── set_max_price_sms
│   │   ├── README.md
│   │   └── set_max_price_sms.py
│   ├── set_subscription_filters
│   │   ├── README.md
│   │   └── set_subscription_filters.py
│   └── sms_month_to_date_spent_usd
│       ├── README.md
│       └── sms_month_to_date_spent_usd.py
└── tmp
    └── images
        ├── AWSLambdaCloudWatchAsyncDelay.png
        ├── AWSLambdaCloudWatchMetric.png
        └── AWSLambdaX-Ray.PNG
```
