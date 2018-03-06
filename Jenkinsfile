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
                    sh "./bin/build_package.py -y -u usgs-astrogeology -t $CLOUD_TOKEN naif"
                }
            }
        }
        stage('build Mac'){
            agent{
                label 'darwin'
            }
            steps{
                withCredentials([string(credentialsId: 'AnacondaCloud', variable: 'CLOUD_TOKEN')]) {
                    sh "./bin/build_package.py -y -u usgs-astrogeology -t $CLOUD_TOKEN naif"
                }
            }
        }
    }
}