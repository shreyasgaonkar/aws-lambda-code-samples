import boto3
regions = client.describe_regions()['Regions']


def lambda_handler(event, context):

    for region in regions:
        region_name = region['RegionName']
        ec2 = boto3.client('ec2', region_name=region_name)
        response = ec2.describe_images(Owners=['Your-Account-Id'])
        print(response)
        print("~~~")
