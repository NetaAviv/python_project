# Neta's Final Python Project

## 📌 Prerequisites

Before running the project, ensure your AWS EC2 instance (Amazon Linux) is properly configured.

### 1️⃣ Install Required Packages
Run the following command to install the necessary packages:
```sh
sudo yum install -y python3 pip git
```

### 2️⃣ Configure AWS CLI
Ensure your AWS CLI is set up with the correct credentials:
```sh
aws configure
```

### 3️⃣ Clone the Repository
Clone the project repository and navigate into it:
```sh
git clone https://github.com/NetaAviv/python_project.git
cd python_project
```

### 4️⃣ Set Up Python Environment
Create and activate a virtual environment:
```sh
python3 -m venv venv
source venv/bin/activate
```

### 5️⃣ Install Dependencies
Install the required Python packages:
```sh
pip install boto3
```

### 6️⃣ Edit Configuration
Before running the project, update the configuration file with the following details:
- **VPC ID**
- **Subnet ID**
- **Key Pair Name**
- **S3 Bucket Name Prefix**

## ▶️ Running the Project
Once everything is set up, start the program by running:
```sh
python main.py
```
This will guide you through the process step by step.

