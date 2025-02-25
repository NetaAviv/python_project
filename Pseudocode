# Neta's Pseudocode for Platform Engineering Python Exercise: Automating AWS Resource Provisioning

## Overview
This CLI tool automates AWS resource provisioning and management. It consists of a `main.py` script that orchestrates three separate modules:

- **`ec2_manager.py`** – Manages EC2 instances.
- **`s3_manager.py`** – Handles S3 bucket operations.
- **`route53_manager.py`** – Manages Route53 DNS records.

### Additional Files:
- **`configuration`** – Stores VPC and Subnet ID for EC2 creation and the S3 bucket prefix.
- **`user-data`** – A bash script that installs Python and Git on an instance.

---
## EC2 Management

### 1. List EC2 Instances
- Prompt the user to choose which instances to display: 
  - Running
  - Stopped
  - Recently Deleted
  - All
- Fetch and display the relevant EC2 instances.

### 2. Create EC2 Instance
- Check the number of running EC2 instances created by the CLI (**limit: 2**).
- Allow the user to select an instance type (**t3.nano** or **t4g.nano**).
- Allow the user to choose an OS (**Ubuntu** or **Amazon Linux**).
- Fetch the latest AMI ID corresponding to the selected OS.
- Prompt the user to enter a custom instance name.
- Ask the user if they want to include User Data to install Git and Python upon instance creation.
- Launch the instance with the following tags:
  ```plaintext
  CreatedBy=CLI
  Owner=NetaAviv
  ```
- Display instance details (**ID, name, state, public IP**).

### 3. Start a Stopped EC2 Instance
- Ensure there are **fewer than 2 running instances** before allowing the action.
- List all stopped instances created by the CLI.
- Prompt the user to select an instance to start.
- Start the selected instance.

### 4. Stop a Running EC2 Instance
- List all running instances created by the CLI.
- Prompt the user to select an instance to stop.
- Stop the selected instance.

### 5. Return to Main Menu
- Provide an option to return to the main menu.

---
## S3 Bucket Management

### 1. Create an S3 Bucket
- Prompt the user to enter a bucket name (**prefix added from configuration file**).
- Ensure the bucket name is unique.
- Allow the user to choose between **public** or **private** access.
- If **public** access is selected, require confirmation.
- Create the bucket with proper settings and CLI-generated tags.
- Display the bucket details.

### 2. Upload a File to an S3 Bucket
- List all buckets created by the CLI.
- Prompt the user to select a bucket.
- Ask for the file path to upload.
- Upload the file to the selected bucket.

### 3. List S3 Buckets
- Display a list of all buckets created by the CLI.

### 4. Return to Main Menu
- Provide an option to return to the main menu.

---
## Route53 DNS Management

### 1. Create a Hosted Zone
- Prompt the user to enter a domain name.
- Validate the domain name format.
- Create the hosted zone with appropriate CLI-generated tags.
- Display zone details (**Zone ID, Name Servers**).

### 2. Manage DNS Records
- List all hosted zones created by the CLI.
- Prompt the user to choose a hosted zone to manage records.
- Provide options to **Create, Update, or Delete** a DNS record.

#### a. Create a Record
- Prompt the user to enter a record name.
- Allow selection of a record type (**A, AAAA, CNAME, TXT**).
- Display an example of the expected format for the chosen record type.
- Validate user input against the expected format.
- Create the record and display confirmation.

#### b. Update a Record
- List all existing **editable** records in the selected hosted zone (**NS and SOA records cannot be modified**).
- Prompt the user to select a record to update.
- Ask the user for a new value, ensuring it matches the required format.
- Update the record and display the modified entry.

#### c. Delete a Record
- List all existing **deletable** records in the selected hosted zone (**NS and SOA records cannot be deleted**).
- Prompt the user to select a record to delete.
- Delete the record and confirm the action.

### 3. List Hosted Zones
- Display a list of hosted zones created by the CLI.
- Allow the user to view all records in a selected zone.
- Provide an option to return to the Route53 main menu.

### 4. Return to Main Menu
- Provide an option to return to the main menu.
