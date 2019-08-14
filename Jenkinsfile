// pipeline {
//     agent any
//     stages { 
//         stage('Example') {
//             steps {
//                 echo 'Hello World 2'
//             }
//         }
//     }
// }



node {
    def app

    stage('Clone repository') {
        /* Let's make sure we have the repository cloned to our workspace */

        checkout scm
    }

    stage('Build image') {
        /* This builds the actual image; synonymous to
         * docker build on the command line */

        // app = docker.build("iabramov/python-test")
        // app = docker.build("iabramov/python-test", "-f server/Dockerfile .")
        app = docker.build("iabramov/python-test", "-f ./server/Dockerfile ./server")
    }

    stage('Test image') {
        /* run a test framework against our image */
        app.inside {
            sh 'pytest -q'
        }
    }

    stage('Push image') {
        /* Finally, we'll push the image with two tags:
         * First, the incremental build number from Jenkins
         * Second, the 'latest' tag.
         * Pushing multiple tags is cheap, as all the layers are reused. */
        docker.withRegistry('https://registry.hub.docker.com', 'e6416be2-1865-42df-bae1-4172dd398822') {
            app.push("${env.BUILD_NUMBER}")
            app.push("latest")
        }
    }
}

