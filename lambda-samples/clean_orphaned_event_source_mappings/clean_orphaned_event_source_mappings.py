import json
import os
import boto3
import botocore

# ==================
# Override AWS Region below, otherwise use Lambda function's region
# ==================
REGION_NAME = os.environ.get("REGION_NAME", os.environ["AWS_REGION"])
LAMBDA_CLIENT = boto3.client("lambda", region_name=REGION_NAME)


# Paginator to loop over paginated API calls for functions and event source mappings
LIST_FUNCTIONS_PAGINATOR = LAMBDA_CLIENT.get_paginator("list_functions")
LIST_ESM_PAGINATOR = LAMBDA_CLIENT.get_paginator("list_event_source_mappings")


def get_lambda_function_arns():
    """Retrieve all Lambda function ARNs in the region"""
    function_arns = set()

    for page in LIST_FUNCTIONS_PAGINATOR.paginate():
        for function in page["Functions"]:
            function_arns.add(function["FunctionArn"])
    return function_arns


def get_event_source_mappings():
    """Retrieve all event source mappings and their associated function ARNs and UUIDs"""
    event_source_mappings = []
    for page in LIST_ESM_PAGINATOR.paginate():
        for esm in page["EventSourceMappings"]:
            event_source_mappings.append((esm["FunctionArn"], esm["UUID"]))
    return event_source_mappings


def delete_orphaned_esm(lambda_arn, esm_id):
    """Delete the event source mapping using the UUID (esm_id)"""
    try:
        response = LAMBDA_CLIENT.delete_event_source_mapping(UUID=esm_id)
        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            print(f"Deleted ESM for UUID: {esm_id} associated with {lambda_arn}")
            return True
    except botocore.exceptions.ClientError as error:
        print(f"ClientError: {error}")
    except botocore.exceptions.ParamValidationError as error:
        print(f"ValidationError: {error}")
    except Exception as exp:
        print(f"Unexpected error: {exp}")
    return False


def find_orphaned_esm(function_arns, event_source_mappings):
    """Find orphaned ESM (Event Source Mappings) that are not associated with a valid Lambda function"""
    deleted_esm = set()
    for function_arn, esm_id in event_source_mappings:
        if function_arn not in function_arns:
            if delete_orphaned_esm(function_arn, esm_id):
                deleted_esm.add(esm_id)
    return deleted_esm


def lambda_handler(event, context):
    """Main Lambda function entry point"""

    # Get all Lambda function ARNs and event source mappings
    function_arns = get_lambda_function_arns()
    event_source_mappings = get_event_source_mappings()

    # Find and delete orphaned ESMs
    deleted_esm = find_orphaned_esm(function_arns, event_source_mappings)

    # Prepare response based on deleted ESMs
    if deleted_esm:
        body = f"Deleted {len(deleted_esm)} orphaned Event Source Mappings. See logs for details."
    else:
        body = f"No orphaned Event Source Mappings found in {REGION_NAME}"

    return {"statusCode": 200, "body": body}
