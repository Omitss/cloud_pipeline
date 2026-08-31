# app/imageRag/service.py
import base64
import json
from typing import List

import boto3
import numpy as np
from openai import OpenAI

from app.config import settings, CAPTION_MODEL, EMBED_MODEL, CACHE_PATH
from .schema import SimilarImageResult, ImageRagResponse

client = OpenAI(max_retries=8)  # OPENAI_API_KEY는 app.config 의 load_dotenv()로 로드됨. 레이트리밋(429) 등 일시적 오류는 SDK가 자동 백오프 후 재시도


def _build_s3_client():
    kwargs = {"region_name": settings.AWS_REGION}
    # 로컬 개발 등 명시적 키가 있을 때만 넘기고, 없으면 boto3 기본 자격증명 체인
    # (EC2 IAM 역할 / 환경변수 / ~/.aws/credentials)이 알아서 찾도록 둔다.
    if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
        kwargs["aws_access_key_id"] = settings.AWS_ACCESS_KEY_ID
        kwargs["aws_secret_access_key"] = settings.AWS_SECRET_ACCESS_KEY
    return boto3.client("s3", **kwargs)


s3_client = _build_s3_client()


def _iter_s3_image_keys():
    """
    S3_BUCKET_NAME 버킷의 S3_IMAGES_PREFIX/음식이름/파일명 오브젝트를 전부 순회한다.
    yield (key, dish_name)
    """
    prefix = f"{settings.S3_IMAGES_PREFIX}/"
    paginator = s3_client.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=settings.S3_BUCKET_NAME, Prefix=prefix):
        for obj in page.get("Contents", []):
            key = obj["Key"]
            if key.endswith("/") or obj["Size"] == 0:
                continue  # "폴더" 마커 오브젝트는 스킵

            rest = key[len(prefix):]
            parts = rest.split("/")
            if len(parts) < 2:
                continue  # images/파일명 처럼 음식 폴더 없이 바로 있는 오브젝트는 스킵

            dish_name = parts[0]
            yield key, dish_name


def _download_image_bytes(key: str) -> bytes:
    obj = s3_client.get_object(Bucket=settings.S3_BUCKET_NAME, Key=key)
    return obj["Body"].read()


def _encode_image_base64(image_bytes: bytes) -> str:
    return base64.b64encode(image_bytes).decode("utf-8")


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


def _presigned_url(key: str, expires_in: int = 3600) -> str:
    return s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.S3_BUCKET_NAME, "Key": key},
        ExpiresIn=expires_in,
    )


def build_cache(force: bool = False) -> int:
    """
    S3의 S3_IMAGES_PREFIX/음식이름/ 아래 이미지들을 순회하며
    캡션 + 임베딩을 생성해 CACHE_PATH(json)에 저장.
    이미 캐시에 있는 오브젝트는 force=True가 아니면 건너뜀.
    반환값: 새로 처리한 이미지 개수
    """
    cache = {}
    if CACHE_PATH.exists() and not force:
        cache = json.loads(CACHE_PATH.read_text(encoding="utf-8"))

    processed = 0
    for key, dish_name in _iter_s3_image_keys():
        if key in cache and not force:
            continue

        try:
            image_bytes = _download_image_bytes(key)
            image_b64 = _encode_image_base64(image_bytes)
            caption = _caption_image(image_b64)
            embedding = _embed_text(caption)
        except Exception as e:
            print(f"[imageRag] {key} 처리 실패, 건너뜀: {e}")
            continue

        cache[key] = {
            "dish_name": dish_name,
            "s3_key": key,
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

    query_b64 = _encode_image_base64(image_bytes)
    query_caption = _caption_image(query_b64)
    query_embedding = _embed_text(query_caption)

    scored = []
    for entry in cache.values():
        if "s3_key" not in entry:
            continue  # 로컬 파일 시스템 시절의 옛 캐시 항목(스키마 다름)은 건너뜀

        sim = _cosine_similarity(query_embedding, entry["embedding"])
        scored.append(
            SimilarImageResult(
                dish_name=entry["dish_name"],
                image_path=_presigned_url(entry["s3_key"]),
                similarity=round(sim, 4),
                caption=entry["caption"],
            )
        )

    scored.sort(key=lambda r: r.similarity, reverse=True)

    return ImageRagResponse(query_caption=query_caption, results=scored[:top_k])
