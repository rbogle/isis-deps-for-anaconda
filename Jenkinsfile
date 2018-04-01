pipeline {
    agent none
    stages{
        stage("Branch OS specific Builds"){
            parallel {
                stage("Linux"){
                    steps{
                        build './linux_isisdeps_build'
                    }
                }
                stage("OS X") {
                    steps{
                        build "./osx_isisdeps_build"
                    }
                }
            }
        }
    }
}