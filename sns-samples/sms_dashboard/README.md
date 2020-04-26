[This script](sms_dashboard.sh) will parse SMS UsageReport S3 bucket to display Total number of messages sent in a month.

This will download and extract all the ```.csv.gz``` files created by SNS under S3 bucket to extract the "TotalParts" - giving us more accurate representation of the number of SMS' sent in a calendar month.

Replace the s3 sync command to point to your S3 bucket configured with the usage plans, and replace the XX at the end with the month for the targeted month.

**Usage**:

```bash
$ bash sms-usage-report.sh
```
OR

```bash
$ chmod +x sms-usage-report.sh && ./sms-usage-report.sh
```

**Output**:

```bash
Creating new directory under /tmp/SMSUsageReports
Total SMS sent: 50
Deleting /tmp/SMSUsageReports
```
