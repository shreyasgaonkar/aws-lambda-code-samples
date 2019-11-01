import json
import boto3
client = boto3.client('ec2')
regions = client.describe_regions()['Regions']
         
def lambda_handler(event, context):
    
    for region in regions:
        region_name=region['RegionName']
        ec2 = boto3.client('ec2', region_name=region_name)
        response = client.describe_images(Owners=['Your-Account-Id'])
        print(response)
        print("~~~")
