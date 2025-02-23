import boto3
import json

route53 = boto3.client('route53')

def create_hosted_zone(domain_name):
    response = route53.create_hosted_zone(
        Name=domain_name,
        CallerReference=str(hash(domain_name)),
        HostedZoneConfig={
            'Comment': 'Hosted zone created via CLI',
            'PrivateZone': False
        }
    )
    hosted_zone_id = response['HostedZone']['Id'].split('/')[-1]
    print(f"Hosted zone created: {domain_name} ID: {hosted_zone_id}")

    # Add the "CreatedByCLI" tag to identify CLI-created zones
    route53.change_tags_for_resource(
        ResourceType='hostedzone',
        ResourceId=hosted_zone_id,
        AddTags=[
            {
                'Key': "CreatedByCLI",
                'Value': "True"
            }
        ]
    )
    print("Finished tagging the hosted zone")
    return hosted_zone_id

def list_hosted_zones():
    response = route53.list_hosted_zones()
    cli_zones = []

    for zone in response['HostedZones']:
        zone_id = zone['Id'].split('/')[-1]  # Extract hosted zone ID
        tag_response = route53.list_tags_for_resource(
            ResourceType='hostedzone',
            ResourceId=zone_id
        )
        
        # Check if the "CreatedByCLI" tag exists and has the correct value
        for tag in tag_response['ResourceTagSet']['Tags']:
            if tag['Key'] == "CreatedByCLI" and tag['Value'] == "True":
                cli_zones.append(zone)

    if not cli_zones:
        print("No hosted zones created by the CLI.")
        return

    print("Hosted zones created by the CLI:")
    for zone in cli_zones:
        print(f"- {zone['Name']} ID: {zone['Id'].split('/')[-1]}")

def manage_dns_record():
    # List CLI-created zones
    response = route53.list_hosted_zones()
    cli_zones = []

    for zone in response['HostedZones']:
        zone_id = zone['Id'].split('/')[-1]  # Extract hosted zone ID
        tag_response = route53.list_tags_for_resource(
            ResourceType='hostedzone',
            ResourceId=zone_id
        )

        # Check if the "CreatedByCLI" tag exists and has the correct value
        for tag in tag_response['ResourceTagSet']['Tags']:
            if tag['Key'] == "CreatedByCLI" and tag['Value'] == "True":
                cli_zones.append({"Name": zone['Name'], "Id": zone_id})

    if not cli_zones:
        print("No hosted zones created by the CLI.")
        return

    # Display numbered list of hosted zones
    print("\nHosted zones created by the CLI:")
    for idx, zone in enumerate(cli_zones, start=1):
        print(f"{idx}. {zone['Name']} (ID: {zone['Id']})")

    # Let the user select a hosted zone by number with validation
    zone_id = None
    while zone_id is None:
        try:
            choice = int(input("\nSelect a hosted zone by number: "))
            if 1 <= choice <= len(cli_zones):
                zone_id = cli_zones[choice - 1]['Id']
            else:
                print(" Invalidinput. Please select a number from the list.")
        except ValueError:
            print(" Invalid input. Please enter a number.")

    # Get valid action from user
    valid_actions = ['CREATE', 'UPSERT', 'DELETE']
    action = None
    while action not in valid_actions:
        action = input("Enter action (CREATE, UPSERT, DELETE): ").strip().upper()
        if action not in valid_actions:
            print(" Invalid action")

    print(f" You chose to {action.lower()} a record.")

    # Get record details
    record_name = input("Enter the record name (e.g., sub.example.com): ").strip()
    record_type = input("Enter record type (A, CNAME, TXT, etc.): ").strip().upper()
    record_value = input("Enter record value (e.g., IP for A record): ").strip()
    ttl = 300  # Default TTL

    # Ensure TXT records are correctly formatted
    if record_type == "TXT":
        record_value = f'"{record_value}"'  # AWS requires TXT values to be quoted

    change_batch = {
        'Comment': 'Managed by CLI',
        'Changes': [
            {
                'Action': action,
                'ResourceRecordSet': {
                    'Name': record_name,
                    'Type': record_type,
                    'TTL': ttl,
                    'ResourceRecords': [{'Value': record_value}]
                }
            }
        ]
    }

    try:
        response = route53.change_resource_record_sets(
            HostedZoneId=zone_id,
            ChangeBatch=change_batch
        )
        print(f" Record {action}d: {record_name} -> {record_value}")
        return response

    except Exception as e:
        print(f" An error occurred: {e}")
