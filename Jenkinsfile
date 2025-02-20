pipeline {
    agent any

    environment {
        AWS_CREDENTIALS = credentials('3efbf7cd-2994-4221-8ced-f72752fbc54a') // Use Jenkins AWS credential ID
        GITHUB_CREDENTIALS = credentials('8f562aa3-4064-4ab9-b185-0a628c7ff735') // Use Jenkins GitHub credential ID
        DOCKER_IMAGE = "skameshh/microservices"
	DOCKER_IMAGE_USER = "skameshh/microservices-user"
        ECS_CLUSTER = "microservices-cluster"
        ECS_SERVICE = "microservices-service"
        ECS_TASK = "microservices-task"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git credentialsId: 'github-credentials-id', url: 'https://github.com/skameshh/python-microservices.git', branch: 'main'
            }
        }

        stage('Build Docker Images') {
            steps {
                sh '''
                docker build -t $DOCKER_IMAGE-auth ./auth_service
                docker build -t $DOCKER_IMAGE-user ./user_service
                '''
            }
        }

        stage('Push Docker Images') {
            steps {
                sh '''
                echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
                docker push $DOCKER_IMAGE-auth
                docker push $DOCKER_IMAGE-user
                '''
            }
        }

        stage('Deploy to AWS EC2') {
            steps {
                sshagent(['on_my_mac']) {
                    sh '''
                    ssh -o StrictHostKeyChecking=no ubuntu@3.215.100.139 '
                    docker pull $DOCKER_IMAGE-auth
                    docker pull $DOCKER_IMAGE-user
                    docker-compose up -d
                    '
                    '''
                }
            }
        }


	stage('Update ECS Service') {
            steps {
                sh '''
                aws ecs update-service --cluster $ECS_CLUSTER --service $ECS_SERVICE --force-new-deployment --region us-east-1
                '''
            }
        }


    }
}
