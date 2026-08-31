from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.auth.web import router as auth_router
from app.imageRag import service
from app.imageRag.web import router as imagerag_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # S3 접근/자격증명 문제로 캐시 생성이 실패해도 서버 자체는 뜨게 둔다.
    # (기존 캐시로 검색은 계속되고, 캐시가 아예 없으면 /imagerag/search가 500으로 알려준다.)
    try:
        count = service.build_cache()
        print(f"[imageRag] 캐시 생성 완료: {count}개 이미지 처리")
    except Exception as e:
        print(f"[imageRag] 캐시 생성 실패, 기존 캐시로 계속 진행: {e}")
    yield


app = FastAPI(title="imageRag API", lifespan=lifespan)

app.include_router(imagerag_router)
app.include_router(auth_router)