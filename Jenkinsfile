pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Train model') {
            steps {
                sh '''
                    . venv/bin/activate
                    python train_model.py
                '''
            }
        }

        stage('Run app') {
            steps {
                // Stop the app from the previous build, then start the new one in the background.
                // JENKINS_NODE_COOKIE=dontKillMe keeps the app running after the build finishes.
                sh '''
                    . venv/bin/activate
                    if [ -f /tmp/sweden_app.pid ]; then kill $(cat /tmp/sweden_app.pid) || true; sleep 2; fi
                    JENKINS_NODE_COOKIE=dontKillMe nohup gunicorn --bind 0.0.0.0:5000 --pid /tmp/sweden_app.pid app:app > app.log 2>&1 &
                    sleep 5
                    curl -s http://localhost:5000/
                '''
            }
        }
    }
}
