📌 Prerequisites
Before running the project, ensure your AWS EC2 instance (Amazon Linux) is properly configured:

1️⃣ Install Required Packages
sh
Copy
Edit
sudo yum install -y python3 pip git
pip install boto3
2️⃣ Configure AWS CLI
Make sure your AWS CLI is set up with the correct credentials:

sh
Copy
Edit
aws configure
3️⃣ Clone the Repository
sh
Copy
Edit
git clone https://github.com/your-username/your-repo.git
cd your-repo
4️⃣ Set Up Python Environment
sh
Copy
Edit
python3 -m venv venv
source venv/bin/activate
5️⃣ Edit Configuration
Before running, update the configuration file with:

VPC ID
Subnet ID
Key Pair Name
▶️ Running the Project
Once everything is set up, start the program:

sh
Copy
Edit
python main.py
This will guide you through the process step by step.

