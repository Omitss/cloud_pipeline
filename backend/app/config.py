import os
from pathlib import Path
from dotenv import load_dotenv

# backend/.env 로드
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # backend/
load_dotenv(BASE_DIR / ".env")


class Settings:
    AWS_REGION: str = os.getenv("AWS_REGION", "ap-northeast-2")
    S3_BUCKET_NAME: str = os.getenv("S3_BUCKET_NAME", "omits-s3-pipeline")
    S3_IMAGES_PREFIX: str = os.getenv("S3_IMAGES_PREFIX", "images")

    # 로컬 개발 시에만 사용. 값이 없으면 boto3가 자동으로
    # EC2 IAM 역할 / 환경변수 / 자격증명 파일 순으로 탐색함.
    AWS_ACCESS_KEY_ID: str | None = os.getenv("AWS_ACCESS_KEY_ID") or None
    AWS_SECRET_ACCESS_KEY: str | None = os.getenv("AWS_SECRET_ACCESS_KEY") or None


settings = Settings()

# imageRag 서비스에서 사용하는 모델/캐시 경로.
# S3 마이그레이션으로 로컬 IMAGES_DIR은 없앴지만, 캡션/임베딩 캐시는 여전히 로컬 파일(json)에 저장한다.
CAPTION_MODEL = "gpt-4o-mini"
EMBED_MODEL = "text-embedding-3-small"
CACHE_PATH = Path(__file__).resolve().parent / "imageRag" / "embeddings_cache.json"