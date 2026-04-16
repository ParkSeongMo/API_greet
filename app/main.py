import asyncio

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from threading import Lock


app = FastAPI(title="Greeting API")
app.state.is_ready = True
app.state.ready_lock = Lock()


class GreetRequest(BaseModel):
    name: str


@app.get("/healthz")
def health_check():
    return {"status": "ok"}

@app.get("/readyz")
def ready_check():
    return {"status": "ok"}
    # # 1) 필수 의존성 점검 (현재 없으면 바로 ready)
    # # 예: DB ping, Redis ping, 내부 API 호출 등
    # with app.state.ready_lock:
    #     is_ready = bool(app.state.is_ready)
    # # 2) 준비 안 됐으면 503 반환
    # if not is_ready:
    #     raise HTTPException(status_code=503, detail="service not ready")
    # # 3) 준비 완료면 200 반환
    # return {"ready": True}


class ReadyUpdateRequest(BaseModel):
    ready: bool


@app.post("/ready")
def set_ready(payload: ReadyUpdateRequest):
    with app.state.ready_lock:
        app.state.is_ready = bool(payload.ready)
        current = bool(app.state.is_ready)
    return {"ready": current}

@app.post("/introduce")
def introduce(payload: IntroduceRequest):
    name = payload.name.strip()
    if not name:
        raise HTTPException(status_code=422, detail="이름은 비어 있을 수 없습니다.")
    return {"message": f"저의 이름은 {name}입니다."}


@app.get("/delay")
async def delay(
    delay_seconds: int = Query(0, ge=0, le=300, description="응답을 지연할 초(0~300)"),
):
    await asyncio.sleep(delay_seconds)
    return {"message": f"{delay_seconds}초 지연되어 응답"}

