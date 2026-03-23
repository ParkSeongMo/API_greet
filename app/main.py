from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI(title="Greeting API")


class GreetRequest(BaseModel):
    name: str


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/greet")
def greet(payload: GreetRequest):
    name = payload.name.strip()
    if not name:
        raise HTTPException(status_code=422, detail="이름은 비어 있을 수 없습니다.")
    return {"message": f"반가워! {name}"}

