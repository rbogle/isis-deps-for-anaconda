pipeline {
    agent none
    stages {
        stage("Do Builds"){
            parallel{
                stage('build Linux') {
                    agent {
                        docker { 
                            image 'astro-bin.wr.usgs.gov/docker/usgsastro/condabuild:1.4'
                            label 'docker'
                        }
                    }
                    steps {
                        withCredentials([string(credentialsId: 'AnacondaCloud', variable: 'CLOUD_TOKEN')]) {
                            sh "./bin/build_package.py -y -u usgs-astrogeology -t $CLOUD_TOKEN all"
                        }
                    }
                    post {
                        always{
                            emailext attachLog: true, body: '''Just and FYI.

Please see the attached build log for more info''', subject: 'Autobuild of conda packages on Linux for ISIS has completed', to: 'astro_devops@usgs.gov'

                        }
                    }
                }
/*                 stage('build OSX'){
                    agent{
                        label 'darwin'
                    }
                    steps{
                        withCredentials([string(credentialsId: 'AnacondaCloud', variable: 'CLOUD_TOKEN')]) {
                            sh "source /opt/miniconda/bin/activate"
                            sh "./bin/build_package.py -y -u usgs-astrogeology -t $CLOUD_TOKEN all"
                        }
                    }
                    post {
                        always{
                            emailext attachLog: true, body: '''Just and FYI.

Please see the attached build log for more info''', subject: 'Autobuild of conda packages on OSX for ISIS has completed', to: 'astro_devops@usgs.gov'

                        }
                    }
                } */
            }
        }
    }
}
