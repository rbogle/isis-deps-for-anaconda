pipeline {
    agent {
        docker { 
            image 'usgsastro/conda-build'
            label 'docker'
        }
    }
    stages {
        stage('init') {
            steps {
                sh 'conda install -y jinja2 yaml'
                sh 'anaconda login -u'
            }
        }
        stage('build'){

        }
    }
}