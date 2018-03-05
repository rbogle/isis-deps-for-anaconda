pipeline {
    agent {
        docker { 
            image 'usgsastro/condabuild:1.0'
            label 'docker'
        }
    }
    stages {
        stage('init') {
            
            steps {
                withCredentials([string(credentialsId: 'AnacondaCloud', variable: 'CLOUD_TOKEN')]) {
                    sh "touch test.ipnb"
                    sh 'anaconda -t $CLOUD_TOKEN upload -u usgs-astrogeology test.ipynb'
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