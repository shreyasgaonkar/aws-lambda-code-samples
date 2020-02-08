# -*- coding: utf-8 -*-
import boto3
client = boto3.client('sns')


def lambda_handler(event, context):
    """ Main function to send SMS message if the price is under the target """

    # Check country/network specific pricing here:
    # https://aws.amazon.com/sns/sms-pricing/

    message = 'Hello, from AWS SNS!'
    response = client.publish(
        PhoneNumber='+11XXX5550100',
        Message=message,
        MessageAttributes={
            'AWS.SNS.SMS.MaxPrice': {
                'DataType': 'Number',
                'StringValue': '0.10'
            }})

    print(response)

    # Above publish call will not send message if the message cost is over $0.1
    # The SDK call will succeed, however the message will not be sent.
    # https://docs.aws.amazon.com/sns/latest/dg/sms_publish-to-phone.html#sms_publish_sdk
