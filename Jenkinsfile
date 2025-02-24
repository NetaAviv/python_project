pipeline {
    agent any

    environment {
        VENV_DIR = "venv"
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
                    python main.py
                '''
            }
        }
    }
}
