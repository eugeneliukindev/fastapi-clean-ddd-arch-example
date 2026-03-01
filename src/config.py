from pathlib import Path
from typing import Annotated, Final

from pydantic import BaseModel, ConfigDict, Field, NonNegativeInt, PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

BASE_DIR: Final[Path] = Path(__file__).resolve().parent.parent

_Port = Annotated[int, Field(ge=1024, le=65_535)]


class DatabaseConfig(BaseModel):
    drivername: PostgresDsn = "postgresql+asyncpg"  # type: ignore[assignment]
    username: str
    password: str
    host: str = "localhost"
    port: _Port = 5432
    database: str

    echo: bool = False
    echo_pool: bool = False
    pool_size: NonNegativeInt = 10
    max_overflow: NonNegativeInt = 5

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @computed_field  # type: ignore[prop-decorator]
    @property
    def url(self) -> URL:
        return URL.create(
            drivername=self.drivername,  # type: ignore[arg-type]
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
        )


class Settings(BaseSettings):
    db: DatabaseConfig

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_prefix="MY_APP__",
        env_file=[BASE_DIR / ".env.example", BASE_DIR / ".env"],
        env_nested_delimiter="__",
        extra="ignore",
    )


settings = Settings()
