pipeline {
    agent { label 'movie-picker' }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
	    }
        }

        stage('Install dependencies') {
            steps {
                sh 'pip install -r requirements-dev.txt'
	    }
        }

        stage('Test') {
            steps {
                sh 'python -m pytest -v'
	    }
        }
    }
}
