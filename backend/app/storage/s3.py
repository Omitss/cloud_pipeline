#s3 CRUD코드

from pathlib import Path
from typing import List, Optional

import boto3
from botocore.exceptions import ClientError

from .config import settings


def _get_client():
    """
    AWS_ACCESS_KEY_ID/SECRET이 .env에 있으면 그걸 사용(로컬 개발),
    없으면 boto3가 EC2 IAM 역할을 자동으로 사용(운영 환경).
    """
    if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
        return boto3.client(
            "s3",
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
    return boto3.client("s3", region_name=settings.AWS_REGION)


s3_client = _get_client()
BUCKET = settings.S3_BUCKET_NAME
PREFIX = settings.S3_IMAGES_PREFIX.rstrip("/")


def _key(dish_name: str, filename: str) -> str:
    """images/{dish_name}/{filename} 형태의 S3 key 생성"""
    return f"{PREFIX}/{dish_name}/{filename}"


# ---------- Create ----------
def upload_image(dish_name: str, filename: str, file_bytes: bytes, content_type: str = "image/jpeg") -> str:
    """
    images/{dish_name}/{filename} 경로로 이미지 업로드.
    반환값: 저장된 S3 key
    """
    key = _key(dish_name, filename)
    s3_client.put_object(
        Bucket=BUCKET,
        Key=key,
        Body=file_bytes,
        ContentType=content_type,
    )
    return key


def upload_local_file(dish_name: str, local_path: Path) -> str:
    """로컬 파일 경로를 그대로 업로드할 때 사용 (마이그레이션용)"""
    key = _key(dish_name, local_path.name)
    s3_client.upload_file(str(local_path), BUCKET, key)
    return key


# ---------- Read ----------
def list_dish_folders() -> List[str]:
    """images/ 바로 아래의 음식 폴더 목록 조회"""
    resp = s3_client.list_objects_v2(
        Bucket=BUCKET, Prefix=f"{PREFIX}/", Delimiter="/"
    )
    folders = []
    for cp in resp.get("CommonPrefixes", []):
        # 'images/갈비구이/' -> '갈비구이'
        folder = cp["Prefix"].rstrip("/").split("/")[-1]
        folders.append(folder)
    return folders


def list_images_in_dish(dish_name: str) -> List[str]:
    """특정 음식 폴더 안의 이미지 key 목록 조회"""
    prefix = f"{PREFIX}/{dish_name}/"
    resp = s3_client.list_objects_v2(Bucket=BUCKET, Prefix=prefix)
    return [obj["Key"] for obj in resp.get("Contents", []) if obj["Key"] != prefix]


def get_image_bytes(dish_name: str, filename: str) -> bytes:
    """이미지 하나를 바이트로 다운로드"""
    key = _key(dish_name, filename)
    try:
        resp = s3_client.get_object(Bucket=BUCKET, Key=key)
        return resp["Body"].read()
    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchKey":
            raise FileNotFoundError(f"S3에 이미지가 없습니다: {key}")
        raise


def get_presigned_url(dish_name: str, filename: str, expires_in: int = 3600) -> str:
    """프론트에서 직접 접근할 수 있는 임시 URL 발급 (버킷이 private일 때 사용)"""
    key = _key(dish_name, filename)
    return s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": BUCKET, "Key": key},
        ExpiresIn=expires_in,
    )


# ---------- Update ----------
def replace_image(dish_name: str, filename: str, new_file_bytes: bytes, content_type: str = "image/jpeg") -> str:
    """같은 key에 새 이미지로 덮어쓰기 (put_object가 곧 upsert이므로 upload_image와 동일 동작)"""
    return upload_image(dish_name, filename, new_file_bytes, content_type)


# ---------- Delete ----------
def delete_image(dish_name: str, filename: str) -> None:
    key = _key(dish_name, filename)
    s3_client.delete_object(Bucket=BUCKET, Key=key)


def delete_dish_folder(dish_name: str) -> int:
    """음식 폴더 전체 삭제. 반환값: 삭제된 객체 수"""
    keys = list_images_in_dish(dish_name)
    if not keys:
        return 0
    s3_client.delete_objects(
        Bucket=BUCKET,
        Delete={"Objects": [{"Key": k} for k in keys]},
    )
    return len(keys)