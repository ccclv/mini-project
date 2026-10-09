pipeline {
  agent any

  environment {
    DOCKERHUB = credentials('dockerhub-creds')
    IMAGE = "${DOCKERHUB_USR}/tebak-angka"
    KUBECONFIG = '/var/jenkins_home/.kube/config'
  }

  stages {
    stage('Build image') {
      steps {
        sh 'docker build -t $IMAGE:$BUILD_NUMBER .'
      }
    }

    stage('Test') {
      steps {
        sh 'docker run --rm $IMAGE:$BUILD_NUMBER python -m pytest'
      }
    }

    stage('Push image') {
      steps {
        sh 'echo $DOCKERHUB_PSW | docker login -u $DOCKERHUB_USR --password-stdin'
        sh 'docker push $IMAGE:$BUILD_NUMBER'
      }
    }

    stage('Deploy') {
      steps {
        sh 'kubectl set image deployment/tebak-angka tebak-angka=$IMAGE:$BUILD_NUMBER'
        sh 'kubectl rollout status deployment/tebak-angka --timeout=120s'
      }
    }
  }

  post {
    always {
      sh 'docker logout || true'
    }
  }
}