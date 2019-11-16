import json
import time
import boto3

# Crete EC2 client to list all regions
ec2 = boto3.client('ec2')
response = ec2.describe_regions()
regions = response['Regions']

all_topics = []
result = []


def lambda_handler(event, context):
    """Main function to return subscriptions under all topics for an account"""

    # Get all regions, and create SNS client inside it
    for region in regions:
        client = boto3.client('sns', region_name=region['RegionName'])

        # Paginator to iterate through all results
        list_topics_paginator = client.get_paginator('list_topics')
        list_subscriptions_paginator = client.get_paginator('list_subscriptions_by_topic')

        response_iterator = list_topics_paginator.paginate()

        # Loop over the iterator
        for topic in response_iterator:

            # Check if topic exists in a region
            if topic['Topics']:

                # List all topic ARN
                for i in range(len(topic['Topics'])):

                    # Create list subscription iterator
                    sub_response_iterator = list_subscriptions_paginator.paginate(
                        TopicArn=topic['Topics'][i]['TopicArn'])

                    # Loop through all subs in a topic
                    for sub in sub_response_iterator:
                        subs = []
                        if sub['Subscriptions']:
                            for j in sub['Subscriptions']:
                                subs.append(j['SubscriptionArn'])
                        # print(sub['Subscriptions'])

                    # Append the data to the variable
                    all_topics.append((topic['Topics'][i]['TopicArn'], subs))
                    # Don't throttle the call!
                    time.sleep(0.2)

    # Let's check if all topics are here?
    for i in all_topics:
        print(i)
    # print(all_topics)

    return {
        'statusCode': 200,
        'body': json.dumps('Completed execution')
    }
