# `kubectl` Quick Reference

> Kubectl is the Kubernetes cli version of a swiss army knife, and can do many things.
>
> -- [Introduction to Kubectl](https://kubectl.docs.kubernetes.io/guides/introduction/kubectl/)

이 문서는 주로 사용되는 `kubectl` 명령어를 다룹니다.

> [!TIP]
> 명령어 `kubectl`을 사용할 때 `--help` 플래그를 이용하면 각 comand와 subcommand에 대한 help 메시지를
> 확인할 수 있습니다. Help 메시지는 용례까지 포함하고 있으므로, 빠르게 사용법을 알아보고 싶을 때 매우 유용합니다.
>
> ```bash
> kubectl --help           # `kubectl` 자체에 대한 help 메시지 출력
> kubectl create --help    # `create` command에 대한 help 메시지 출력
> kubectl create ns --help # `create ns` subcommand에 대한 help 메시지 출력
> ```

## 목차

- [리소스 생성하기](#리소스-생성하기)
- [리소스 및 로그 조회하기](#리소스-및-로그-조회하기)
  - [리소스 조회하기](#리소스-조회하기)
  - [로그 조회하기](#로그-조회하기)
- [리소스 수정하기](#리소스-수정하기)
- [리소스 삭제하기](#리소스-삭제하기)
- [컨테이너에서 명령어 실행하기](#컨테이너에서-명령어-실행하기)
- [더 알아보기](#더-알아보기)

## 리소스 생성하기

```bash
##### Imperative Ways #####
###########################
# `my-ns` Namespace 생성
kubectl create ns my-ns
# 현재 Namespace(기본값: `default`)에 `my-deployment` Deployment 생성
kubectl create deployment my-deployment --image=nginx
# `my-ns` Namespace에 `my-deployment` Deployment 생성
kubectl create -n my-ns deployment my-deployment --image=nginx
###########################

##### Declarative Ways #####
############################
# `my-ns` Namespace 생성
cat <<EOF > ./my-ns.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: my-ns
EOF
kubectl apply -f ./my-ns.yaml

# `my-ns` Namespace에 `my-deployment` Deployment 생성
cat <<EOF > ./my-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-deployment
  namespace: my-ns
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
        - name: my-nginx
          image: nginx:latest
EOF
kubectl apply -f ./my-deployment.yaml
############################
```

## 리소스 및 로그 조회하기

### 리소스 조회하기

```bash
kubectl get nodes -o wide # PKS에서 관리 중인 Node 목록 확인

kubectl get -A pods # 모든 Namespace의 Pod 조회
kubectl get pods # 현재 Namespace(기본값: `default`)의 Pod 조회
kubectl get -n my-ns pods # `my-ns` Namespace의 Pod 조회

kubectl get -A all # 모든 Namespace의 Workload 및 Service 조회
kubectl get all # 현재 Namespace(기본값: `default`)의 Workload 및 Service 조회
kubectl get -n my-ns all # `my-ns` Namespace의 Workload 및 Service 조회

# `poolc-n1` Node의 자세한 정보 조회
kubectl describe node poolc-n1
# `ingress-nginx` Namespace에서 `ingress-nginx` Deployment의 자세한 정보 조회
kubectl describe -n ingress-nginx deployment ingress-nginx
# `argocd` Namespace에서 `argocd-application-controller-0` Pod의 자세한 정보 조회
kubectl describe -n argocd pod argocd-application-controller-0
```

#### 참조

- Nodes: <https://kubernetes.io/docs/concepts/architecture/nodes/>
- Workloads: <https://kubernetes.io/docs/concepts/workloads/>
- Service: <https://kubernetes.io/docs/concepts/services-networking/service/>

### 로그 조회하기

```bash
# `my-deployment-658d4cf5d8-qlwxn` Pod 내 (유일한) 컨테이너의 로그 조회
kubectl logs -n my-ns my-deployment-658d4cf5d8-qlwxn
# `my-deployment-658d4cf5d8-qlwxn` Pod 내 `my-nginx` 컨테이너의 로그 조회
kubectl logs -n my-ns my-deployment-658d4cf5d8-qlwxn -c my-nginx
# `my-ns` Namespace에서 `my-deployment` Deployment에 속한 모든 Pod의 로그 조회
kubectl logs -n my-ns deployment/my-deployment --all-pods=true
```

## 리소스 수정하기

```bash
# 에디터에서 `my-ns` Namespace manifest 수정
kubectl edit ns/my-ns
# 에디터에서 `my-ns` Namespace의 `my-deployment` Deployment manifest 수정
kubeclt edit -n my-ns deployment/my-deployment

# 수정된 `my-ns.yaml` manifest 파일의 내용을 반영
kubectl apply -f ./my-ns.yaml
# 수정된 `my-deployment.yaml` manifest 파일의 내용을 반영
kubectl apply -f ./my-deployment.yaml
```

### 참조

- Manifests: <https://kubernetes.io/docs/concepts/overview/working-with-objects/#describing-a-kubernetes-object>

## 리소스 삭제하기

```bash
##### Imperative Ways #####
###########################
# `my-ns` Namespace 삭제
kubectl delete ns my-ns
# `my-ns` Namespace에서 `my-deployment` Deployment 삭제
kubectl delete -n my-ns deployment my-deployment
###########################

##### Declarative Ways #####
############################
# `my-ns.yaml`, `my-deployment.yaml` 파일의 `.metadata.name`에 대응되는 리소스 삭제
kubectl delete ./my-ns.yaml ./my-deployment.yaml
############################
```

## 컨테이너에서 명령어 실행하기

```bash
# `my-ns` Namespace에서 `my-deployment-658d4cf5d8-qlwxn` Pod의 첫 번째 컨테이너에서
# `ls /` 명령어 실행
kubectl exec -n my-ns my-deployment-658d4cf5d8-qlwxn -- ls /
# `my-ns` Namespace에서 `my-deployment-658d4cf5d8-qlwxn` Pod의 `my-nginx`
# 컨테이너에서 `ls /` 명령어 실행
kubectl exec -n my-ns my-deployment-658d4cf5d8-qlwxn -c my-nginx -- ls /

# `my-ns` Namespace에서 `my-deployment-658d4cf5d8-qlwxn` Pod의 첫 번째 컨테이너에서
# `sh` 명령어 실행 (이때 로컬 클라이언트의 stdin은 컨테이너에서 실행된 `sh`로, `sh`의
# stdout/stderr는 로컬 클라이언트로 연결되므로, 사용자는 해당 쉘과 상호작용 가능)
kubectl exec -n my-ns my-deployment-658d4cf5d8-qlwxn -it -- sh
```

## 더 알아보기

- [리소스 생성](https://kubernetes.io/docs/reference/kubectl/quick-reference/#creating-objects)
- [리소스 조회](https://kubernetes.io/docs/reference/kubectl/quick-reference/#viewing-and-finding-resources)
- [리소스 업데이트](https://kubernetes.io/docs/reference/kubectl/quick-reference/#editing-resources)
- [리소스 삭제](https://kubernetes.io/docs/reference/kubectl/quick-reference/#deleting-resources)
- [컨테이너에서 명령어 실행하기](https://kubernetes.io/docs/reference/kubectl/quick-reference/#interacting-with-running-pods)
