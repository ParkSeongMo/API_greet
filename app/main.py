import asyncio

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from threading import Lock


app = FastAPI(title="Greeting API")
app.state.is_ready = True
app.state.ready_lock = Lock()


class GreetRequest(BaseModel):
    name: str


@app.get("/health")
def health_check():
    return {"status": "ok"}

# @app.get("/ready")
# def ready_check():
#     # 1) 필수 의존성 점검 (현재 없으면 바로 ready)
#     # 예: DB ping, Redis ping, 내부 API 호출 등
#     with app.state.ready_lock:
#         is_ready = bool(app.state.is_ready)
#     # 2) 준비 안 됐으면 503 반환
#     if not is_ready:
#         raise HTTPException(status_code=503, detail="service not ready")
#     # 3) 준비 완료면 200 반환
#     return {"ready": True}


class ReadyUpdateRequest(BaseModel):
    ready: bool


# @app.post("/ready")
# def set_ready(payload: ReadyUpdateRequest):
#     with app.state.ready_lock:
#         app.state.is_ready = bool(payload.ready)
#         current = bool(app.state.is_ready)
#     return {"ready": current}

@app.post("/greet")
def greet(payload: GreetRequest):
    name = payload.name.strip()
    if not name:
        raise HTTPException(status_code=422, detail="이름은 비어 있을 수 없습니다.")
    return {"message": f"반가워! {name}"}


class DelayRequest(BaseModel):
    delay: float = Field(..., gt=0, description="딜레이 시간(초), 응답 result에 그대로 반영")


@app.post("/delay")
async def delay_endpoint(payload: DelayRequest):
    await asyncio.sleep(payload.delay)
    return {"result": f"{payload.delay}초"}

