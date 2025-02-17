📌 Prerequisites
Before running the project, ensure your AWS EC2 instance (Amazon Linux) is properly configured:

1. Install Required Packages
sudo yum install -y python3 pip git
pip install boto3

2. Configure AWS CLI
Make sure your AWS CLI is set up with the correct credentials:
aws configure

3. Clone this Repository
git clone 
cd python_project

4. Set Up Python Environment
python3 -m venv venv
source venv/bin/activate

5. Edit Configuration
Before running, update the configuration file with:

VPC ID
Subnet ID
Key Pair Name

Running the Project
Once everything is set up, start the program:
python main.py
This will guide you through the process step by step.

