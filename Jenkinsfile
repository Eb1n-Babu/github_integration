pipeline {
    agent any

    stages {
        stage('Clone Repo') {
            steps {
                git url: 'https://github.com/Eb1n-Babu/github_integration.git', branch: 'main'
            }
        }
        stage('Run Unit Tests') {
            steps {
                bat 'python manage.py test'
            }
        }
    }
}