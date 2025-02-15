import boto3

ec2 = boto3.resource('ec2')

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

def viewing_request():
    # Handles user input for viewing instances
    to_view = '0'
    while to_view != '4':  # Corrected the 'while' loop condition for proper exit
        to_view = input("\nEnter 1 - View running instances\n"
                        "Enter 2 - View stopped instances\n"
                        "Enter 3 - View all\n"
                        "Enter 4 - Return to main page\n"
                        "Your input: ").strip()

        if to_view == '1':
            running_instances = list_instances("running")
            if len(running_instances) == 0:
                print("No running instances.")
            else:
                print("The IDs of the instances you have running already:")
                for instance in running_instances:
                    print(f"Instance ID: {instance.id}, State: {instance.state['Name']}")

        elif to_view == '2':
            stopped_instances = list_instances("stopped")
            if len(stopped_instances) == 0:
                print("No stopped instances.")
            else:
                print("The IDs of the stopped instances:")
                for instance in stopped_instances:
                    print(f"Instance ID: {instance.id}, State: {instance.state['Name']}")

        elif to_view == '3':
            all_instances = list_instances("stopped") + list_instances("running")
            if len(all_instances) == 0:
                print("No instances were made by the program.")
            else:
                print("The IDs of all instances made by the program:")
                for instance in all_instances:
                    print(f"Instance ID: {instance.id}, State: {instance.state['Name']}")

        elif to_view == '4':
            print("Returning back to the main page.")

        else:
            print("Invalid option! Please enter a valid option.")

def starting_instance_request():
    instances = list_instances("stopped")
    if len(instances) > 0:
        print("\nYour stopped instances are: ")
        for i, instance in enumerate(instances):  # Fixed iteration with enumerate
            print(f"{i + 1}: Instance ID: {instance.id}")

        try:
            chosen_instance_num = int(input("Enter the number of the instance you want to start: ").strip()) - 1
            if 0 <= chosen_instance_num < len(instances):
                start_instance(instances[chosen_instance_num].id)  # Pass instance id to start
            else:
                print(f"Invalid instance number: {chosen_instance_num + 1}")
        except ValueError:
            print("Please enter a valid number.")
    else:
        print("You don't have any stopped instances.")


def stopping_instance_request():
    print("\n")
    instances = list_instances("running")  # Get running instances instead of stopped ones
    if len(instances) > 0:
        print("Your running instances are: ")
        for i, instance in enumerate(instances):  # Fixed iteration with enumerate
            print(f"{i + 1}: Instance ID: {instance.id}")

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
    ec2_client = boto3.client('ec2')

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
        response = ec2_client.describe_images(Filters=filters, Owners=['amazon'])

        # Get the most recent AMI based on the creation date
        if response['Images']:
            latest_ami = max(response['Images'], key=lambda x: x['CreationDate'])
            return latest_ami['ImageId']
        else:
            raise Exception(f"No matching AMIs found for the given OS '{os}' and instance type '{instance_type}'.")
    except Exception as e:
        raise Exception(f"Error retrieving AMIs: {e}")

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
        os = input("Please choose an OS for your instance, 'amazon-linux' or 'ubuntu': ").strip()
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
            instance_name = input("Choose a name for the new instance: ").strip()
            print("Creating the instance...")
            new_instance_id = create_ec2_instance(ami_id, instance_type, instance_name)
            print(f"Created EC2 Instance with ID: {new_instance_id}")
        else:
            print("Failed to find a suitable AMI.")
    except Exception as e:
        print(f"Error: {e}")

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
