# Neta's final python project
Before me can start, the project should run on ec2 aws linux and we need to configure the following:
- install python: sudo yum install python
- install pip: sudo yum install pip
- install boto3: pip install boto3
- configure aws cli
- install git (to copy this repo): sudo yum install git
- set the python enviorment:
  1. python -m venv venv
  2. source venv/bin/activate
- Edit the configuration file, place there the vpc, the subnet and the key pair you want the instances to be made with

To run the code, cd into the project and run the main.py file which will guide you through! 
Enter "python main.py" to start 
