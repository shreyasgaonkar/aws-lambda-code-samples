# AWS Lambda ENI Analyzer

## Overview

This [AWS Lambda function](lambda_created_enis.py) identifies and reports all Elastic Network Interfaces (ENIs) created by Lambda function(s) in a region.

## Features

- Retrieves all ENIs associated with AWS Lambda VPC configurations
- Generates a report of ENI Id, it's current status, VPC-ID, Subnet-ID and the Security Groups used


## Prerequisites

- `prettytable` as Lambda layer
- AWS account with appropriate permissions

## Lambda Layer

- Uses [PrettyTable](https://pypi.org/project/PrettyTable/) module imported as a [Lambda layer](/lambda-layer/prettyTable.zip).

## Output:

```bash
+-----------------------+--------+--------------+-----------------+-----------------------------------------------+
|         ENI ID        | Status |    VPC ID    |    Subnet Id    |                Security Groups                |
+-----------------------+--------+--------------+-----------------+-----------------------------------------------+
| eni-XXXXXXXXXXXXXXXXX | in-use | vpc-XXXXXXXX | subnet-XXXXXXXX |                ['sg-XXXXXXXX']                |
| eni-XXXXXXXXXXXXXXXXX | in-use | vpc-XXXXXXXX | subnet-XXXXXXXX |         ['sg-XXXXXXXX', 'sg-XXXXXXXX']        |
| eni-XXXXXXXXXXXXXXXXX | in-use | vpc-XXXXXXXX | subnet-XXXXXXXX | ['sg-XXXXXXXX', 'sg-XXXXXXXX', 'sg-XXXXXXXX'] |
+-----------------------+--------+--------------+-----------------+-----------------------------------------------+
```

## Further reading

Looking for Lambda function(s) and its versions if they are using a particular ENI? Try [lambda_hyperplane_eni_checker](../lambda_hyperplane_eni_checker/)
