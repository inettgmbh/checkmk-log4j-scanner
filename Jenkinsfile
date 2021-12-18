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
    def t_di_1
    def t_di_2
    stage('Checkout') {
        checkout scm
    }

    try {
        stage('build log4j-scanner') {
            t_di_1 = docker.build(
                "log4j-scanner-build:${env.BRANCH_NAME}-${env.BUILD_ID}",
                "--build-arg USER_ID=\$(id -u) --build-arg GROUP_ID=\$(id -g) " +
                "log4j-scanner"
            )
            docker.image(t_di_1.id).inside {
                dir('log4j-scanner') {
                    sh "mvn clean package"
                }
                dir('log4j-scanner/target') {
                    archiveArtifacts artifacts: '*.jar', fingerprint: true
                    archiveArtifacts artifacts: 'log4j_scanner', fingerprint: true
                    stash includes: 'log4j_scanner', name: 'log4j_scanner'
                }
            }
        }

        stage('package mkp') {
            t_di_2 = docker.build(
                "log4j-scanner-build-mkp:${env.BRANCH_NAME}-${env.BUILD_ID}",
                "--build-arg USER_ID=\$(id -u) --build-arg GROUP_ID=\$(id -g) " +
                "--build-arg PYTHON_MKP_REPO=${PYTHON_MKP_REPO} " +
                "mkp"
            )
            docker.image(t_di_2.id).inside {
                dir('mkp') {
                    sh 'chmod +x build/mkp-pack build/update-version'
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

                    sh 'mkdir -pv agents/plugins'
                    dir('agents/plugins') {
                        unstash 'log4j_scanner'
                    }

                    def releaseVersion

                    if (thisCommitTag != null && thisCommitTag != "") {
                        releaseVersion = thisCommitTag
                    } else {
                        releaseVersion = env.BRANCH_NAME+"-"+env.BUILD_ID
                    }

                    sh "build/update-version ${releaseVersion}"
                    sh 'build/mkp-pack'
                    archiveArtifacts artifacts: '*.mkp', fingerprint: true
                }
            }
        }
    } finally {
        stage('Cleanup') {
            cleanWs()
            if(t_di_1 && t_di_1.id) {
                sh "docker rmi ${t_di_1.id}"
            }
            if(t_di_2 && t_di_2.id) {
                sh "docker rmi ${t_di_2.id}"
            }
        }
    }
}