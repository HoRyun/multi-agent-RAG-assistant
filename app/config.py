from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # WHY (KR): .env 값을 FastAPI 코드에서 직접 읽지 않고 설정 객체로 모읍니다.
    # 나중에 Docker Compose로 app을 옮겨도 이 파일의 env 값만 바꾸면 됩니다.
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    EMBEDDING_DIM: int = 768

    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"

    @property
    def database_url(self) -> str:
        """DB 연결 URL을 조합해 반환한다. URL 조합 책임을 config에 집중한다."""
        return (
            f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


# WHY (KR): 앱 전체에서 같은 설정 객체를 재사용합니다.
# v1에서는 단순성을 위해 DI 대신 module-level singleton으로 둡니다.
settings = Settings()