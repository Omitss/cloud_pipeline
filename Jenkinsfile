pipeline {
    agent any

    environment {
        COMPOSE_DIR = 'jenkins'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Load .env from Credentials') {
            steps {
                withCredentials([file(credentialsId: 'project-env-file', variable: 'ENV_FILE')]) {
                    sh 'cp "$ENV_FILE" .env'
                }
            }
        }

        stage('Build & Deploy') {
            steps {
                dir("${COMPOSE_DIR}") {
                    sh 'docker compose down'
                    sh 'docker compose build --no-cache'
                    sh 'docker compose up -d'
                }
            }
        }

        stage('Cleanup') {
            steps {
                sh 'docker image prune -f'
            }
        }
    }

    post {
        always {
            sh 'rm -f .env'
        }
        failure {
            echo '배포 실패'
        }
    }
}