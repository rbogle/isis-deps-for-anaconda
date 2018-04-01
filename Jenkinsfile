pipeline {
    agent none
    stages{
        stage("Branch OS specific Builds"){
            parallel {
                stage("Linux"){
                    build './linux_isisdeps_build'
                }
                stage("OS X") {
                    build "./osx_isisdeps_build"
                }
            }
        }
    }
}