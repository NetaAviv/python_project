import boto3

# Initialize EC2 resource
ec2 = boto3.resource('ec2')

# Example of using a specific Ubuntu AMI ID (e.g., ami-01aeb1bc44e073c63)
AMI_ID = "ami-01aeb1bc44e073c63"  # Replace with your selected AMI ID

import boto3

def create_ec2_instance(ami_id, instance_type):
    ec2 = boto3.resource('ec2')

    # Check if the number of running instances with the correct tags is less than 2
    running_instances = [
        instance for instance in ec2.instances.all()
        if instance.state['Name'] == 'running' 
        and 'Created by' in [tag['Key'] for tag in instance.tags]
        and 'Owner' in [tag['Key'] for tag in instance.tags]
        and any(tag['Value'] == 'netaaviv' for tag in instance.tags)  # Check if 'Owner' tag is 'netaaviv'
    ]
    
    if len(running_instances) >= 2:
        raise Exception("Cannot create more than 2 running instances with 'Owner' tag set to 'netaaviv' at a time.")

    # Proceed to create the instance if condition is met
    instances = ec2.create_instances(
        ImageId=ami_id,
        InstanceType=instance_type,
        MinCount=1,
        MaxCount=1,
        TagSpecifications=[{
            'ResourceType': 'instance',
            'Tags': [
                {'Key': 'Created by', 'Value': 'CLI'},
                {'Key': 'Owner', 'Value': 'netaaviv'}
            ]
        }]
    )

    return instances[0].id  # Return the ID of the created instance

def start_instance(instance_id):
    """
    Starts the EC2 instance with the given instance ID.
    """
    instance = ec2.Instance(instance_id)
    instance.start()
    print(f"Started EC2 Instance ID: {instance_id}")


def stop_instance(instance_id):
    """
    Stops the EC2 instance with the given instance ID.
    """
    instance = ec2.Instance(instance_id)
    instance.stop()
    print(f"Stopped EC2 Instance ID: {instance_id}")


def list_instances():
    """
    Lists all EC2 instances created by the CLI (tagged with Owner: netaaviv and Created by: CLI),
    and are in running state.
    """
    ec2 = boto3.resource('ec2')

    # Filter instances that have the tags 'Owner: netaaviv' and 'Created by: CLI', and are running
    instances = ec2.instances.filter(
        Filters=[
            {'Name': 'tag:Owner', 'Values': ['netaaviv']}, 
            {'Name': 'tag:Created by', 'Values': ['CLI']},  # Ensure this filter is added
            {'Name': 'instance-state-name', 'Values': ['running']}
        ]
    )
    
    for instance in instances:
        print(f"Instance ID: {instance.id}, State: {instance.state['Name']}")

def get_latest_ami():
    """
    Returns the latest AMI ID for Ubuntu (hardcoded in this case).
    """
    return AMI_ID
