pipeline {
    agent {
        docker { 
            image 'usgsastro/condabuild:1.0'
            label 'docker'
        }
    }
    stages {
        stage('init') {
            withCredentials([string(credentialsId: 'AnacondaCloud', variable: 'CLOUD_TOKEN')]) {
                steps {
                    sh "touch test.ipnb"
                    sh 'anaconda -t $CLOUD_TOKEN upload -u usgs-astrogeology test.ipnb'
                }
            }
        }
        stage('build'){
            steps{
                sh 'ls -l'
            }
        }
    }
}