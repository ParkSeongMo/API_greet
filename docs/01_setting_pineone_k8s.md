# 파인원 k8s 개발기 연동 방법

[https://dev.pineone.com:20443/internal/wiki/Setting_k8s_summay.md](https://dev.pineone.com:20443/internal/wiki/Setting_k8s_summay.md)

# **kubectl 설정 - 파인원 k8s 개발기 연동 방법**

## **1. kubectl 설치 (macOS / Homebrew)**

### **Homebrew로 설치 (권장)**

```
brew update
brew installkubectl
```

## **2. kubelogin 설치 - 자동 oauth 인증 설정**

[https://github.com/int128/kubelogin](https://github.com/int128/kubelogin) 참고하여 kubelogin 설치

## **3. 파인원 개발 k8s 연동 설정**

파일명 : ~/.kube/config

```
apiVersion: v1
clusters:
- cluster:
    server: https://dev.pineone.com:20446
  name: pineone-dev-k8s
contexts:
- context:
    cluster: pineone-dev-k8s
    namespace: platform
    user: pineone-oidc
  name: pineone-dev-k8s-platform
current-context: pineone-dev-k8s-platform
kind: Config
preferences: {}
users:
- name: pineone-oidc
  user:
    exec:
      apiVersion: client.authentication.k8s.io/v1beta1
      args:
      - oidc-login
      - get-token
      - --oidc-issuer-url=https://dev.pineone.com:20445/auth/realms/pineone-account
      - --oidc-client-id=pineone-dev-k8s
      - --oidc-client-secret=qQtgDu1SRPVvhnKLeyUa8LftsbMvq2mU
      - --listen-address=127.0.0.1:8081
      command: kubectl
      env: null
      provideClusterInfo: false
```

## **4. 명령어 수행 (kubectl)**

- oidc 연동되어 로그인 후 권한 부여 받아서 명령어 처리 됨
- modelready 관련하여 namespace 2개 생성 (uplus-mready-gateway, uplus-mready-model)

## **5. 기타**

~/.zshrc에 하기 설정해놓으면 터미널에서 사용 용이함.

- 아래 kns 명령어를 통해 내가 접근하고 하는 namespace를 변경해줘야함

```
alias k="kubectl --insecure-skip-tls-verify"

### Custom Function
function kns() {
    # 사용할 namespace 목록
    namespaces=("uplus-mready-gateway" "uplus-mready-model" "argocd")

    echo "Select a namespace:"
    selectns in "${namespaces[@]}"; do
        if [[ -n "$ns" ]]; then
            # alias 갱신
	    kubectl config set-context --current --namespace "$ns"
            echo "Namespace changed to '$ns'. Use 'k' for kubectl commands."
            breakelseecho "Invalid selection. Try again."
        fi
    done
}

function kc() {
    kubectl --insecure-skip-tls-verify exec --stdin --tty $1 -- /bin/sh
}
```