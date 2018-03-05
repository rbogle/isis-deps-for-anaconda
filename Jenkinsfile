pipeline {
    agent {
        docker { 
            image 'usgsastro/condabuild:1.0'
            label 'docker'
        }
    }
    stages {
        stage('init') {
            steps {
                sh 'conda install -y jinja2 yaml'
                // sh 'anaconda login -u'
            }
        }
        stage('build'){
            steps{
                sh 'ls -l'
            }
        }
    }
}