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

    stage('build info') {
        sh "echo BRANCH_NAME=${env.BRANCH_NAME}"
    }

    try {
        stage('build log4j-scanner') {
            git url: 'https://github.com/inettgmbh/checkmk-log4j-scanner.git',
                branch: "${env.BRANCH_NAME}"
            def t_di = docker.build(
                "log4j-scanner-build:${env.BRANCH_NAME}-${env.BUILD_ID}",
                "--build-arg USER_ID=\$(id -u) --build-arg GROUP_ID=\$(id -g) " +
                "log4j-scanner"
            )
            docker.image(t_di.id).inside {
                git url: 'https://github.com/inettgmbh/checkmk-log4j-scanner.git',
                    branch: "${env.BRANCH_NAME}"
                dir('log4j-scanner') {
                    sh "mvn clean package"
                }
                dir('log4j-scanner/target') {
                    archiveArtifacts artifacts: '*.jar', fingerprint: true
                    archiveArtifacts artifacts: 'log4j-scanner', fingerprint: true
                    stash includes: 'log4j-scanner', 'log4j-scanner'
                }
            }
        }

        stage('package mkp') {
            def t_di = docker.build(
                "log4j-scanner-build:${env.BRANCH_NAME}-${env.BUILD_ID}",
                "--build-arg USER_ID=\$(id -u) --build-arg GROUP_ID=\$(id -g) " +
                "--build-arg PYTHON_MKP_REPO=${PYTHON_MKP_REPO} " +
                "mkp"
            )
            docker.image(t_di.id).inside {
                git url: 'https://github.com/inettgmbh/checkmk-log4j-scanner.git',
                    branch: "${env.BRANCH_NAME}"
                dir('mkp') {
                    sh 'chmod +x build/mkp-pack build/update-version'
                    def containsTag = sh(returnStdout: true, script: "git tag --sort version:refname | tail -1").trim()
                    def shortCommit = sh(returnStdout: true, script: "git log -n 1 --pretty=format:'%h'").trim()

                    sh 'mkdir -pv agents/plugins'
                    dir('agents/plugins') {
                        unstash 'log4j-scanner'
                    }

                    def releaseVersion
                    if (containsTag != "") {
                        releaseVersion = containsTag
                    } else {
                        releaseVersion = shortCommit
                    }
                    withEnv(["RELEASE_VERSION=${releaseVersion}"]) {
                        sh 'build/update-version ${RELEASE_VERSION}'
                    }
                    sh 'build/mkp-pack'
                    archiveArtifacts artifacts: '*.mkp', fingerprint: true
                }
            }
        }
    } finally {
        cleanWs()
    }
}