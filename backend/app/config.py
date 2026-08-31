# app/config.py
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent  # backend/
PROJECT_DIR = BASE_DIR.parent  # project/
load_dotenv(PROJECT_DIR / ".env")

IMAGES_DIR = BASE_DIR / "images"
CACHE_PATH = BASE_DIR / "app" / "imageRag" / "embeddings_cache.json"

CAPTION_MODEL = "gpt-4o-mini"
EMBED_MODEL = "text-embedding-3-small"
