## dockerFile

```bash
ENV="FAT"
JOB_NAME="test"

JOB_PATH=/home/$JOB_NAME
cd $JOB_PATH

cat << EOF > Dockerfile
FROM test/skywalking-agent
COPY ${JOB_NAME}.jar app.jar
ENTRYPOINT java -javaagent:/agent/skywalking-agent.jar -jar app.jar -Xmx1G -Xms1G -XX:+UseG1GC -XX:MaxGCPauseMillis=20 --spring.profiles.active=$ENV -XX:+HeapDumpOnOutOfMemoryError
EOF

echo  docker build $JOB_NAME
docker build -t   test/$JOB_NAME:$BUILD_ID .
docker push test/$JOB_NAME:$BUILD_ID

if [ $? -eq 0 ]; then
   :
else
    echo '************上传镜像失败************'
    exit 1
fi;

docker rmi  test/$JOB_NAME:$BUILD_ID
```

## k8s

```bash
Port="8080"
Status="Deploy"
RollbackId=""
BUILD_ID="295"
JOB_NAME="test"
Replicas="1"

if [ $Status == Deploy ];
then
  TAG=$BUILD_ID;
else
    TAG=$RollbackId; 
fi
echo $TAG


cd /k8syaml

cat <<EOF> deployment-${JOB_NAME}.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${JOB_NAME}
  labels:
    app: ${JOB_NAME}
spec:
  replicas: ${Replicas}
  selector:
    matchLabels:
      app: ${JOB_NAME}
  template:         
    metadata:
      labels:
        app: ${JOB_NAME}
    spec:
      terminationGracePeriodSeconds: 65
      dnsPolicy: ClusterFirstWithHostNet

      nodeSelector:
        kubernetes.io/hostname: test

      containers:                                                                 
      - name: ${JOB_NAME}
        image: test/${JOB_NAME}:$TAG
        imagePullPolicy: IfNotPresent
        env:
        - name: SW_AGENT_COLLECTOR_BACKEND_SERVICES
          value: 127.0.0.1:11800
        - name: SW_AGENT_NAME
          value: $JOB_NAME
        envFrom:
        - secretRef:
            name: eureka-account

        #resources:
          #limits:
            #memory: 5G

        volumeMounts:
        - mountPath: /logs
          name: log-volume

        startupProbe:
          httpGet:
            path: /
            port: ${Port}
          failureThreshold: 60
          periodSeconds: 5

        livenessProbe:
          httpGet:
            path: /
            port: ${Port}
          initialDelaySeconds: 1
          failureThreshold: 5
          periodSeconds: 1

        readinessProbe:
          httpGet:
            path: /
            port: ${Port}
          initialDelaySeconds: 1
          periodSeconds: 1

        lifecycle:
          postStart:
            exec:
              command: ["/bin/sh", "-c", "curl -X PUT http://\$(echo \${USER_NAME}|sed s/[[:space:]]//g):\$(echo \${PASSWORD}|sed s/[[:space:]]//g)@fat-eureka-server:8761/eureka/apps/${JOB_NAME}/\$(hostname -i):${JOB_NAME}:${Port}/status?value=UP"]
          preStop:
            exec:
              command: ["/bin/sh","-c","curl -X PUT http://\$(echo \${USER_NAME}|sed s/[[:space:]]//g):\$(echo \${PASSWORD}|sed s/[[:space:]]//g)@fat-eureka-server:8761/eureka/apps/${JOB_NAME}/\$(hostname -i):${JOB_NAME}:${Port}/status?value=OUT_OF_SERVICE"]

      volumes:
      - name: log-volume
        hostPath:
          path: /home/logs/${JOB_NAME}
          type: DirectoryOrCreate

      imagePullSecrets:
      - name: registry
EOF

kubectl  apply -f deployment-${JOB_NAME}.yaml
kubectl  get deployments.apps ${JOB_NAME} -o jsonpath={".status.conditions[1].reason"}

while :
do
  Status=$(kubectl  get deployments.apps ${JOB_NAME} -o jsonpath={".status.conditions[1].reason"})
  if [ $Status = NewReplicaSetAvailable ]
  then
    echo -e "服务已启动"
    break
  else
    echo $Status
    sleep 3s
  fi
done

kubectl  get deployments.apps
```
