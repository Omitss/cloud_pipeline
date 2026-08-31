# app/imageRag/service.py
import json
import base64
from pathlib import Path
from typing import List

import numpy as np
from openai import OpenAI

from app import config
from .schema import SimilarImageResult, ImageRagResponse

IMAGES_DIR = config.IMAGES_DIR
CACHE_PATH = config.CACHE_PATH
CAPTION_MODEL = config.CAPTION_MODEL
EMBED_MODEL = config.EMBED_MODEL

client = OpenAI(max_retries=8)  # OPENAI_API_KEY는 app.config 의 load_dotenv()로 로드됨. 레이트리밋(429) 등 일시적 오류는 SDK가 자동 백오프 후 재시도


def _encode_image_base64(path: Path) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def _caption_image(image_b64: str) -> str:
    """이미지를 짧은 한국어 설명(캡션)으로 변환"""
    resp = client.chat.completions.create(
        model=CAPTION_MODEL,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "이 음식 사진을 한두 문장으로 간단히 설명해줘. 음식 이름과 특징 위주로.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_b64}",
                            "detail": "low",
                        },
                    },
                ],
            }
        ],
        max_tokens=100,
    )
    return resp.choices[0].message.content.strip()


def _embed_text(text: str) -> List[float]:
    resp = client.embeddings.create(model=EMBED_MODEL, input=text)
    return resp.data[0].embedding


def _cosine_similarity(a: List[float], b: List[float]) -> float:
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def build_cache(force: bool = False) -> int:
    """
    images/ 하위 폴더(음식 이름별)를 순회하며
    캡션 + 임베딩을 생성해 CACHE_PATH(json)에 저장.
    이미 캐시에 있는 이미지는 force=True가 아니면 건너뜀.
    반환값: 새로 처리한 이미지 개수
    """
    cache = {}
    if CACHE_PATH.exists() and not force:
        cache = json.loads(CACHE_PATH.read_text(encoding="utf-8"))

    processed = 0
    for dish_dir in sorted(IMAGES_DIR.iterdir()):
        if not dish_dir.is_dir():
            continue
        dish_name = dish_dir.name

        for img_path in dish_dir.glob("*.*"):
            key = str(img_path.relative_to(IMAGES_DIR))
            if key in cache and not force:
                continue

            try:
                image_b64 = _encode_image_base64(img_path)
                caption = _caption_image(image_b64)
                embedding = _embed_text(caption)
            except Exception as e:
                print(f"[imageRag] {key} 처리 실패, 건너뜀: {e}")
                continue

            cache[key] = {
                "dish_name": dish_name,
                "image_path": str(img_path),
                "caption": caption,
                "embedding": embedding,
            }
            processed += 1

            # 이미지 하나 처리할 때마다 즉시 저장 (중간에 실패해도 이미 처리한 건 재호출하지 않도록)
            CACHE_PATH.write_text(
                json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8"
            )

    return processed


def search_similar_images(image_bytes: bytes, top_k: int = 5) -> ImageRagResponse:
    if not CACHE_PATH.exists():
        raise RuntimeError(
            "임베딩 캐시가 없습니다. 서버가 시작되면서 자동으로 생성되므로 서버가 완전히 기동됐는지 확인하세요."
        )

    cache = json.loads(CACHE_PATH.read_text(encoding="utf-8"))

    query_b64 = base64.b64encode(image_bytes).decode("utf-8")
    query_caption = _caption_image(query_b64)
    query_embedding = _embed_text(query_caption)

    scored = []
    for entry in cache.values():
        sim = _cosine_similarity(query_embedding, entry["embedding"])
        scored.append(
            SimilarImageResult(
                dish_name=entry["dish_name"],
                image_path=entry["image_path"],
                similarity=round(sim, 4),
                caption=entry["caption"],
            )
        )

    scored.sort(key=lambda r: r.similarity, reverse=True)

    return ImageRagResponse(query_caption=query_caption, results=scored[:top_k])