import boto3
import configparser

ec2 = boto3.resource('ec2')

def load_user_data():
    #Reads the user_data script from the user data file 
    try:
        with open("user_data", "r") as file:
            return file.read()
    except Exception as e:
        print(f"Error reading user_data file: {e}")
        return ""

def load_configuration():
    config = configparser.ConfigParser()
    config.read("configuration")
    vpc_id = config["VPC"]["vpc_id"]
    subnet_id = config["VPC"]["subnet_id"]
    key_name = config["SSH"]["key_name"]

    return vpc_id, subnet_id, key_name

def list_instances(state):
    # Lists all EC2 instances with the required tags and chosen state
    instances = [
        instance for instance in ec2.instances.all()
        if instance.state['Name'] == state
        and instance.tags  # Ensure tags exist
        and any(tag['Key'] == 'Created by' and tag['Value'] == 'CLI' for tag in instance.tags)
        and any(tag['Key'] == 'Owner' and tag['Value'] == 'netaaviv' for tag in instance.tags)
    ]
    return instances
    
def print_instances_details(list_of_instances):
    for instance in list_of_instances:
        public_ip = instance.public_ip_address if instance.public_ip_address else "No Public IP"
        name_tag = next((tag['Value'] for tag in instance.tags if tag['Key'] == 'Name'), "No Name")
        print(f"Instance ID: {instance.id}, Name: {name_tag}, State: {instance.state['Name']}, Public IP: {public_ip}")

def viewing_request():
    # Handles user input for viewing instances
    to_view = '0'
    while to_view != '4':
        to_view = input("\nEnter 1 - View running instances\n"
                        "Enter 2 - View stopped instances\n"
                        "Enter 3 - View all\n"
                        "Enter 4 - Return to main ec2 managment page\n"
                        "Your input: ").strip()

        if to_view == '1':
            print("\nRunning instances:")
            running_instances = list_instances("running")
            if len(running_instances) == 0:
                print("\nNo running instances.")
            else:
                print_instances_details(running_instances)
        elif to_view == '2':
            print("\nStopped instances:")
            stopped_instances = list_instances("stopped")
            if len(stopped_instances) == 0:
                print("\nNo stopped instances.")
            else:
                print_instances_details(stopped_instances)
        elif to_view == '3':
            print("\nAll instances:")
            all_instances = list_instances("stopped") + list_instances("running")
            if len(all_instances) == 0:
                print("\nNo instances were made by the program.")
            else:
                print_instances_details(all_instances)
        elif to_view == '4':
            print("Returning back to main ec2 managment page...")
        else:
            print("Invalid option! Please enter a valid option.")


def starting_instance_request():
    instances = list_instances("stopped")

    if instances:
        print("\nYour stopped instances are: ")
        for i, instance in enumerate(instances):
            print(f"{i+1}: ", end="")
            print_instances_details([instance])

        if len(list_instances("running")) >= 2:
            print("You already have 2 running instances, you are not allowed to start another.")
        else:
            try:
                chosen_instance_num = int(input("Enter the number of the instance you want to start: ").strip()) - 1
                if 0 <= chosen_instance_num < len(instances):
                    start_instance(instances[chosen_instance_num].id)
                else:
                    print(f"Invalid instance number: {chosen_instance_num + 1}")
            except ValueError:
                print("Please enter a valid number.")
    else:
        print("You don't have any stopped instances.")

def stopping_instance_request():
    instances = list_instances("running")  # Get running instances instead of stopped ones
    if len(instances) > 0:
        print("\nYour running instances are: ")
        for i, instance in enumerate(instances):  # Fixed iteration with enumerate
            print(f"{i+1}: ", end="")
            print_instances_details([instance])
        try:
            chosen_instance_num = int(input("Enter the number of the instance you want to stop: ").strip()) - 1
            if 0 <= chosen_instance_num < len(instances):
                stop_instance(instances[chosen_instance_num].id)  # Pass instance id to stop
            else:
                print(f"Invalid instance number: {chosen_instance_num + 1}")
        except ValueError:
            print("Please enter a valid number.")
    else:
        print("You don't have any running instances.")

def get_matching_ami(instance_type, os):
    if instance_type not in ['t3.nano', 't4g.nano']:
        raise ValueError("Invalid instance type. Only 't3.nano' and 't4g.nano' are supported.")

    ssm_client = boto3.client('ssm')

    if os == 'ubuntu':
        if instance_type == 't3.nano':
            parameter_name = "/aws/service/canonical/ubuntu/server/jammy/stable/current/amd64/hvm/ebs-gp2/ami-id"
        else:  # t4g.nano (ARM-based)
            parameter_name = "/aws/service/canonical/ubuntu/server/jammy/stable/current/arm64/hvm/ebs-gp2/ami-id"

    elif os == 'amazon-linux':
        if instance_type == 't3.nano':
            parameter_name = "/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64"
        else:  # t4g.nano (ARM-based)
            parameter_name = "/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-arm64"

    else:
        raise ValueError("Invalid OS. Only 'ubuntu' and 'amazon-linux' are supported.")

    try:
        response = ssm_client.get_parameter(Name=parameter_name)
        ami_id = response['Parameter']['Value']
        print(f"Latest AMI ID for {os} ({instance_type}): {ami_id}")
        return ami_id

    except Exception as e:
        raise Exception(f"Error retrieving AMI: {e}")

def get_new_instance_details():
    # Choose instance type
    valid_instance_type = False
    while not valid_instance_type:
        instance_type = input("Please choose an instance type, 't3.nano' or 't4g.nano': ").strip()
        if instance_type not in ["t3.nano", "t4g.nano"]:
            print("Invalid instance type. Please choose either 't3.nano' or 't4g.nano'.")
        else:
            valid_instance_type = True
            print(f"You've selected {instance_type}.")
    
    # Choose OS
    valid_os = False
    while not valid_os:
        os = input("/nPlease choose an OS for your instance, 'amazon-linux' or 'ubuntu': ").strip()
        if os not in ["amazon-linux", "ubuntu"]:
            print("Invalid OS. Please choose either 'amazon-linux' or 'ubuntu'.")
        else:
            valid_os = True
            print(f"You've selected {os}. Proceeding with instance creation...")

    print("Trying to find the perfect AMI based on your choices...")
    try:
        ami_id = get_matching_ami(instance_type, os)  # Get the latest AMI based on OS and instance type
        if ami_id:
            print(f"Found AMI: {ami_id}")
            instance_name = input("\nChoose a name for the new instance: ").strip()
            print("Creating the instance...")
            new_instance_id = create_ec2_instance(ami_id, instance_type, instance_name)
            print(f"\nCreated EC2 Instance with ID: {new_instance_id}")
        else:
            print("\nFailed to find a suitable AMI.")
    except Exception as e:
        print(f"Error: {e}")

def create_ec2_instance(ami_id, instance_type, instance_name):
    use_userdata = input("Do you want to install Git and Python on the instance? (yes/no): ").strip().lower()
    if use_userdata == "yes":
        print("Ok, will install git and python")
        user_data = load_user_data()
    else:
        print("Ok,will not install git or python")
        user_data = ""
    try:
        vpc_id, subnet_id, key_name = load_configuration()
        instances = ec2.create_instances(
            ImageId=ami_id,
            KeyName=key_name,
            SubnetId=subnet_id,
            InstanceType=instance_type,
            MinCount=1,
            MaxCount=1,
            UserData=user_data,
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
