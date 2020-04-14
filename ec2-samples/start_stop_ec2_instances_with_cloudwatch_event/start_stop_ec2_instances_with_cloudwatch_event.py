import datetime
import json
import boto3


# Create EC2 and paginator client for the SDK calls
client = boto3.client('ec2')
paginator = client.get_paginator('describe_instances')

# Filter the paginator with the tags we require
# If the tag name is 'start-stop' with value 'yes',
# we create the filter like this:
# Filters=[{
#     'Name': 'tag:start-stop',
#     'Values': [
#         'yes'
#     ]
# }]
#
# Feel free to change as per the tags on the EC2 instance(s)

paginator = paginator.paginate(Filters=[{
    'Name': 'tag:start-stop',
    'Values': [
        'yes'
    ]
}])

# Create an array to store the instance id's to loop over later
final_result = []


def message(instance_id, state, changed=0):
    """Create a message function to send info back to the original function."""

    # Changed parameter determines what message to return
    if changed != 0:
        return_message = ("Instance {} is in {} state").format(instance_id, state)
    else:
        return_message = "No change for Instance# {}. Currently in {} state".format(
            instance_id, state)
    return return_message


def toggle_state(instance_id, state):
    """Check the current state if it needs to be altered."""

    now = datetime.datetime.now()

    # check if current time in AM or PM
    if now.hour >= 12:
        if state == "stopped":
            final_result.append(message(instance_id, state))
            return True

        # stop instance
        try:
            client.stop_instances(InstanceIds=[instance_id])
            final_result.append(message(instance_id, state, 1))
            return True
        except Exception as e:
            return False

    # If the time is in AM
    else:
        if state == "running":
            final_result.append(message(instance_id, state))
            return True
        else:
            # start instance
            try:
                client.start_instances(InstanceIds=[instance_id])
                final_result.append(message(instance_id, state, 1))
                return True
            except Exception as e:
                return False


def instance_metadata(result):
    """Get instance information and call toggle function"""

    current_state = result['Instances'][0]['State']['Name']
    instance_id = result['Instances'][0]['InstanceId']

    temp = toggle_state(instance_id, current_state)
    if temp:
        return True
    msg = "Something went wrong for InstanceID: {}".format(instance_id)
    return msg


def lambda_handler(event, context):
    """ Main function for Lambda """

    # Loop over the instances to get metadata
    for page in paginator:
        instance_metadata(page['Reservations'][0])

    # Print all the affected resources from this function
    for i in final_result:
        print(i)

    # This is important when dealing with async Lambda function invokes.
    # Services like CloudWatchEvent will trigger Lambda asynchronously
    #
    # If Lambda errors, it will be auto-retried *two* more times.

    return {
        'statusCode': 200,
        'body': json.dumps("Completed execution.")
    }
