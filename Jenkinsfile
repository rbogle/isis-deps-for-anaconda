pipeline {
    agent none
    stages {
        stage('build Linux') {
             agent {
                docker { 
                    image 'astro-bin.wr.usgs.gov/docker/usgsastro/condabuild:1.3'
                    label 'docker'
                }
            }
            steps {
                withCredentials([string(credentialsId: 'AnacondaCloud', variable: 'CLOUD_TOKEN')]) {
                    sh "./bin/build_package.py -y -u usgs-astrogeology -t $CLOUD_TOKEN all"
                }
            }
        }
        stage('build Mac'){
            agent{
                label 'darwin'
            }
            steps{
                withCredentials([string(credentialsId: 'AnacondaCloud', variable: 'CLOUD_TOKEN')]) {
                    sh "source /opt/miniconda/bin/activate"
                    sh "./bin/build_package.py -y -u usgs-astrogeology -t $CLOUD_TOKEN all"
                }
            }
        }
    }
}
