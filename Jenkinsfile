pipeline {
    agent none
    stages {
        stage('build Linux') {
             agent {
                docker { 
                    image 'usgsastro/condabuild:1.0'
                    label 'docker'
                }
            }
            steps {
                withCredentials([string(credentialsId: 'AnacondaCloud', variable: 'CLOUD_TOKEN')]) {
                    sh "touch test.ipynb"
                    sh 'anaconda -t $CLOUD_TOKEN upload -u usgs-astrogeology test.ipynb'
                }
            }
        }
        stage('build Mac'){
            agent{
                label 'mac'
            }
            steps{
                sh 'ls -l'
            }
        }
    }
}