pipeline {
    agent none

    environment {
        DOCKERHUB_CREDENTIALS = credentials('docker_cred')
        DOCKERHUB_REPO = 'mehuljain4751/flask_server'
    }

    stages {
        stage('Build Docker Image and push') {
            agent {
                label 'amz-ec2'
            }
            steps {
                script {
                    git 'https://github.com/mehul-kocheta/flask_app.git'
                    dockerImage = docker.build("${env.DOCKERHUB_REPO}:${env.BUILD_NUMBER}")
                    docker.withRegistry('https://index.docker.io/v1/', 'docker_cred') {
                        dockerImage.push()
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            agent {
                label 'k8_node'
            }
            steps {
                script {
                    withCredentials([file(credentialsId: 'k8_cred', variable: 'KUBECONFIG')]) { 
                        git 'https://github.com/mehul-kocheta/flask_app.git'
                        sh ''' # Replace the image tag in the YAML file with the build number
                               sed -i 's|mehuljain4751/flask_server:[0-9]*|mehuljain4751/flask_server:${BUILD_NUMBER}|g' flask.yaml 
                               kubectl apply -f flask.yaml'''
                        sh 'kubectl apply -f mysql.yaml'
                        sh 'kubectl apply -f flask.yaml' 
                    }
                }
            }
        }
    }
}
