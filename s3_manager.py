import boto3
import configparser
import json
import os

s3_client = boto3.client('s3')

def load_s3_configuration():
    config = configparser.ConfigParser()
    config.read("configuration")
    return config["S3"]["default_bucket_prefix"]

def create_s3_bucket():
    print("You chose to create an S3 bucket:")
    default_prefix = load_s3_configuration()
    bucket_name = input(f"Enter a name for your bucket (prefix '{default_prefix}'): ").strip()

    if not bucket_name.startswith(default_prefix):
        bucket_name = f"{default_prefix}{bucket_name}"

    # Check if the bucket already exists
    existing_buckets = [bucket["Name"] for bucket in s3_client.list_buckets()["Buckets"]]
    if bucket_name in existing_buckets:
        print(f"The bucket name must be unique, bucket '{bucket_name}' already exists.")
        return

    public_access = input("Do you want this bucket to be public? (yes/no): ").strip().lower()
    if public_access == "yes":
        confirm = input("Are you sure you want to make this bucket public? (yes/no): ").strip().lower()
        if confirm != "yes":
            print(" OK, bucket will be private.")
            public_access = "no"

    try:
        s3_client.create_bucket(Bucket=bucket_name)
        if public_access == "yes":
            s3_client.put_public_access_block(
                Bucket=bucket_name,
                PublicAccessBlockConfiguration={
                    "BlockPublicPolicy": False}
            )
            public_policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": "*",
                        "Action": "s3:GetObject",
                        "Resource": f"arn:aws:s3:::{bucket_name}/*"
                    }
                ]
            }
            s3_client.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(public_policy))
            print(f"Bucket '{bucket_name}' created successfully with public access")

        else:
            print(f"Bucket '{bucket_name}' created successfully with private access")

        s3_client.put_bucket_tagging(
            Bucket=bucket_name,
            Tagging={
                'TagSet': [
                    {'Key': 'Created by', 'Value': 'CLI'},
                    {'Key': 'Owner', 'Value': 'netaaviv'}
                ]
            }
        )

    except Exception as e:
        print(f" Error creating bucket: {e}")

def upload_file_to_s3():
    """Uploads a file to an S3 bucket created by the CLI."""
    buckets = list_cli_buckets()
    
    if not buckets:
        print(" No CLI-created buckets found.")
        return
    
    print("\n Choose a bucket to upload to:")
    for i, bucket in enumerate(buckets):
        print(f"{i + 1}: {bucket}")

    try:
        bucket_choice = int(input("Enter the number of the bucket: ").strip()) - 1
        if bucket_choice < 0 or bucket_choice >= len(buckets):
            print(" Invalidnumber.")
            return
        bucket_name = buckets[bucket_choice]
    except ValueError:
        print(" Invalid input. Please enter a number.")
        return

    file_path = input("Enter the full path of the file to upload: ").strip()

    if not os.path.isfile(file_path):
        print(" Invalid file path.")
        return

    file_name = os.path.basename(file_path)

    try:
        s3_client.upload_file(file_path, bucket_name, file_name)
        print(f" File '{file_name}' successfully uploaded to '{bucket_name}'.")
    except Exception as e:
        print(f" Error uploading file: {e}")

def list_cli_buckets():
    try:
        response = s3_client.list_buckets()
        cli_buckets = []
        for bucket in response["Buckets"]:
            bucket_name = bucket["Name"]
            try:
                tags = s3_client.get_bucket_tagging(Bucket=bucket_name)["TagSet"]
                tag_dict = {tag["Key"]: tag["Value"] for tag in tags}
                if tag_dict.get("Created by") == "CLI" and tag_dict.get("Owner") == "netaaviv":
                    cli_buckets.append(bucket_name)
            except s3_client.exceptions.ClientError:
                continue  # Skip buckets without tags

        if cli_buckets:
            print("\nS3 Buckets created by the CLI:")
            for i, bucket in enumerate(cli_buckets):
                print(f"{i + 1}: {bucket}")

        else:
            print("No CLI-created buckets found.")

        return cli_buckets
    except Exception as e:
        print(f" Error listing buckets: {e}")
        return []
