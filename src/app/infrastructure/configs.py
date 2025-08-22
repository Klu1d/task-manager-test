from os import environ as env

from pydantic import Field, BaseModel

class PostgresConfig(BaseModel):
    host: str = Field(alias="POSTGRES_HOST")
    port: int = Field(alias="POSTGRES_PORT")
    user: str = Field(alias="POSTGRES_USER")
    password: str = Field(alias="POSTGRES_PASSWORD")
    database: str = Field(alias="POSTGRES_DB")

    @property
    def uri(self) -> str:
        # full_url = "postgresql+asyncpg://"
        full_url = "postgresql+psycopg://"
        full_url += f"{self.user}:{self.password}"
        full_url += f"@{self.host}:{self.port}/{self.database}"
        return full_url



class Config(BaseModel):
    postgres: PostgresConfig = Field(default_factory=lambda: PostgresConfig(**env))