node {
    stage("Do Builds"){
        lin = build (job: "linux_isisdeps_build", propogate: false).result
        osx = build (job: "osx_isisdeps_build").result
        if(lin == 'FAILURE' || osx == 'FAILURE') {
            currentBuild.result = 'FAILURE' // of FAILURE
        }
    }
}