Along with SenderId, you can optionally choose to send SMS messages using one of the short/long codes assigned to your account from the Pinpoint console. This can be programmatically set using ```AWS.MM.SMS.OriginationNumber``` MessageAttributes as per the [docs](https://docs.aws.amazon.com/sns/latest/dg/sms_publish-to-phone.html). If you don't use this parameter, SNS will randomly choose an endpoint for you to ensure message delivery.

### Output:

#### Success:
```json
{
  "statusCode": 200,
  "body": "Success. Message sent to +1XXXXXXXXXX"
}
```

#### Error:
```json
{
  "statusCode": 200,
  "body": "Not a valid phone endpoint type. Supported messages types: Mobile/Prepaid. Skipping sending message to +1XXXXXXXXXX"
}
```
