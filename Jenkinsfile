node {

    try {
        stage('Checkout'){
            echo 'Building..'
            checkout scm
            echo "Running ${env.BUILD_ID} on ${env.JENKINS_URL}"
            sh 'git log HEAD^..HEAD --pretty="%h %an - %s" > GIT_CHANGES'
            def lastChanges = readFile('GIT_CHANGES')
            sh 'echo Started'
        }

        // uncomment to enable test
        /*
        stage('Test'){
            echo 'Testing..'
            sh './scripts/run_test.sh'
        }
        */

        // uncomment to enable deploy
        /*
        stage('Deploy'){
            echo 'Deploying..'
            sh './scripts/update.sh'
        }
        */

        stage('Publish results'){
            echo 'Build successful'
        }
    }

    catch (err) {
        echo 'Build failed!'
        throw err
    }

}
