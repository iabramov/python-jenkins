node {
    def app

    stage('Clone repository') {
        checkout scm
    }

    stage('Build image') {
        app = docker.build("iabramov/python-test", "-f ./server/Dockerfile ./server")
    }

    stage('Test image') {
        // app.inside {
        //     sh 'pytest -q'
        // }

        def reportsAbsPath = "${env.WORKSPACE}/tests"
        sh "echo ${reportsAbsPath}"
        sh "echo ${env.WORKSPACE}"

        // it maps host file system to a "nested" docker container because it is not nested at all, using the same socket
        sh 'docker run  -v /root/jenkins_home/tests:/tests iabramov/python-test pytest --junitxml=/tests/report.xml'
        sh 'ls -la /var/jenkins_home/tests'
        // app.withRun('-e "MYSQL_ROOT_PASSWORD=my-secret-pw" -p 3306:3306') { c ->
        //     /* Wait until mysql service is up */
        //     sh 'pytest --junitxml=/var/jenkins_home/tests/report.xml'
        // }
    }

    // stage('Push image') {
    //     docker.withRegistry('https://registry.hub.docker.com', 'e6416be2-1865-42df-bae1-4172dd398822') {
    //         app.push("${env.BUILD_NUMBER}")
    //         app.push("latest")
    //     }
    // }

    stage('Publish test result') {
        sh 'ls -la /var/jenkins_home/tests'
        junit '/var/jenkins_home/tests/*.xml'
    }

    // stage('Deploy') {
    //     sh 'docker container stop python-test && docker container rm python-test'
    //     sh 'docker run -d -p 8081:8080 --name python-test iabramov/python-test'
    // }


}

