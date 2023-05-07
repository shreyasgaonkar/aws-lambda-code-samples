# -*- coding: utf-8 -*-
import boto3
from functools import lru_cache

SNS_CLIENT = boto3.client("sns")
PINPOINT_CLIENT = boto3.client("pinpoint")
MOBILE_ENDPOINT = "+1XXXXXXXXXX"  # Phone number in E.164 Format
MESSAGE = "Hello, from AWS SNS!"
ORIGINATING_NUMBER = "+1XXXXXXXXXX"  # Optional: Select short/long code from Pinpoint SMS and voice console


@lru_cache
def validate_endpoint(mobile_endpoint):
    """
    Validates the mobile endpoint and returns the validation result.
    """
    try:
        response = PINPOINT_CLIENT.phone_number_validate(
            NumberValidateRequest={"PhoneNumber": MOBILE_ENDPOINT}
        )
    except PINPOINT_CLIENT.exceptions.BadRequestException:
        validation_result = (
            f"Not a valid phone endpoint. Skipping sending message to {mobile_endpoint}"
        )
    except PINPOINT_CLIENT.exceptions.ServiceException as error:
        validation_result = f"Service error. Error: {error}"
    except Exception as error:
        validation_result = f"Something went wrong. Error: {error}"
    else:
        if response["NumberValidateResponse"]["PhoneType"].lower() in {
            "mobile",
            "prepaid",
            "voip",
        }:
            validation_result = "valid"
        else:
            validation_result = f"Not a valid phone endpoint type. Supported messages types: Mobile/Prepaid/VOIP. Skipping sending message to {mobile_endpoint}"
    return validation_result


def send_message(number, message):
    """
    Sends an SMS text message to the specified mobile endpoint.
    """

    try:
        message_attributes = {
            "AWS.MM.SMS.OriginationNumber": {
                "DataType": "String",
                "StringValue": ORIGINATING_NUMBER,
            }
        }
    except NameError:
        message_attributes = {}

    SNS_CLIENT.publish(
        PhoneNumber=number, Message=message, MessageAttributes=message_attributes
    )


def lambda_handler(event, context):
    """Main Lambda function"""

    response_body = validate_endpoint(MOBILE_ENDPOINT)

    if response_body == "valid":
        try:
            send_message(number=MOBILE_ENDPOINT, message=MESSAGE)
        except Exception as exp:
            response_body = f"Message not sent to {MOBILE_ENDPOINT}. Couldn't Validate the endpoint. Exception: {exp}"
        else:
            response_body = f"Success. Message sent to {MOBILE_ENDPOINT}"

    print(response_body)
    return {"statusCode": 200, "body": response_body}
