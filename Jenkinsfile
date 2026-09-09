pipeline {
    agent { label 'movie-picker' }
	
    environment {
	TMDB_TOKEN = credentials('tmdb-token')
    }  
 
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
        
        stage('Deploy') {
            steps {
                withCredentials([
                    string(
                        credentialsId: 'ansible-vault-password',
                        variable: 'VAULT_PASSWORD'
                    )
                ]) {
                    sh '''
                        printf '%s' "$VAULT_PASSWORD" > .vault-pass
                        chmod 600 .vault-pass

                        ansible-playbook \
                            -i ansible/inventory.ini \
                            ansible/setup.yml \
                            --vault-password-file .vault-pass

                        rm -f .vault-pass
                    '''
                }
            }
        }
    }
}
