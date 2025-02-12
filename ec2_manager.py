import boto3
ec2 = boto3.resource('ec2')

def list_instances():
    print("Lists all running EC2 instances that have the 'Created by' tag with value 'CLI' and 'Owner' tag with value 'netaaviv'.")
    running_instances = [
        instance for instance in ec2.instances.all()
        if instance.state['Name'] == 'running' 
        and any(tag['Key'] == 'Created by' and tag['Value'] == 'CLI' for tag in instance.tags)
        and any(tag['Key'] == 'Owner' and tag['Value'] == 'netaaviv' for tag in instance.tags)
    ]
    return running_instances

def create_ec2_instance(ami_id, instance_type):
    if instance_type not in ["t3.nano", "t4g.nano"]:
        raise Exception("Invalid instance type. Choose either 't3.nano' or 't4g.nano'.")

    # Check if the number of running instances with the correct tags is less than 2   
    if len(list_instances()) >= 2:
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
    print("Starting ...")
    instance = ec2.Instance(instance_id)
    instance.start()
    print(f"Started EC2 Instance ID: {instance_id}")


def stop_instance(instance_id):
    print("Stopping ...")
    instance = ec2.Instance(instance_id)
    instance.stop()
    print(f"Stopped EC2 Instance ID: {instance_id}")


def choose_ami(instance_type, instance_os):
    """
    Returns the latest AMI ID for Ubuntu (hardcoded in this case).
    """
    return AMI_ID
