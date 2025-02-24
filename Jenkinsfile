pipeline {
    agent any
    
    environment {
        VIRTUAL_ENV = "${WORKSPACE}/venv"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/NetaAviv/python_project.git'
            }
        }

        stage('Setup Python Virtual Environment') {
            steps {
                sh 'python3 -m venv $VIRTUAL_ENV'
                sh 'source $VIRTUAL_ENV/bin/activate'
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run CLI Tool') {
            steps {
                sh 'source $VIRTUAL_ENV/bin/activate && python main.py'
            }
        }
    }
}
