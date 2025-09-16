# Quick? Start

## 목차

- [실습 환경 구성](#0-실습-환경-구성)
  - [클러스터 접속 테스트](#클러스터-접속-테스트)
  - [모니터링 페이지 접속 테스트](#모니터링-페이지-접속-테스트)
- [네임스페이스 생성하기](#1-네임스페이스-생성하기)
- [파드 생성하기](#2-파드-생성하기)
- [로그 확인하기](#3-로그-확인하기)
  - [로그 생성하기](#로그-생성하기)
  - [Grafana 사용하기](#grafana-사용하기)
  - [Logs / App 대시보드](#logs--app-대시보드)
  - [Logs / Ingress-Nginx 대시보드](#logs--ingress-nginx-대시보드)
- [프로젝트 정리하기](#4-프로젝트-정리하기)
- [부록](#부록)


## 0. 실습 환경 구성

### 클러스터 접속 테스트
클러스터가 정상적으로 접속이 가능한 상태라면, 다음의 명령어가 오류 없이 실행되어야 합니다.
```console
$ kubectl get namespaces
NAME                 STATUS   AGE
argocd               Active   62d
cilium-secrets       Active   79d
default              Active   79d
ingress-nginx        Active   78d
kube-node-lease      Active   79d
kube-public          Active   79d
kube-system          Active   79d
kyverno              Active   13d
local-path-storage   Active   18d
monitoring           Active   74d
pks-argocd-demo      Active   11d
poolc-system         Active   13d
poolc-users          Active   33h
```

> [!WARNING]
> 위 명령어가 제대로 실행되지 않을 시, PKS와의 연결이 정상적이지 않은 상태입니다.
> 
> 사용자 가이드를 통해 연결을 진행 한 후에 실습 진행해주세요.

### 모니터링 페이지 접속 테스트
모니터링 페이지는 Grafana로 구성되어 있습니다.

다음의 페이지 접속을 통해 모니터링 페이지에 정상적으로 접속이 가능한지 확인해주세요!

[https://mon.dev.poolc.org](https://mon.dev.poolc.org)

> [!WARNING]
> 정상적으로 접속되지 않을 시 교내망에 정상적으로 연결되어 있지 않았을 가능성이 큽니다.
> 
> 교내 네트워크를 사용하거나 YSVPN을 사용하고있는지 확인해주세요

## 1. 네임스페이스 생성하기

먼저 실습에 사용할 네임스페이스를 생성해야 합니다.

``` console
apiVersion: v1
kind: Namespace
metadata:
  name: <원하는 네임스페이스 이름 지정>
```



## 2. 파드 생성하기

다음의 내용을 사용해서 deployment와 service를 띄워봅시다

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  namespace: <1번에서 사용한 네임스페이스 이름>
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: nginx:latest
          ports:
            - containerPort: 80
          command: ["/bin/sh", "-c"]
          args:
            - |
              echo '<html>
              <head><title>PKS Monitoring Demo</title></head>
              <body>
                <h1>안녕하세요! 모니터링 실습입니다.</h1>
              </body>
              </html>' > /usr/share/nginx/html/index.html && \
              nginx -g 'daemon off;'
---
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
  namespace: <1번에서 사용한 네임스페이스 이름>
spec:
  selector:
    app: nginx
  ports:
    - port: 80
      targetPort: 80
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: nginx-ingress
  namespace: <1번에서 사용한 네임스페이스 이름>
  annotations:
    kubernetes.io/ingress.class: "nginx"
spec:
  ingressClassName: nginx
  rules:
    - host: <본인이 원하는 url>.dev.poolc.org
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: nginx-service
                port:
                  number: 80
```

자 다음의 명령어를 실행해서 원하는 리소스가 잘 생성되었는지 확인해봅시다
```console
kubectl get all -n <1번에서 사용한 네임스페이스 이름>

NAME                                    READY   STATUS    RESTARTS   AGE
pod/nginx-deployment-698d9748f5-g64dx   1/1     Running   0          23m

NAME                    TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)   AGE
service/nginx-service   ClusterIP   10.105.107.233   <none>        80/TCP    23m

NAME                               READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/nginx-deployment   1/1     1            1           23m

NAME                                          DESIRED   CURRENT   READY   AGE
replicaset.apps/nginx-deployment-698d9748f5   1         1         1       23m
```

## 3. 로그 확인하기

### 로그 생성하기

로그를 확인하기 전 다음의 명령어를 통해 로그를 생성해주세요
```
curl <2번에서 생성한 url>.dev.poolc.org
```

또는 브라우저에서 해당 url로 접속해도 괜찮습니다

### Grafana 사용하기

다음의 링크를 통해 모니터링 페이지로 접속해주세요

[https://mon.dev.poolc.org](https://mon.dev.poolc.org)

좌측의 탭 중 Dashboards를 클릭해주세요

> [!NOTE]
> 풀씨 PKS의 모니터링페이지는 로그인 없이 대시보드를 확인할 수 있습니다.

<figure align="center">
    <img src="../../assets/user_main.webp" />

</figure>



수 많은 대시보드 중 저희가 사용할 대시보드는 **logs** 라는 태그를 가진 대시보드입니다.

Tag를 선택하여 logs 태그를 가진 대시보드만을 확인할 수 있게 필터링해주세요.

<figure align="center">
    <img src="../../assets/user_dashboard_filter.webp" />
</figure>

<figure align="center">
    <img src="../../assets/user_dashboard_logs.webp" />
</figure>

### Logs / App 대시보드
먼저, **"Logs / App"** 대시보드는 Pod에서 발생한 로그를 모니터링하는 대시보드입니다.

사용하는 방법은 다음과 같습니다.

<figure align="center">
    <img src="../../assets/user_dashboard_logs_app.webp" />
</figure>

1. 네임스페이스와 pod를 선택하여 로그를 확인할 파드를 특정할 수 있습니다.
> [!NOTE]
> 다른 namespace의 로그가 많을 경우 생성한 로그가 출력되지 않을 수 있습니다.
>
> 이러한 경우 namespace에 본인이 생성한 namespace를 직접 입력하여 선택할 수 있습니다.

2. 로그를 확인할 기간을 선택합니다.
3. 생성된 로그의 개수를 나타내는 화면입니다.
4. 시간별로 얼마나 로그가 발생했는지 확인하는 화면입니다.
5. 발생된 로그의 데이터가 출력됩니다.

### Logs / Ingress-Nginx 대시보드
다음으로, **"Logs / Ingress-Nginx"** 대시보드는 ingress-nginx를 통해서 접속한 로그를 모니터링하는 대시보드입니다.

사용하는 방법은 다음과 같습니다.

<figure align="center">
    <img src="../../assets/user_dashboard_logs_ingress.webp" />
</figure>

1. 네임스페이스와 pod를 선택하여 로그를 확인할 파드를 특정할 수 있습니다.
2. 로그를 확인할 기간을 선택합니다.
3. 생성된 로그의 개수를 나타내는 화면입니다.
4. 시간별로 얼마나 로그가 발생했는지 확인하는 화면입니다.
5. 발생된 로그의 데이터가 출력됩니다.

## 4. 프로젝트 정리하기

다음의 명령어를 통해 생성했던 자원을 한꺼번에 정리할 수 있습니다.
```
kubectl delete namespace <1번에서 사용한 네임스페이스 이름>
```

모든 리소스가 정리된 후 다음과 같은 명령어를 통해 네임스페이스가 삭제되었는지 확인하세요.
```console
$ kubectl get namespaces
NAME                 STATUS   AGE
argocd               Active   62d
cilium-secrets       Active   79d
default              Active   79d
ingress-nginx        Active   78d
kube-node-lease      Active   79d
kube-public          Active   79d
kube-system          Active   79d
kyverno              Active   13d
local-path-storage   Active   18d
monitoring           Active   74d
pks-argocd-demo      Active   11d
poolc-system         Active   13d
poolc-users          Active   33h
```

## 부록
