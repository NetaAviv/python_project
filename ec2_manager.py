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

def get_new_instance_details():
        # Choose instance type
        valid_instance_type = False
        while not valid_instance_type:
            instance_type = input("Please choose an instance type (t3.nano or t4g.nano): ").strip()
            if instance_type not in ["t3.nano", "t4g.nano"]:
                print("Invalid instance type. Please choose either 't3.nano' or 't4g.nano'.")
            else:
                valid_instance_type = True
                print(f"You've selected {instance_type}.")
        
        # Choose OS
        valid_os = False
        while not valid_os:
            os = input("Please choose an OS for your instance, 'amazon-linux' or 'ubuntu': ").strip()
            if os not in ["amazon-linux", "ubuntu"]:
                print("Invalid OS. Please choose either 'amazon-linux' or 'ubuntu'.")
            else:
                valid_os = True
                print(f"You've selected {os}. Proceeding with instance creation...")

        print("Trying to find the perfect AMI based on your choices...")
        ami_id = get_matching_ami(instance_type, os)  # Get the latest AMI based on OS and instance type
        
        if ami_id:
            print(f"Found AMI: {ami_id}")
            instance_name = input("Choose a name for the new instance: ").strip()
            print("Creating the instance...")
            new_instance_id = create_ec2_instance(ami_id, instance_type, instance_name)
            print(f"Created EC2 Instance with ID: {new_instance_id}")
        else:
            print("Failed to find a suitable AMI.")


def create_ec2_instance(ami_id, instance_type, instance_name):
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
    instance = ec2.Instance(instance_id)
    tags = {tag['Key']: tag['Value'] for tag in instance.tags or []}
    if tags.get('Owner') == 'netaaviv' and tags.get('Created by') == 'CLI':
        print("Starting ...")
        instance.start()
        print(f"Started EC2 Instance ID: {instance_id}")
    else:
        print("Instance does not have the required tags. Cannot start.")

def stop_instance(instance_id):
    instance = ec2.Instance(instance_id)
    tags = {tag['Key']: tag['Value'] for tag in instance.tags or []}
    if tags.get('Owner') == 'netaaviv' and tags.get('Created by') == 'CLI':
        print("Stopping ...")
        instance.stop()
        print(f"Stopped EC2 Instance ID: {instance_id}")
    else:
        print("Instance does not have the required tags. Cannot stop.")
