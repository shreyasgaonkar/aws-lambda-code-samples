# -*- coding: utf-8 -*-
import json
import boto3
import botocore


SNS = boto3.client('sns')
PINPOINT = boto3.client('pinpoint')
MOBILE_ENDPOINT = '+1XXXXXXXXXX'  # Phone number in E.164 Format
SENDERID = 'Godzilla'
MESSAGE = 'Hello, from AWS SNS!'


def send_message(number, message):
    """ Send SMS text message """
    # Check optional senderid requirements here:
    # https://docs.aws.amazon.com/pinpoint/latest/userguide/channels-sms-countries.html

    response = SNS.publish(
        PhoneNumber=number,
        Message=message,
        MessageAttributes={
            'AWS.SNS.SMS.SenderID': {
                'DataType': 'String',
                'StringValue': SENDERID
            }})
    print(response)


def lambda_handler(event, context):
    """ Main Lambda function """
    try:
        response = PINPOINT.phone_number_validate(
            NumberValidateRequest={
                'PhoneNumber': MOBILE_ENDPOINT
            }
        )
    except PINPOINT.exceptions.BadRequestException:
        response_body = f"Not a valid phone endpoint. Skipping sending message to {MOBILE_ENDPOINT}"

    except Exception as error:
        response_body = f"Something went wrong. Error: {error}"

    else:
        # Validate the endpoint before sending the message
        try:
            if response['NumberValidateResponse']['PhoneType'].lower() in ['mobile', 'prepaid']:
                send_message(number=MOBILE_ENDPOINT, message=MESSAGE)
                response_body = f"Success. Message sent to {MOBILE_ENDPOINT}"
            else:
                response_body = f"Not a valid phone endpoint type. Supported messages types: Mobile/Prepaid. Skipping sending message to {MOBILE_ENDPOINT}"

        except Exception as exp:
            response_body = f"Message not sent to {MOBILE_ENDPOINT}. Couldn't Validate the endpoint. Exception: {exp}"
            print(exp)

    return {
        'statusCode': 200,
        'body': response_body
    }
