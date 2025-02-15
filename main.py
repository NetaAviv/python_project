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
                starting_instance_request()

            elif to_do == '4':
                print("You chose to stop a running instance.")
                stopping_instance_request()

            elif to_do == '5':
                print("Exiting the program...")
                stop_program = True

            else:
                print("That's not a valid option!")

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
