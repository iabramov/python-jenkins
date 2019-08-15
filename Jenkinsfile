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

        // host directory should be /root/jenkins_home
        def hostReportsAbsPath = reportsAbsPath.replace("/root/", "/var/")
        // it maps host file system to a "nested" docker container because it is not nested at all, using the same socket
        sh "docker run  -v ${hostReportsAbsPath}:/tests iabramov/python-test pytest -q --junitxml=/tests/report.xml"
    }

    stage('Push image') {
        docker.withRegistry('https://registry.hub.docker.com', 'e6416be2-1865-42df-bae1-4172dd398822') {
            app.push("${env.BUILD_NUMBER}")
            app.push("latest")
        }
    }

    stage('Publish test result') {
        sh "touch tests/*.xml"
        junit 'tests/*.xml'
    }

    stage('Deploy') {
        sh 'docker container stop python-test ; docker container rm python-test || true'
        sh "docker run -d -p 8081:8080 --name python-test iabramov/python-test:${env.BUILD_NUMBER}"
    }


}

