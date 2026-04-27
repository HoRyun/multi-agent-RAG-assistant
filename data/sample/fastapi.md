# FastAPI 개요

FastAPI는 Python으로 API를 빠르게 만들기 위한 모던 웹 프레임워크다. Starlette을 기반으로 하며 Pydantic을 사용해 데이터 검증을 처리한다.

## 주요 특징

FastAPI는 타입 힌트를 적극 활용한다. 함수 파라미터에 타입을 선언하면 자동으로 요청 데이터를 파싱하고 검증한다. 잘못된 데이터가 들어오면 422 Unprocessable Entity 응답을 자동으로 반환한다.

OpenAPI 문서가 자동으로 생성된다. `/docs` 경로에서 Swagger UI를, `/redoc`에서 ReDoc UI를 바로 확인할 수 있다. 별도의 문서 작업 없이 코드만으로 API 명세가 유지된다.

## 비동기 지원

FastAPI는 async/await를 기본으로 지원한다. 엔드포인트 함수를 `async def`로 선언하면 비동기로 실행된다. I/O 바운드 작업이 많은 서비스에서 성능 이점이 크다.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

## 의존성 주입

FastAPI의 Depends 시스템을 사용하면 공통 로직(인증, DB 세션 등)을 여러 엔드포인트에서 재사용할 수 있다.

```python
from fastapi import Depends

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users")
async def get_users(db=Depends(get_db)):
    return db.query(User).all()
```

## Pydantic 모델

요청과 응답 데이터는 Pydantic BaseModel로 정의한다. 타입 검증, 직렬화, JSON 변환이 자동으로 처리된다.

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = False
```

FastAPI는 이 모델을 바탕으로 OpenAPI 스키마를 자동 생성하고, 요청 본문을 자동으로 파싱한다.
