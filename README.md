## FastAPI Greeting API

- `GET /health`: 헬스체크
- `POST /introduce`: `{ "name": "홍길동" }` -> `{ "message": "저의 이름은 홍길동입니다." }`

### 로컬 실행

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 배포 과정

### 태그 설정

```bash
TAG=sha-$(date +"%m%d-%H%M")
```

### 빌드 및 업로드

```bash
docker buildx build --platform linux/amd64 \
  -t dev.pineone.com:20444/uplus-mready/fastapi-greet:$TAG \
  --push .
```

### 배포

1. 위에서 Secret이 없으면 먼저 생성
2. `deployment.yaml`에서 이미지 태그 등 수정
3. 적용:

```bash
k apply -f k8s/deployment.yaml
```

