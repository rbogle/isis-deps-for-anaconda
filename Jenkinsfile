node {
    stage("Branch OS specific Builds"){
        parallel{
            lin = build (job: "./linux_isisdeps_build", propagate: false).result
            osx = build (job: "./osx_isisdeps_build", propagate: false).result
            if(lin == 'FAILURE' || osx == 'FAILURE') {
                currentBuild.result = 'FAILURE' // of FAILURE
            }
        }
    }
}