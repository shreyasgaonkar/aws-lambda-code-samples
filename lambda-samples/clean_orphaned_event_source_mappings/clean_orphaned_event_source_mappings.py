import json
import os
import boto3

LAMBDA_CLIENT = boto3.client('lambda', region_name='us-east-1')

# Paginator to loop over paginated API calls
LIST_FUNCTIONS_PAGINATOR = LAMBDA_CLIENT.get_paginator('list_functions')
LIST_FUNCTIONS_PAGE_ITERATOR = LIST_FUNCTIONS_PAGINATOR.paginate()

LIST_ESM_PAGINATOR = LAMBDA_CLIENT.get_paginator('list_event_source_mappings')
LIST_ESM_PAGE_ITERATOR = LIST_ESM_PAGINATOR.paginate()

# Create set to keep track
LIST_FUNTIONS = set()
DELETED_ESM = set()


def find_orphaned_esm():
    """Return all ESM and FunctionArn in this region"""
    functions = LIST_FUNCTIONS_PAGE_ITERATOR.search("Functions[*].FunctionArn")
    for function in functions:
        LIST_FUNTIONS.add(function)

    esms = LIST_ESM_PAGE_ITERATOR.search("EventSourceMappings[*].[FunctionArn,UUID]")
    for esm in esms:
        # if this function valid?
        if esm[0] not in LIST_FUNTIONS:
            delete_orphaned_esm(esm[0], esm[1])
    return True


def delete_orphaned_esm(lambda_arn, uuid):
    """Delete the event source mapping using the UUID"""
    try:
        response = LAMBDA_CLIENT.delete_event_source_mapping(UUID=uuid)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            print(f"Deleted ESM for UUID: {uuid} associated with {lambda_arn}")
            DELETED_ESM.add(uuid)
    except Exception as exp:
        print(exp)
    return True


def lambda_handler(event, context):
    """Main Lambda function"""

    find_orphaned_esm()
    if DELETED_ESM:
        body = "See logs for deleted Event Source Mappings"
    else:
        body = f"No orphaned Event Source mappings found in {os.environ['AWS_REGION']}"
    return {
        'statusCode': 200,
        'body': json.dumps(body)
    }
