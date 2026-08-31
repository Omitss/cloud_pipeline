# app/auth/service.py
from sqlalchemy.orm import Session

from app.db.models import User
from . import redis_client, security
from .schema import LoginRequest, SignupRequest


def signup(db: Session, data: SignupRequest) -> User:
    if db.query(User).filter(User.email == data.email).first():
        raise ValueError("이미 가입된 이메일입니다.")

    user = User(
        email=data.email,
        password_hash=security.hash_password(data.password),
        nickname=data.nickname,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate(db: Session, data: LoginRequest) -> User:
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not security.verify_password(data.password, user.password_hash):
        raise ValueError("이메일 또는 비밀번호가 올바르지 않습니다.")
    return user


def issue_tokens(user: User) -> tuple[str, str]:
    access_token = security.create_access_token(user.id)
    refresh_token, jti, expires_at = security.create_refresh_token(user.id)
    redis_client.store_refresh_token(user.id, jti, expires_at)
    return access_token, refresh_token


def refresh_access_token(db: Session, refresh_token: str) -> tuple[str, User]:
    try:
        payload = security.decode_token(refresh_token)
    except Exception:
        raise ValueError("유효하지 않은 refresh token입니다.")

    if payload.get("type") != "refresh":
        raise ValueError("refresh token이 아닙니다.")

    user_id = int(payload["sub"])
    jti = payload["jti"]

    if not redis_client.is_refresh_token_valid(user_id, jti):
        raise ValueError("만료되었거나 폐기된 refresh token입니다.")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("사용자를 찾을 수 없습니다.")

    return security.create_access_token(user_id), user
