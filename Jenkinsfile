pipeline {
    agent any

    environment {
        VENV_DIR = "venv"
        AWS_REGION = 'us-east-1'  // Replace with your actual region
        AWS_DEFAULT_REGION = 'us-east-1'  // Add this
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/NetaAviv/python_project.git'
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''
                    python3 -m venv $VENV_DIR
                    source $VENV_DIR/bin/activate
                    python3 -m pip install --upgrade pip
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    source $VENV_DIR/bin/activate
                    pip install boto3
                '''
            }
        }

        stage('Run CLI Tool') {
            steps {
                sh '''
                    source $VENV_DIR/bin/activate
                    export AWS_REGION=$AWS_REGION  # Set region
                    python main.py
                '''
            }
        }
    }
}
