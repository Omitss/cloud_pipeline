from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app import config
from app.imageRag import service
from app.imageRag.web import router as imagerag_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    count = service.build_cache()
    print(f"[imageRag] 캐시 생성 완료: {count}개 이미지 처리")
    yield


app = FastAPI(title="imageRag API", lifespan=lifespan)

app.include_router(imagerag_router)
app.mount("/images", StaticFiles(directory=config.IMAGES_DIR), name="images")