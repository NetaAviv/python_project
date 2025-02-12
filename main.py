from ec2_manager import create_ec2_instance, get_latest_ami

def main():
    print("Welcome to make your own infra with Neta's CLI tool!")
    valid_instance_type = False  # Fix typo here

    while not valid_instance_type:
        instance_type = input("Please choose an instance type (t3.nano or t4g.nano): ").strip()
        
        if instance_type not in ["t3.nano", "t4g.nano"]:
            print("Invalid instance type. Please choose either 't3.nano' or 't4g.nano'.")
        else:
            valid_instance_type = True 
            print(f"You've selected {instance_type}.")
    
    valid_os = False
    while not valid_os:
        os = input("Please choose an os for you instance, 'aws linux' or 'ubuntu'. ").strip()

        if os not in ["aws linux", "ubuntu"]:
            print("Invalid os. Please choose either 'aws linux' or 'ubuntu'.")
        else:
            valid_os = True
            print(f"You've selected {os}. Proceeding with instance creation...")

if __name__ == "__main__":
    main()
