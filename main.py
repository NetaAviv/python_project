from ec2_manager import *
from s3_manager import *
from route53_manager import *

def main():
    print("\nWelcome to make your own infra with Neta's CLI tool!")
    stop_program = False
    while not stop_program:
        manage = input(
            "\nEnter 1 - EC2 Management\n"
            "Enter 2 - S3 Management\n"
            "Enter 3 - Route 53 Management\n"
            "Enter 4 - Exit\n"
            "Your input: "
        ).strip()

        if manage == '1':
            while True:
                to_do = input(
                    "\nEC2 Management:\n"
                    "1 - View instances made by the program\n"
                    "2 - Launch a new instance\n"
                    "3 - Start a stopped instance\n"
                    "4 - Stop a running instance\n"
                    "5 - Return to main menu\n"
                    "Your input: "
                ).strip()

                try:
                    if to_do == '1':
                        print("\nYou chose to view instances made by the program.")
                        viewing_request()

                    elif to_do == '2':
                        print("\nYou chose to launch a new EC2 instance.")
                        if len(list_instances("running")) >= 2:
                            raise Exception("Cannot create more than 2 running instances at a time.")
                        else:
                            get_new_instance_details()

                    elif to_do == '3':
                        print("\nYou chose to start a stopped instance.")
                        starting_instance_request()

                    elif to_do == '4':
                        print("\nYou chose to stop a running instance.")
                        stopping_instance_request()

                    elif to_do == '5':
                        print("Returning to main menu...")
                        break

                    else:
                        print("Invalid option. Please enter a valid number.")

                except Exception as e:
                    print(f"An error occurred: {e}")

        elif manage == '2':
            while True:
                to_do = input(
                    "\nS3 Management:\n"
                    "1 - Create a new S3 bucket\n"
                    "2 - Upload a file to a CLI-created S3 bucket\n"
                    "3 - List S3 buckets created by this CLI\n"
                    "4 - Return to main menu\n"
                    "Your input: "
                ).strip()

                try:
                    if to_do == '1':
                        print("\nYou chose to create a new S3 bucket.")
                        create_s3_bucket()

                    elif to_do == '2':
                        print("\nYou chose to upload a file to an S3 bucket.")
                        upload_file_to_s3()

                    elif to_do == '3':
                        print("\nYou chose to list all CLI-created S3 buckets.")
                        list_cli_buckets()

                    elif to_do == '4':
                        print("Returning to main menu...")
                        break

                    else:
                        print("Invalid option. Please enter a valid number.")

                except Exception as e:
                    print(f"An error occurred: {e}")

        elif manage == '3':
            while True:
                to_do = input(
                    "\nRoute53 Management:\n"
                    "1 - Create a new zone\n"
                    "2 - Manage DNS record\n"
                    "3 - List zones created by the program\n"
                    "4 - Return to main menu\n"
                    "Your input: "
                ).strip()

                try:
                    if to_do == '1':
                        print("\nYou chose to create a new zone.")
                        domain_name = input("Please enter a domain name: ").strip()
                        create_hosted_zone(domain_name)

                    elif to_do == '2':
                        print("\nYou chose to manage DNS records.")
                        manage_dns_record()

                    elif to_do == '3':
                        print("\nYou chose to list all hosted zones created by this CLI.")
                        list_hosted_zones()

                    elif to_do == '4':
                        print("Returning to main menu...")
                        break

                    else:
                        print("Invalid option. Please enter a valid number.")

                except Exception as e:
                    print(f"An error occurred: {e}")
        
        elif manage == '4':
            print("Exiting the program...")
            stop_program = True
        
        else:
            print("Invalid input. Please enter a valid number.")

if __name__ == "__main__":
    main()
