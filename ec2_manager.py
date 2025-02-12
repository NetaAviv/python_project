import boto3

ec2 = boto3.resource('ec2')

def list_instances(state):
    # Lists all EC2 instances with the required tags and chosen state
    running_instances = [
        instance for instance in ec2.instances.all()
        if instance.state['Name'] == state
        and instance.tags  # Ensure tags exist
        and any(tag['Key'] == 'Created by' and tag['Value'] == 'CLI' for tag in instance.tags)
        and any(tag['Key'] == 'Owner' and tag['Value'] == 'netaaviv' for tag in instance.tags)
    ]
    return running_instances

def get_matching_ami(instance_type, os):
    ec2 = boto3.client('ec2')

    # Filters based on OS and instance type
    filters = []
    if os == 'ubuntu':
        filters.append({'Name': 'name', 'Values': ['ubuntu*']})
    elif os == 'amazon-linux':
        filters.append({'Name': 'name', 'Values': ['amzn2-ami-hvm*']})

    # Determine architecture based on instance type
    architecture = 'x86_64' if instance_type == 't3.nano' else 'arm64'
    filters.append({'Name': 'architecture', 'Values': [architecture]})

    try:
        # Fetching the images based on filters
        response = ec2.describe_images(Filters=filters, Owners=['amazon'])

        # Get the most recent AMI based on the creation date
        if response['Images']:
            latest_ami = max(response['Images'], key=lambda x: x['CreationDate'])
            return latest_ami['ImageId']
        else:
            raise Exception("No matching AMIs found for the given OS and instance type.")
    except Exception as e:
        raise Exception(f"Error retrieving AMIs: {e}")

def create_ec2_instance(ami_id, instance_type, instance_name):
    if instance_type not in ["t3.nano", "t4g.nano"]:
        raise Exception("Invalid instance type. Choose either 't3.nano' or 't4g.nano'.")

    if len(list_instances("running")) >= 2:
        raise Exception("Cannot create more than 2 running instances with 'Owner' tag set to 'netaaviv' at a time.")

    try:
        instances = ec2.create_instances(
            ImageId=ami_id,
            InstanceType=instance_type,
            MinCount=1,
            MaxCount=1,
            TagSpecifications=[{
                'ResourceType': 'instance',
                'Tags': [
                    {'Key': 'Name', 'Value': instance_name},
                    {'Key': 'Created by', 'Value': 'CLI'},
                    {'Key': 'Owner', 'Value': 'netaaviv'}
                ]
            }]
        )
        return instances[0].id  # Return the instance ID
    except Exception as e:
        raise Exception(f"Failed to create EC2 instance: {e}")

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
