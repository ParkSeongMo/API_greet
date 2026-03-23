## FastAPI Greeting API

- `GET /health`: 헬스체크
- `POST /greet`: `{ "name": "홍길동" }` -> `{ "message": "반가워! 홍길동" }`

### 로컬 실행

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

