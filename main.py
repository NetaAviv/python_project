from ec2_manager import *

def main():
    print("Welcome to make your own infra with Neta's CLI tool!")
    
    to_do = input("Enter 1 - View instances made by the program\n"
                  "Enter 2 - Launch a new instance\n"
                  "Enter 3 - Start a stopped instance\n"
                  "Enter 4 - Stop a running instance\n"
                  "Your input: ").strip()

    try:
        if to_do == '1':
            to_view = input("Enter 1 - View running instances\n"
                            "Enter 2 - View stopped instances\n"
                            "Enter 3 - View all\n"
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
                all_instances = list_instances("stopped") + (list_instances("running"))
                if len(all_instances) == 0:
                    print("No instances were made by the program.")
                else:
                    print("The IDs of all instances made by the program:")
                    for instance in all_instances:
                        print(f"Instance ID: {instance.id}, State: {instance.state['Name']}")
            
            else:
                print("Invalid option for viewing instances.")

        elif to_do == '2':
            print("You chose to launch a new EC2 instance.")
            if len(list_instances("running")) >= 2:
                raise Exception("Cannot create more than 2 running instances at a time.")
            else:
                get_new_instance_details()

        elif to_do == '3':
            print("You chose to start a stopped instance.")
            instances = list_instances("stopped")
            if len(instances) > 0:
                print("Your stopped instances are: ")
                for instance in instances:
                    print(f"Instance ID: {instance.id}")
                
                instance_id = input("Enter the ID of the instance you want to start: ").strip()
                if any(instance.id == instance_id for instance in instances):
                    start_instance(instance_id)
                    print(f"Started instance {instance_id}.")
                else:
                    print(f"Invalid instance ID: {instance_id}")
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
                if any(instance.id == instance_id for instance in instances):
                    stop_instance(instance_id)
                    print(f"Stopped instance {instance_id}.")
                else:
                    print(f"Invalid instance ID: {instance_id}")
            else:
                print("You don't have any running instances.")
        else:
            print("That's not a valid option!")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
