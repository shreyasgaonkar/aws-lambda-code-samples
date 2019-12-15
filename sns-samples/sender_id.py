# -*- coding: utf-8 -*-
import boto3
client = boto3.client('sns')


def lambda_handler(event, context):

    # Check senderid requirements here:
    # https://docs.aws.amazon.com/pinpoint/latest/userguide/channels-sms-countries.html

    message = 'Hello, from AWS SNS!'
    response = client.publish(
        PhoneNumber='+11XXX5550100',
        Message=message,
        MessageAttributes={
            'AWS.SNS.SMS.SenderID': {
                'DataType': 'String',
                'StringValue': 'Godzilla'
            }})

    print(response)
