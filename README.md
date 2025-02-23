# Neta's Final Python Project

📌 Prerequisites

Before running the project, ensure your AWS EC2 instance (Amazon Linux) is properly configured:

1️⃣ Install Required Packages

 - sudo yum install -y python3 pip git
 - pip install boto3

2️⃣ Configure AWS CLI

Make sure your AWS CLI is set up with the correct credentials:

 - aws configure

3️⃣ Clone the Repository

 - git clone https://github.com/NetaAviv/python_project.git
 - cd python_project

4️⃣ Set Up Python Environment

 - python3 -m venv venv
 - source venv/bin/activate

5️⃣ Edit Configuration

Before running, update the configuration file with:

 - VPC ID

 - Subnet ID

 - Key Pair Name

 - S3 bucket name prefix

▶️ Running the Project

Once everything is set up, start the program:

python main.py

This will guide you through the process step by step.

