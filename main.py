from ec2_manager import *

def main():
    print("Welcome to make your own infra with Neta's CLI tool!")
    stop_program = False
    while not stop_program:
        to_do = input("\nEnter 1 - View instances made by the program\n"
                      "Enter 2 - Launch a new instance\n"
                      "Enter 3 - Start a stopped instance\n"
                      "Enter 4 - Stop a running instance\n"
                      "Enter 5 - Exit the program\n"
                      "Your input: ").strip()

        try:
            if to_do == '1':
                print("You chose to view instances made by the program.")
                viewing_request()

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
                    else:
                        print(f"Invalid instance ID: {instance_id}")
                else:
                    print("You don't have any running instances.")
            
            elif to_do == '5':
                print("Exiting the program...")
                stop_program = True

            else:
                print("That's not a valid option!")

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
