pipeline {
    agent any
    stages {
        stage('Creating a VM in Azure') {
            steps {
                script{
                    sh '''
                    #!/bin/bash
                    python3 automationvm.py
     
                    ''' 
                }
            }
        }
    }
}
