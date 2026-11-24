pipeline {
    agent any

    environment {
        IMAGE_NAME   = 'assign3-site'
        STAGING_PORT = '8090'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'ls -l'
            }
        }

        stage('Package') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .'
            }
        }

        stage('Start Staging') {
            steps {
                sh '''
                    docker rm -f assign3-staging || true
                    docker run -d --name assign3-staging -p ${STAGING_PORT}:80 ${IMAGE_NAME}:${BUILD_NUMBER}
                    sleep 3
                    curl -sf http://localhost:${STAGING_PORT}/ > /dev/null
                '''
            }
        }

        stage('Test') {
            agent {
                dockerfile {
                    dir 'tests'
                    args '--network host'
                    reuseNode true
                }
            }
            environment {
                HOME     = '/tmp'
                BASE_URL = "http://localhost:${STAGING_PORT}"
            }
            steps {
                sh 'pytest tests/test_site.py -v --junitxml=test-results.xml'
            }
            post {
                always {
                    junit 'test-results.xml'
                    archiveArtifacts artifacts: 'screenshot.png', allowEmptyArchive: true
                }
            }
        }

        stage('Deploy') {
            steps {
                echo 'All Selenium tests passed. Deploying to production on port 80'
                sh '''
                    docker rm -f lab11-prod assign3-prod || true
                    docker run -d --name assign3-prod --restart unless-stopped -p 80:80 ${IMAGE_NAME}:${BUILD_NUMBER}
                '''
            }
        }
    }

    post {
        always {
            sh 'docker rm -f assign3-staging || true'
        }
        success {
            echo "Build ${BUILD_NUMBER} deployed successfully"
        }
        failure {
            echo "Build ${BUILD_NUMBER} failed. Live site remains unchanged."
        }
    }
}
