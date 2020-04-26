#!/bin/bash
echo "Creating new directory under /tmp/SMSUsageReports"
mkdir /tmp/SMSUsageReports
cd /tmp/SMSUsageReports

aws s3 sync --only-show-errors s3://<usage-report-S3-bucket>/SMSUsageReports/us-west-2/2020/04 . && find . –name "*.gz" 2> /dev/null | xargs gunzip 2> /dev/null
TOTALSMS=$(find . -type d | cat */* | awk -F ',' '{count[$8]++} END {for (word in count) print word, count[word]}' | grep -v  TotalParts | awk -F " " '{print $2}')
echo "Total SMS sent: ${TOTALSMS}"

echo "Deleting /tmp/SMSUsageReports"
rm -r /tmp/SMSUsageReports
