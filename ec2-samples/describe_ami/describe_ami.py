import boto3
CLIENT = boto3.client('ec2')
REGIONS = CLIENT.describe_regions()['Regions']


def lambda_handler(event, context):

    for region in REGIONS:
        region_name = region['RegionName']
        ec2 = boto3.client('ec2', region_name=region_name)
        response = ec2.describe_images(Owners=['Your-Account-Id'])
        print(response)
        print("~~~")
