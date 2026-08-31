from pydantic import BaseModel, Field
from typing import List


class SimilarImageResult(BaseModel):
    """검색된 유사 음식 이미지 1건"""
    dish_name: str = Field(..., description="음식 이름 (images 하위 폴더명)")
    image_path: str = Field(..., description="가장 유사한 참조 이미지의 S3 presigned URL")
    similarity: float = Field(..., description="코사인 유사도 (0~1, 높을수록 유사)")
    caption: str = Field(..., description="참조 이미지에 대한 GPT 생성 설명")


class ImageRagResponse(BaseModel):
    """이미지 RAG 검색 결과 응답"""
    query_caption: str = Field(..., description="업로드된 이미지에 대한 GPT 생성 설명")
    results: List[SimilarImageResult] = Field(..., description="유사도 상위 결과 목록")