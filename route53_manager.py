import boto3
import re

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
        print("\nNo hosted zones created by the CLI.")
        return []
    
    print("\nHosted zones created by the CLI:")
    for idx, zone in enumerate(cli_zones, start=1):
        print(f"{idx}. {zone['Name']} ID: {zone['Id'].split('/')[-1]}")
    
    return cli_zones

def list_records(zone_id):
    response = route53.list_resource_record_sets(HostedZoneId=zone_id)
    records = [record for record in response['ResourceRecordSets'] if record['Type'] not in ['NS', 'SOA']]
    
    if not records:
        print("\nNo editable records found in this hosted zone.")
        return []
    
    print("\nExisting DNS Records:")
    for idx, record in enumerate(records, start=1):
        values = ", ".join([r['Value'] for r in record.get('ResourceRecords', [])])
        print(f"{idx}. {record['Name']} ({record['Type']}) -> {values}")
    
    return records

def check_valid_type_to_value(record_type):
    format_examples = {
        "A": "(IPv4 address, e.g., 192.168.1.1)",
        "AAAA": "(IPv6 address, e.g., 2001:db8::1)",
        "CNAME": "(Domain name, e.g., example.com)",
        "TXT": "(Text value, e.g., \"example text\")"
    }
    
    example = format_examples.get(record_type, "(Custom format)")
    print(f"\nExpected format for {record_type} record: {example}")
    
    while True:
        record_value = input("Enter a value for the record: ").strip()
        
        if record_type == "A" and not re.match(r"^\d{1,3}(\.\d{1,3}){3}$", record_value):
            print("Invalid IPv4 address! Please enter a valid IPv4 address.")
        elif record_type == "AAAA" and not re.match(r"^[0-9a-fA-F:]+$", record_value):
            print("Invalid IPv6 address! Please enter a valid IPv6 address.")
        elif record_type == "CNAME" and not re.match(r"^[a-zA-Z0-9.-]+\.[a-zA-Z]+$", record_value):
            print("Invalid domain name! Please enter a valid domain.")
        elif record_type == "TXT":
            if not (record_value.startswith('"') and record_value.endswith('"')):
                record_value = f'"{record_value}"'
            return record_value
        else:
            return record_value

def manage_dns_record():
    cli_zones = list_hosted_zones()
    if not cli_zones:
        print("Can't manage DNS records without a hosted zone. Please create a zone first.")
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
    
    action = ""
    while action not in ["CREATE", "UPDATE", "DELETE"]:
        action = input("\nChoose an action: 'create', 'update' or 'delete': ").strip().upper()
    
    if action == "CREATE":
        record_name = input("Enter a name for the new record: ").strip() + f".{zone_name}"
        record_type = ""
        while record_type not in ["A", "AAAA", "CNAME", "TXT"]:
            record_type = input("Enter record type (A, AAAA, CNAME, TXT): ").strip().upper()
        record_value = check_valid_type_to_value(record_type)
        
        change_batch = {
            'Changes': [{
                'Action': 'CREATE',
                'ResourceRecordSet': {
                    'Name': record_name,
                    'Type': record_type,
                    'TTL': 300,
                    'ResourceRecords': [{'Value': record_value}]
                }
            }]
        }
        route53.change_resource_record_sets(HostedZoneId=zone_id, ChangeBatch=change_batch)
        print(f"Record created: {record_name} -> {record_value}")
    
    elif action == "UPDATE":
        records = list_records(zone_id)
        if not records:
            return
        
        while True:
            try:
                record_choice = int(input("Select a record to update: "))
                if 1 <= record_choice <= len(records):
                    break
                else:
                    print("Invalid choice!")
            except ValueError:
                print("Invalid input! Enter a number.")
        
        selected_record = records[record_choice - 1]
        new_value = check_valid_type_to_value(selected_record['Type'])
        
        change_batch = {
            'Changes': [{
                'Action': 'UPSERT',
                'ResourceRecordSet': {
                    'Name': selected_record['Name'],
                    'Type': selected_record['Type'],
                    'TTL': 300,
                    'ResourceRecords': [{'Value': new_value}]
                }
            }]
        }
        route53.change_resource_record_sets(HostedZoneId=zone_id, ChangeBatch=change_batch)
        print("Record updated successfully!")
    
    elif action == "DELETE":
        records = list_records(zone_id)
        if not records:
            return
        
        while True:
            try:
                record_choice = int(input("Select a record to delete: "))
                if 1 <= record_choice <= len(records):
                    break
                else:
                    print("Invalid choice!")
            except ValueError:
                print("Invalid input! Enter a number.")
        
        selected_record = records[record_choice - 1]
        change_batch = {'Changes': [{'Action': 'DELETE', 'ResourceRecordSet': selected_record}]}
        route53.change_resource_record_sets(HostedZoneId=zone_id, ChangeBatch=change_batch)
        print("Record deleted successfully!")
