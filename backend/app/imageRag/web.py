from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from .schema import ImageRagResponse
from . import service

router = APIRouter(prefix="/imagerag", tags=["imageRag"])


@router.post("/search", response_model=ImageRagResponse)
async def search_similar_food(
    file: UploadFile = File(...),
    top_k: int = Form(5, ge=1, le=50),
):
    """
    음식 사진을 업로드하면, images/ 폴더 내 유사한 음식 사진들을
    코사인 유사도 기준으로 찾아 이름/설명과 함께 반환한다.
    top_k: 반환할 결과 개수 (기본 5, 1~50)
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="이미지 파일만 업로드 가능합니다.")

    image_bytes = await file.read()

    try:
        return service.search_similar_images(image_bytes, top_k=top_k)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))