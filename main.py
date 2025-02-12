from ec2_manager import *

def main():
    print("Welcome to make your own infra with Neta's CLI tool!")
    
    to_do = input("Enter 1 - To view all of your running instances made by the program\n"
                  "Enter 2 - To launch a new instance\n"
                  "Enter 3 - To start a stopped instance\n"
                  "Enter 4 - To stop a running instance\n"
                  "Your input: ").strip()

    if to_do == '1':
        instances = list_instances("running")
        print("You chose to view all your running instances.")
        if len(instances) > 0:
            print("The IDs of the instances you have running already:")
            for instance in instances:
                print(f"Instance ID: {instance.id}, State: {instance.state['Name']}")
        else:
            print("You don't have any instances running from this program.")
    
    elif to_do == '2':
        print("You chose to launch a new EC2 instance.")
        
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

    elif to_do == '3':
        print("You chose to start a stopped instance.")
        instances = list_instances("stopped")
        if len(instances) > 0:
            print("Your stopped instances are: ")
            for instance in instances:
                print(f"Instance ID: {instance.id}")
            
            instance_id = input("Enter the ID of the instance you want to start: ").strip()
            start_instance(instance_id)
            print(f"Started instance {instance_id}.")
        else:
            print("You don't have any stopped instances.")

    elif to_do == '4':
        print("You chose to stop a running instance.")
        instances = list_instances("running")
        if len(instances) > 0:
            print("Your running instances are: ")
            for instance in instances:
                print(f"Instance ID: {instance.id}")
            
            instance_id = input("Enter the ID of the instance you want to stop: ").strip()
            stop_instance(instance_id)
            print(f"Stopped instance {instance_id}.")
        else:
            print("You don't have any ruuning instances.")
    else:
        print("That's not a vaild option!")
if __name__ == "__main__":
    main()
