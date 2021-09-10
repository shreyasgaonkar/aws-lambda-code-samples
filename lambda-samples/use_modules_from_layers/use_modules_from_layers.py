import sys
import os
import json
sys.path.insert(0, '/opt/python/')
import urllib3


def lambda_handler(event, context):
    """Main Lambda function"""

    # Print where is the module loaded from
    print(f'urllib3 imported from: {urllib3.__file__}')

    # Print urllib3 version
    print(f'urllib3 version loaded: {urllib3.__version__}')

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
