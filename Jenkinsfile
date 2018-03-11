pipeline {
    agent none
    stages {
        stage("Do Builds"){
            parallel{
                stage('Linux') {
                    agent {
                        docker { 
                            image 'astro-bin.wr.usgs.gov/docker/usgsastro/condabuild:1.7'
                            label 'docker'
                        }
                    }
                    stage("scm checkout"){
                        steps{
                            git credentialsId: 'jenkins-ssh', url: 'git@astrogit.wr.usgs.gov:rbogle/isis-deps-for-anaconda.git'
                            env.CONT = sh "./bin/git_changes.py -r recipies -r conda_build_config.yaml || return"
                        }
                    }
                    stage("Build Linux Packages"){
                        steps {
                            sh "./bin/build_package.py -y --hardfail --buildlog linux_${env.BUILD_ID}.log all"
                        }
                    }
                    stage("Upload Linux Packages"){
                        steps {
                            withCredentials([string(credentialsId: 'AnacondaCloud', variable: 'CLOUD_TOKEN')]) {
                                sh "./bin/dist_package.py -u usgs-astrogeology -t $CLOUD_TOKEN -l main -l isis --force -f ./logs/linux_${env.BUILD_ID}.log"
                            }
                        }
                    }
                }
                stage('OSX'){
                    agent{
                        label 'darwin'
                    }
                    stage("scm checkout"){
                        steps{
                            git credentialsId: 'jenkins-ssh', url: 'git@astrogit.wr.usgs.gov:rbogle/isis-deps-for-anaconda.git'
                        }
                    }                    
                    stage("Build OSX Packages"){
                        steps {
                            sh "./bin/build_package.py -y --hardfail --buildlog osx_${env.BUILD_ID}.log all"
                        }
                    }
                    stage("Upload OSX Packages"){
                        steps {
                            withCredentials([string(credentialsId: 'AnacondaCloud', variable: 'CLOUD_TOKEN')]) {
                                sh "./bin/dist_package.py -u usgs-astrogeology -t $CLOUD_TOKEN -l main -l isis --force -f ./logs/osx_${env.BUILD_ID}.log"
                            }
                        }
                    }
                }
            }
            post {
                always{
                    emailext attachLog: true, body: '''Just FYI.

Please see the attached build log for more info''', subject: 'The autobuild job of conda packages for ISIS has completed', to: 'astro_devops@usgs.gov'

                }
            }
        }
    }
}