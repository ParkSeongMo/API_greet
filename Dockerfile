FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 비루트 사용자(쿠버네티스 권장)
RUN useradd -m appuser

# 의존성 설치 레이어 캐시 활용
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY app ./app

EXPOSE 8000

USER appuser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

