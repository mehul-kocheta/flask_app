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
                        sh 'latest_tag=$(curl -s "https://registry.hub.docker.com/v2/repositories/mehuljain4751/flask_server/tags/?page_size=5" | jq -r \'.results[].name\' | head -n 1)'
                        sh """sed -i 's|mehuljain4751/flask_server:.*|mehuljain4751/flask_server:${latest_tag}|' flask.yaml"""
                        sh 'kubectl apply -f flask.yaml'
                        sh 'kubectl apply -f mysql.yaml' 
                    }
                }
            }
        }
    }
}
