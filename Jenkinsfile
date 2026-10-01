pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Java failure demo') {
            steps {
                // Writes a tiny Java program that throws an exception, compiles it and runs it.
                // The exception makes java exit with code 1, so this stage (and the build) fails.
                sh '''
                    cat > FailDemo.java <<'EOF'
public class FailDemo {
    public static void main(String[] args) {
        System.out.println("Starting Java step...");
        int[] sizes = {1000, 1200, 1500};
        System.out.println("Reading size: " + sizes[5]);   // index 5 does not exist
    }
}
EOF
                    javac FailDemo.java
                    java FailDemo
                '''
            }
        }

        stage('Install dependencies') {
            // Skipped automatically because the stage before it failed.
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }
    }

    post {
        failure {
            echo "BUILD FAILED: the Java step threw an exception. See the stack trace in the 'Java failure demo' stage log."
        }
        success {
            echo 'Build succeeded.'
        }
        always {
            sh 'rm -f FailDemo.java FailDemo.class'
        }
    }
}
