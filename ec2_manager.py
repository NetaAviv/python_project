import boto3
ec2_client = boto3.client("ec2")

def get_latest_ami(os_type):
    """Fetch the latest Ubuntu or Amazon Linux AMI."""
    if os_type == "ubuntu":
        filters = [
            {"Name": "name", "Values": ["ubuntu/images/hvm-ssd/ubuntu-*"]},
            {"Name": "state", "Values": ["available"]},
            {"Name": "architecture", "Values": ["x86_64"]},
            {"Name": "root-device-type", "Values": ["ebs"]}
        ]
        owner = "099720109477"  # Canonical (Ubuntu)

    elif os_type == "amazon-linux":
        filters = [
            {"Name": "name", "Values": ["amzn2-ami-hvm-*"]},
            {"Name": "state", "Values": ["available"]},
            {"Name": "architecture", "Values": ["x86_64"]},
            {"Name": "root-device-type", "Values": ["ebs"]}
        ]
        owner = "137112412989"  # Amazon Linux owner ID

    else:
        raise ValueError("Invalid OS type. Choose 'ubuntu' or 'amazon-linux'.")

    try:
        response = ec2_client.describe_images(Owners=[owner], Filters=filters)

        if not response["Images"]:
            print("No AMIs found. Check your AWS region and filters.")
            return None

        # Sort by creation date (latest first)
        images = sorted(response["Images"], key=lambda x: x["CreationDate"], reverse=True)
        latest_ami = images[0]["ImageId"]  # Take the first image (latest)
        
        print(f"Latest AMI for {os_type}: {latest_ami}")
        return latest_ami

    except Exception as e:
        print("Error fetching AMI:", e)
        return None
