from ec2_manager import create_ec2_instance, get_latest_ami, list_instances

def main():
    print("Welcome to make your own infra with Neta's CLI tool!")
    
    # List existing instances
    instances = list_instances()
    if len(instances) > 0:
        print("The ids of the instances you have running already:")
        for instance in instances:
            print(f"Instance ID: {instance.id}, State: {instance.state['Name']}")
    else:
        print("You don't have any instances running from this program.")
    
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
        os = input("Please choose an OS for your instance, 'aws linux' or 'ubuntu': ").strip()

        if os not in ["aws linux", "ubuntu"]:
            print("Invalid OS. Please choose either 'aws linux' or 'ubuntu'.")
        else:
            valid_os = True
            print(f"You've selected {os}. Proceeding with instance creation...")
    
    # Get the latest AMI based on OS choice
#    if os == "aws linux":
#        ami_id = get_latest_ami("amazon-linux")
#    elif os == "ubuntu":
#        ami_id = get_latest_ami("ubuntu")
    
    # Create EC2 instance
#    if ami_id:
#        print(f"Using AMI: {ami_id} for {os} and instance type {instance_type}")
#        instance_id = create_ec2_instance(ami_id, instance_type)
#        print(f"Created EC2 Instance with ID: {instance_id}")
#    else:
#        print(f"Could not find a suitable AMI for {os}.")

if __name__ == "__main__":
    main()
