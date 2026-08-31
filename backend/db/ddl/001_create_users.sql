-- DataGrip 등에서 직접 실행하는 DDL. app/db/models.py의 User 모델과 동일한 스키마로 맞춰둘 것.
-- 스키마를 바꿀 때는 이 파일과 app/db/models.py를 같이 수정한다 (마이그레이션 도구 없이 수동 관리).

CREATE TABLE IF NOT EXISTS users (
    id              BIGSERIAL PRIMARY KEY,
    email           VARCHAR(255) NOT NULL UNIQUE,
    password_hash   VARCHAR(255) NOT NULL,
    nickname        VARCHAR(100) NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);
