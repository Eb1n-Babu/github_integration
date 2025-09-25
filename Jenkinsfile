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
                bat 'C:\\Users\\ebinb\\AppData\\Local\\Programs\\Python\\Python313\\python.exe manage.py test'
            }
        }
    }
}