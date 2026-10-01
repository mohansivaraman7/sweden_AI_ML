// Jenkinsfile for Jenkins running on WINDOWS (uses bat instead of sh).
pipeline {
    agent any

    environment {
        // If Jenkins can't find Python, put the full path here, e.g.
        // PYTHON = 'C:\\Users\\<you>\\AppData\\Local\\Programs\\Python\\Python311\\python.exe'
        PYTHON = 'python'
        PORT   = '5000'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install dependencies') {
            steps {
                bat '''
                    "%PYTHON%" --version
                    "%PYTHON%" -m venv venv
                    venv\\Scripts\\python.exe -m pip install --upgrade pip
                    venv\\Scripts\\python.exe -m pip install -r requirements.txt waitress
                '''
            }
        }

        stage('Train model') {
            steps {
                bat 'venv\\Scripts\\python.exe train_model.py'
            }
        }

        stage('Stop old app') {
            steps {
                // Kill whatever is listening on the port from the previous build (ok if nothing is).
                bat(returnStatus: true, script: '''
                    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :%PORT% ^| findstr LISTENING') do taskkill /F /PID %%a
                ''')
            }
        }

        stage('Run app') {
            steps {
                // JENKINS_NODE_COOKIE=dontKillMe keeps the app running after the build finishes.
                withEnv(['JENKINS_NODE_COOKIE=dontKillMe']) {
                    bat '''
                        start "sweden_app" /B venv\\Scripts\\waitress-serve.exe --listen=0.0.0.0:%PORT% app:app > app.log 2>&1
                        ping -n 8 127.0.0.1 > nul
                        curl.exe -s http://localhost:%PORT%/
                    '''
                }
            }
        }
    }

    post {
        failure {
            echo 'Build failed - if the app did not start, open app.log in the job workspace.'
        }
    }
}
