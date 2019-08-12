import boto3
import json

client = boto3.client('ec2')

# Enter Target VPC ID
target_vpc_id = '<Enter-VPC-id>'


def lambda_handler(event, context):
    
    # Create an array to store the instance id's to loop over later
    all_instances = []
    
    # Desribe all instances in this region
    result = client.describe_instances()
    
    # Get the instance id from the above call
    for instance in range(len(result['Reservations'])):
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
        
    
    # Check if 'result' call is paginated, if so repeat the call
    try:
        while(result.NextToken):
            get_token = result.NextToken
            result = client.describe_instances(NextToken=get_token)
            
            for instance in range(len(result['Reservations'])):
                 # Check if the instance is in the Target VPC:
                if(result['Reservations'][instance]['Instances'][0]['NetworkInterfaces'][0]['VpcId'] == target_vpc_id):
                    instance_id = (result['Reservations'][instance]['Instances'][0]['InstanceId'])
                    all_instances.append(instance_id)
        
    # This should populate all the instances in all_instance array. Loop over to get the Security groups.
    
    # If no next token found, ignore the above
    except: 
        pass



    # Print Instance and it's Security Group ID

    for i in all_instances:
        print(i)
