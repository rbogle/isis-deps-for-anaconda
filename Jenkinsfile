pipeline {
    agent: none
    stages{
        stage("Branch OS specific Builds"){
            steps{
                parallel {
                    stage("Linux"){
                        build (job: "./linux_isisdeps_build")
                    }
                    stage("OS X") {
                        build (job: "./osx_isisdeps_build")
                    }
                }
            }
        }
    }
}