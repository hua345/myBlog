# Jenkinsfile

可以在 `pipeline` 工程中打开`Pipeline Syntax`
在代码仓库创建`Jenkinsfile`文件

```bash
pipeline {
    agent any
    stages {
        stage('ready') {
              steps {
                    sh 'echo "ready to build"'
              }
        }
        stage('Build') {
              steps {
                    echo "Building"
                    sh '''mvn clean install'''
              }
        }
        stage('Test') {
              steps {
                   echo "Testing"
              }
        }
        stage('Deploy') {
              steps {
                   echo "Deploying"'
                   archiveArtifacts artifacts: '**/target/*. jar', fingerprint: true, onlyIfSuccessful: true
                   sh '''cp ${WORKSPACE}/${buildPath}/target/*. jar ${uploadPath}
              }
        }
        stage('Clean') {
              steps {
                   echo "Cleaning"
              }
        }
    }
    post {
        succese {
            echo 'success build!'
            sh '''for((i=1;i<=`expr ${BUILD_NUMBER} - 5`;i++));
            do
            archivePath="${JENKINS_HOME}/jobs/${JOB_NAME}/builds/$i/archive/"
            if [ -d $archivePath ]; then
            echo "$archivePath文件夹已经存在"
            rm -rf $archivePath
            fi
            done'''
        }
    }
}
```

`sh`命令多行时需要三个单引号`'`

### 常用`Step`

`echo`, 打印消息。`echo 'hello'`
`build`, 构建其他`jenkins job`。`build 'api-job'`
`sh`, 执行 linux 脚本。
`bat`, 执行 windows 脚本。
`archiveArtifacts artifacts`, 归档打包好的文件`archiveArtifacts artifacts: '**/target/*. jar'`
`fileExists`, 判断文件是否存在。`fileExists 'mypath'`
`dir`, 改变构建文件夹。

```bash
dir (mypath) {
      sh '''mvn clean install'''
}
```

### 常用的环境变量

```bash
${WORKSPACE} #构建工作区
${GIT_COMMIT} #git代码构建时commit SHA1值
${JOB_NAME} #构建…工程名称
```
