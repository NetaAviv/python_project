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
    
    route53.change_tags_for_resource(
        ResourceType='hostedzone',
        ResourceId=hosted_zone_id,
        AddTags=[{'Key': "CreatedByCLI", 'Value': "True"}]
    )
    print("Finished tagging the hosted zone")
    return hosted_zone_id

def list_hosted_zones():
    response = route53.list_hosted_zones()
    cli_zones = []
    
    for zone in response['HostedZones']:
        zone_id = zone['Id'].split('/')[-1]
        tag_response = route53.list_tags_for_resource(ResourceType='hostedzone', ResourceId=zone_id)
        
        for tag in tag_response['ResourceTagSet']['Tags']:
            if tag['Key'] == "CreatedByCLI" and tag['Value'] == "True":
                cli_zones.append(zone)
    
    if not cli_zones:
        print("No hosted zones created by the CLI.")
        return []
    
    print("Hosted zones created by the CLI:")
    for idx, zone in enumerate(cli_zones, start=1):
        print(f"{idx}. {zone['Name']} ID: {zone['Id'].split('/')[-1]}")
    
    return cli_zones

def list_records(zone_id):
    response = route53.list_resource_record_sets(HostedZoneId=zone_id)
    records = response['ResourceRecordSets']
    
    if not records:
        print("No records found in this hosted zone.")
        return []
    
    print("Records in the hosted zone:")
    for idx, record in enumerate(records, start=1):
        values = ", ".join([r['Value'] for r in record.get('ResourceRecords', [])])
        print(f"{idx}. {record['Name']} ({record['Type']}): {values}")
    
    return records

def manage_dns_record():
    cli_zones = list_hosted_zones()
    if not cli_zones:
        return
    
    while True:
        try:
            choice = int(input("Select a hosted zone by number: "))
            if 1 <= choice <= len(cli_zones):
                break
            else:
                print("Invalid choice! Please select a valid number.")
        except ValueError:
            print("Invalid input! Please enter a number.")
    
    selected_zone = cli_zones[choice - 1]
    zone_id = selected_zone['Id'].split('/')[-1]
    zone_name = selected_zone['Name'].rstrip('.')
    
    valid_actions = ['CREATE', 'UPDATE', 'DELETE']
    action = ""
    while action not in valid_actions:
        action = input("Choose an action 'create', 'update' or 'delete: ").strip().upper()
        if action not in valid_actions:
            print("Invalid action")
        else:
            print(f"You chose to {action.lower()} a record.")
    
    if action == "DELETE":
        records = list_records(zone_id)
        if not records:
            return
        
        while True:
            record_choice = input("Select a record to delete by number (or type 'exit' to exit this page): ").strip()
            if record_choice.lower() == 'exit':
                print("Exiting record deletion...")
                return
            try:
                record_choice = int(record_choice)
                selected_record = records[record_choice - 1]
                
                if selected_record['Type'] in ['NS', 'SOA']:
                    print("Cannot delete NS or SOA records! They are required for the hosted zone.")
                    continue
                
                if 1 <= record_choice <= len(records):
                    break
                else:
                    print("Invalid choice! Please select a valid number.")
            except (ValueError, IndexError):
                print("Invalid input! Please enter a valid number or type 'exit' to cancel.")
        
        record_name = selected_record['Name']
        record_type = selected_record['Type']
        record_value = selected_record['ResourceRecords'][0]['Value']
        
    elif action == "UPDATE":
        action = "UPSERT"
        records = list_records(zone_id)
        if not records:
            return
        
        while True:
            record_choice = input("Select a record by number to modify (or type 'exit' to exit): ").strip()
            if record_choice.lower() == 'exit':
                print("Exiting record update...")
                return
            try:
                record_choice = int(record_choice)
                selected_record = records[record_choice - 1]
                if 1 <= record_choice <= len(records):
                    break
                else:
                    print("Invalid choice! Please select a valid number.")
            except (ValueError, IndexError):
                print("Invalid input! Please enter a valid number or type 'exit' to cancel.")
        
        record_name = selected_record['Name']
        record_type = selected_record['Type']
        record_value = input(f"Enter new value for {record_name} ({record_type}): ").strip()
    
    else:
        record_sub_name = input("Enter the record sub-name (e.g., 'sub' for sub.example.com): ").strip()
        record_name = f"{record_sub_name}.{zone_name}"
        record_type = input("Enter record type (A, CNAME, TXT, etc.): ").strip().upper()
        record_value = input("Enter record value (e.g., IP for A record): ").strip()
    
    ttl = 300
    if record_type == "TXT":
        record_value = f'"{record_value}"'
    
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
        print(f"Record {action.lower()}d: {record_name} -> {record_value}")
        return response
    except Exception as e:
        print(f"An error occurred: {e}")
