import boto3
import json

client = boto3.client('ec2')

target_vpc_id = '<Enter-VPC=ID>'

# Create an array to store the instance id's to loop over later
all_instances = []

# Function defination outside the handler for faster function execution
# This will get all the required metadata - instance id, associated subnet and the NACL id for the target VPC.
def instanceMetadata(instance, result):
    # Check if the instance is in the Target VPC:
    if(result['Reservations'][instance]['Instances'][0]['NetworkInterfaces'][0]['VpcId'] == target_vpc_id):
        instance_id = result['Reservations'][instance]['Instances'][0]['InstanceId']
        security_group_id = result['Reservations'][instance]['Instances'][0]['NetworkInterfaces'][0]['Groups'][0]['GroupId']
        subnet_id = result['Reservations'][instance]['Instances'][0]['NetworkInterfaces'][0]['SubnetId']
        
        response = client.describe_network_acls(
            Filters=[
                {
                    'Name': 'association.subnet-id',
                    'Values': [subnet_id]
                }
            ]
        )
        nac_id = response['NetworkAcls'][0]["NetworkAclId"]
        all_instances.append(("Instance id: " + instance_id, "Security Group ID: " + security_group_id, "NACL id: " + nac_id))
            

def lambda_handler(event, context):
    
    # Desribe all instances in this region
    
    # While True will simulate do-while in python to make the first call, and check if any subsequent calls are needed
    
    while(True):
        
        # First SDK call to get all instances.
        result = client.describe_instances()
        
        # Get the instance id from the above call
        for instance in range(len(result['Reservations'])):
            instanceMetadata(instance, result)
            
        
        # Check if 'result' call is paginated, if so repeat the call
        try:
            while(result.NextToken):
                # If the first SDK call was paginated, it will return 'NextToken', use that to make the next SDK calls to desribe other instances.
                get_token = result.NextToken
                result = client.describe_instances(NextToken=get_token)
                
                # Get the instance id from the above call
                for instance in range(len(result['Reservations'])):
                   
                    instanceMetadata(instance, result)
            
        # This should populate all the instances in all_instance array. Loop over to get the Security groups.
        
        # If no next token found, break the loop
        except: 
            break;



    # Print Instance and it's Security Group ID

    for i in all_instances:
        print(i)

    # print(all_instances)
    
