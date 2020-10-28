[This script](sms_month_to_date_spent_usd.py) will parse CloudWatch logs to determine the current SMSMonthToDateSpentUSD metric for all regions where [SMS is supported](https://docs.aws.amazon.com/sns/latest/dg/sns-supported-regions-countries.html), and spit out the metric along with the Max MonthlySpendLimit.

If your account doesn't support [AWS GovCloud (US) Access](https://aws.amazon.com/govcloud-us/?whats-new-ess.sort-by=item.additionalFields.postDateTime&whats-new-ess.sort-order=desc), the script will mention it.


## Output:
```
+----------------+------------------------------------------+------------------------------------------+
|     Region     |          MonthlySpendLimit ($)           |          SMSMonthToDateSpentUSD          |
+----------------+------------------------------------------+------------------------------------------+
|   us-east-2    |               Default: $1                |                    0                     |
|   us-east-1    |                    10                    |                    0                     |
|   us-west-1    |               Default: $1                |                    0                     |
|   us-west-2    |                    5                     |                 1.61379                  |
|   ap-south-1   |               Default: $1                |                    0                     |
| ap-southeast-1 |                    10                    |                    0                     |
| ap-southeast-2 |                    5                     |                    0                     |
| ap-northeast-1 |               Default: $1                |                    0                     |
|  ca-central-1  |               Default: $1                |                    0                     |
|  eu-central-1  |               Default: $1                |                    0                     |
|   eu-west-1    |               Default: $1                |                    0                     |
|   eu-west-2    |               Default: $1                |                    0                     |
|   eu-west-3    |               Default: $1                |                    0                     |
|   eu-north-1   |               Default: $1                |                    0                     |
|   me-south-1   |  Account not configured for me-south-1   |  Account not configured for me-south-1   |
|   sa-east-1    |               Default: $1                |                    0                     |
| us-gov-west-1  | Account not configured for us-gov-west-1 | Account not configured for us-gov-west-1 |
+----------------+------------------------------------------+------------------------------------------+
```
