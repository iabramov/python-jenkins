node {
    def app

    stage('Clone repository') {
        checkout scm
    }

    stage('Build image') {
        // app = docker.build("iabramov/python-test")
        app = docker.build("iabramov/python-test", "-f ./server/Dockerfile ./server")
    }

    stage('Test image') {
        // app.inside {
        //     sh 'pytest -q'
        // }

        // it maps host file system to a "nested" docker container because it is not nested at all, use the same socket
        sh 'docker run -v /root/jenkins_home/tests:/tests/report.xml pytest --junitxml=/tests/report.xml'

        // app.withRun('-e "MYSQL_ROOT_PASSWORD=my-secret-pw" -p 3306:3306') { c ->
        //     /* Wait until mysql service is up */
        //     sh 'pytest --junitxml=/var/jenkins_home/tests/report.xml'
        // }
    }

    stage('Push image') {
        docker.withRegistry('https://registry.hub.docker.com', 'e6416be2-1865-42df-bae1-4172dd398822') {
            app.push("${env.BUILD_NUMBER}")
            app.push("latest")
        }
    }

    post {
      always {
        junit '/var/jenkins_home/tests/report.xml'
        // junit '**/reports/junit/*.xml'
      }
   } 
}

