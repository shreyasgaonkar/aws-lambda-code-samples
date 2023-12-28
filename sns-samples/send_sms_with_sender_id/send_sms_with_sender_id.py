# -*- coding: utf-8 -*-
import boto3

SNS_CLIENT = boto3.client("sns")
PINPOINT_CLIENT = boto3.client("pinpoint")


MOBILE_ENDPOINT = "+1XXXXXXXXXX"  # Phone number in E.164 Format
SENDERID = "Godzilla"  # Set required SenderID
MESSAGE = "Hello, from AWS SNS!"


def send_message(number, message):
    """Send SMS text message"""
    # Check optional senderid requirements here:
    # https://docs.aws.amazon.com/pinpoint/latest/userguide/channels-sms-countries.html

    try:
        return SNS_CLIENT.publish(
            PhoneNumber=number,
            Message=message,
            MessageAttributes={
                "AWS.SNS.SMS.SenderID": {"DataType": "String", "StringValue": SENDERID}
            },
        )
    except Exception as exp:
        response = f"Message not sent to {number}. Couldn't Validate the endpoint. Exception: {exp}"
        print(exp)
        return response


def validate_phone_number(pinpoint_client, mobile_endpoint):
    is_success_response = False
    try:
        response = pinpoint_client.phone_number_validate(
            NumberValidateRequest={"PhoneNumber": mobile_endpoint}
        )
        is_success_response = True
    except pinpoint_client.exceptions.BadRequestException:
        response = (
            f"Not a valid phone endpoint. Skipping sending message to {mobile_endpoint}"
        )
    except Exception as error:
        response = f"Something went wrong. Error: {error}"

    return (response, is_success_response)


def verify_valid_endpoint(endpoint_type):
    return endpoint_type in ["mobile", "prepaid"]


def return_lambda_execution_object(status_code, response_body):
    return {"statusCode": status_code, "body": response_body}


def lambda_handler(event, context):
    """Main Lambda function"""
    status_code = 200
    response_body, is_success_response = validate_phone_number(
        PINPOINT_CLIENT, MOBILE_ENDPOINT
    )

    if not is_success_response:
        return return_lambda_execution_object(status_code, response_body)

    endpoint_type = response_body["NumberValidateResponse"]["PhoneType"].lower()
    is_endpoint_valid = verify_valid_endpoint(endpoint_type)

    if not is_endpoint_valid:
        response_body = f"Not a valid phone endpoint type. Supported messages types: Mobile/Prepaid. Skipping sending message to {MOBILE_ENDPOINT}"
    else:
        response_body = send_message(number=MOBILE_ENDPOINT, message=MESSAGE)

    return return_lambda_execution_object(status_code, response_body)
