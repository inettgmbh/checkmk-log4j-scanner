properties([
    [$class: 'BuildDiscarderProperty',
     strategy: [
         $class: 'EnhancedOldBuildDiscarder',
         daysToKeepStr: '10', numToKeepStr: '10',
         discardOnlyOnSuccess: true, holdMaxBuilds: true
         ]
     ]
 ]);

node {
    def PYTHON_MKP_REPO = "git+https://github.com/inettgmbh/python-mkp.git@0.6"
    def DOCKER_BUILD_ARGS = "--build-arg USER_ID=\$(id -u) --build-arg GROUP_ID=\$(id -g)"
    def t_di_1
    def t_di_2

    def releaseVersion

    stage('Checkout') {
        checkout scm
        def lastTag = sh(
            returnStdout: true,
            script: "git tag --sort version:refname | tail -1"
        ).trim()
        def thisCommitTag = sh(
            returnStdout: true,
            script: "git tag --points-at HEAD"
        )
        if (thisCommitTag != null) {
            thisCommitTag = thisCommitTag.trim()
        }
        if (thisCommitTag != null && thisCommitTag != "") {
            releaseVersion = thisCommitTag
        } else {
            releaseVersion = env.BRANCH_NAME+"-"+env.BUILD_ID
        }
    }

    def parallel_list = []
    def parallel_dependencies = [:]

    parallel_dependencies.put("log4j2-scanner", {
        stage("Container log4j-scanner-build") {
            t_di_1 = docker.build(
                "log4j-scanner-build:${env.BRANCH_NAME}-${env.BUILD_ID}",
                "${DOCKER_BUILD_ARGS} log4j-scanner"
            )
        }
        stage("Build log4j2-scanne") {
            docker.image(t_di_1.id).inside {
                dir('log4j-scanner') {
                    sh "mvn clean package"
                }
            }
        }
        stage("Archive and stash artifacts") {
            dir('log4j-scanner/target') {
                archiveArtifacts artifacts: '*.jar', fingerprint: true
                archiveArtifacts artifacts: 'log4j_scanner', fingerprint: true
                stash includes: 'log4j_scanner', name: 'log4j_scanner'
            }
        }
        stage("Remove docker image log4j-scanner-build-scanner") {
            if(t_di_1 && t_di_1.id) {
                sh "docker rmi ${t_di_1.id}"
                t_di_1 = null
            }
        }
    } )
    parallel_dependencies.put("Container log4j-scanner-build-mkp", {
        stage("Build docker container") { t_di_2 = docker.build(
            "log4j-scanner-build-mkp:${env.BRANCH_NAME}-${env.BUILD_ID}",
            "${DOCKER_BUILD_ARGS} --build-arg PYTHON_MKP_REPO=${PYTHON_MKP_REPO} " +
            "mkp"
        ) }
        stage("Prepare Build") { dir('mkp') {
            sh 'chmod +x build/mkp-pack build/update-version'
            sh 'mkdir -pv agents/plugins'
        } }
    } )

    parallel_list.add(parallel_dependencies)


    try {
        for (parallels in parallel_list) {
            parallel(parallels)
        }

        stage('Unstash scanner') {
            dir('mkp/agents/plugins') {
                unstash 'log4j_scanner'
            }
        }
        stage('package mkp') {
            docker.image(t_di_2.id).inside {
                dir('mkp') {
                    sh "build/update-version ${releaseVersion}"
                    sh 'build/mkp-pack'
                }
            }
        }
        stage('Archive Artifacts') {
            dir('mkp') {
                archiveArtifacts artifacts: '*.mkp', fingerprint: true
            }
        }
        stage("Remove image log4j-scanner-build-mkp") {
            if(t_di_2 && t_di_2.id) {
                sh "docker rmi ${t_di_2.id}"
                t_di_2 = null
            }
        }
        stage("Cleanup") {
            cleanWs()
        }
    } finally {
        stage('Delete docker containers') {
            if(t_di_1 && t_di_1.id) {
                sh "docker rmi ${t_di_1.id}"
            }
            if(t_di_2 && t_di_2.id) {
                sh "docker rmi ${t_di_2.id}"
            }
        }
    }
}